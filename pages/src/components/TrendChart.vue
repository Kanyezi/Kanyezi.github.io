<template>
  <div class="chart-container">
    <div class="chart-title">
      <span>{{ chartTitle }}</span>
      <div class="chart-actions">
        <button @click="changeChartType('line')" :class="{ active: currentChartType === 'line' }">折线图</button>
        <button @click="changeChartType('bar')" :class="{ active: currentChartType === 'bar' }">柱状图</button>
      </div>
    </div>
    <canvas ref="trendChartRef"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick, watch, computed } from 'vue';
import Chart from 'chart.js/auto';

// 定义数据类型
interface User {
  name: string;
  class: string;
  codeforces_id: string;
  atcoder_id: string;
  matiji_id: string;
  grade: number;
  atcoder: number;
  codeforces: number;
  matiji: number;
}

interface PlatformData {
  [date: string]: number;
}

interface StudentData {
  atcoder: PlatformData;
  codeforces: PlatformData;
  matiji: PlatformData;
}

interface Props {
  displayUsers: User[];
  userData: Record<string, StudentData>;
  currentPlatformFilter: string;
  chartType: string;
}

const props = withDefaults(defineProps<Props>(), {
  displayUsers: () => [],
  userData: () => ({}),
  currentPlatformFilter: 'all',
  chartType: 'line'
});

// 定义事件
interface Emits {
  (e: 'chart-type-change', chartType: string): void;
}

const emit = defineEmits<Emits>();

// 引用和响应式数据
const trendChartRef = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

// 计算属性
const chartTitle = computed(() => {
  switch (props.currentPlatformFilter) {
    case 'atcoder': return 'AtCoder 刷题数量趋势';
    case 'codeforces': return 'Codeforces 刷题数量趋势';
    case 'matiji': return 'Matiji 刷题数量趋势';
    default: return '全部平台 刷题数量趋势';
  }
});

const currentChartType = ref(props.chartType);

// 获取所有日期标签
const getDateLabels = () => {
  // 从所有用户的数据中获取所有唯一日期并排序
  const allDates = new Set<string>();
  
  props.displayUsers.forEach(user => {
    const userHistory = props.userData[user.name];
    if (userHistory) {
      Object.values(userHistory).forEach(platformData => {
        Object.keys(platformData).forEach(date => allDates.add(date));
      });
    }
  });
  
  // 将日期转换为Date对象进行排序，确保按照实际时间顺序递增
  return Array.from(allDates).sort((date1, date2) => {
    // 解析日期字符串为Date对象
    const d1 = new Date(date1);
    const d2 = new Date(date2);
    
    // 按日期从小到大排序（递增）
    return d1.getTime() - d2.getTime();
  });
};

// 图表渲染函数
const renderChart = () => {
  if (!trendChartRef.value) return;

  try {
    // 销毁旧的图表实例
    if (chartInstance) {
      chartInstance.destroy();
      chartInstance = null;
    }
    
    // 确保Canvas元素仍然在DOM中
    if (!document.body.contains(trendChartRef.value)) {
      console.warn('Canvas元素已从DOM中移除，跳过图表渲染');
      return;
    }
    
    const dateLabels = getDateLabels();
    const platform = props.currentPlatformFilter;
    
    const colors = [
      '#4a6cf7', '#28a745', '#ffc107', '#dc3545', 
      '#6f42c1', '#20c997', '#fd7e14', '#e83e8c'
    ];
    
    // 根据平台选择处理数据
    const datasets = props.displayUsers.map((user, index) => {
      let data: number[] = [];
      
      if (platform === 'all') {
        // 全部平台：计算每个日期的总和
        data = dateLabels.map(date => {
          const userHistory = props.userData[user.name];
          if (!userHistory) return 0;
          
          let total = 0;
          Object.values(userHistory).forEach(platformData => {
            if (platformData[date]) {
              total += platformData[date];
            }
          });
          return total;
        });
      } else {
        // 单个平台：获取该平台的历史数据
        const userHistory = props.userData[user.name];
        if (userHistory && userHistory[platform as keyof StudentData]) {
          const platformData = userHistory[platform as keyof StudentData];
          data = dateLabels.map(date => platformData[date] || 0);
        } else {
          data = dateLabels.map(() => 0);
        }
      }
      
      return {
        label: user.name,
        data: data,
        backgroundColor: currentChartType.value === 'bar' ? colors[index % colors.length] : 'transparent',
        borderColor: colors[index % colors.length],
        borderWidth: 2,
        pointBackgroundColor: colors[index % colors.length],
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 5,
        tension: 0.3
      };
    });
    
    // 获取上下文并创建图表
    const ctx = trendChartRef.value.getContext('2d');
    if (ctx) {
      chartInstance = new Chart(ctx, {
        type: currentChartType.value as 'line' | 'bar',
        data: {
          labels: dateLabels,
          datasets: datasets
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top' as const,
            },
            tooltip: {
              mode: 'index' as const,
              intersect: false
            },
            title: {
              display: true,
              text: chartTitle.value
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: '刷题数量'
              }
            },
            x: {
              title: {
                display: true,
                text: '日期'
              }
            }
          },
          animation: false
        }
      });
    }
  } catch (error) {
    console.error('图表渲染过程中出现未预期错误:', error);
    // 确保实例被清理
    if (chartInstance) {
      try {
        chartInstance.destroy();
      } catch (e) {
        console.warn('销毁图表实例时出错:', e);
      }
      chartInstance = null;
    }
  }
};

// 更改图表类型的方法
const changeChartType = (type: string) => {
  currentChartType.value = type;
  emit('chart-type-change', type);
  nextTick(() => {
    renderChart();
  });
};

// 监听属性变化并重绘图表
watch(() => [props.displayUsers, props.currentPlatformFilter, currentChartType.value], () => {
  nextTick(() => {
    renderChart();
  });
}, { deep: true });

// 生命周期
onMounted(() => {
  nextTick(() => {
    renderChart();
  });
});

onBeforeUnmount(() => {
  // 清理图表实例
  if (chartInstance) {
    chartInstance.destroy();
  }
});
</script>

<style scoped>
/* Import base framework styles */
@import '../styles/base-framework.css';

/* Import enhanced styles */
@import '../styles/enhanced-styles.css';
</style>