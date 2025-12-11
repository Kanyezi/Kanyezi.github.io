<template>
  <div class="chart-container">
    <div class="chart-title">
      <span>{{ chartTitle }}</span>
      <div class="chart-actions">
        <button @click="changeView('table')" :class="{ active: currentView === 'table' }">表格</button>
        <button @click="changeView('chart')" :class="{ active: currentView === 'chart' }">图表</button>
      </div>
    </div>
    
    <!-- 图表 -->
    <div v-if="currentView === 'chart'">
      <canvas ref="trendChartRef"></canvas>
    </div>
    
    <!-- 数据表格 -->
    <div v-if="currentView === 'table'" class="data-table-container">
      <h3>数据表格</h3>
      <table class="data-table">
        <thead>
          <tr>
            <th @click="sortBy('name')" :class="{ 'sortable': true, 'sorted-asc': sortKey === 'name' && sortOrder === 1, 'sorted-desc': sortKey === 'name' && sortOrder === -1 }">
              姓名
              <span v-if="sortKey === 'name'" class="sort-indicator">
                {{ sortOrder === 1 ? '↑' : '↓' }}
              </span>
            </th>
            <th @click="sortBy('atcoder')" :class="{ 'sortable': true, 'sorted-asc': sortKey === 'atcoder' && sortOrder === 1, 'sorted-desc': sortKey === 'atcoder' && sortOrder === -1 }">
              AtCoder题数
              <span v-if="sortKey === 'atcoder'" class="sort-indicator">
                {{ sortOrder === 1 ? '↑' : '↓' }}
              </span>
            </th>
            <th @click="sortBy('codeforces')" :class="{ 'sortable': true, 'sorted-asc': sortKey === 'codeforces' && sortOrder === 1, 'sorted-desc': sortKey === 'codeforces' && sortOrder === -1 }">
              Codeforces题数
              <span v-if="sortKey === 'codeforces'" class="sort-indicator">
                {{ sortOrder === 1 ? '↑' : '↓' }}
              </span>
            </th>
            <th @click="sortBy('matiji')" :class="{ 'sortable': true, 'sorted-asc': sortKey === 'matiji' && sortOrder === 1, 'sorted-desc': sortKey === 'matiji' && sortOrder === -1 }">
              Matiji题数
              <span v-if="sortKey === 'matiji'" class="sort-indicator">
                {{ sortOrder === 1 ? '↑' : '↓' }}
              </span>
            </th>
            <th @click="sortBy('total')" :class="{ 'sortable': true, 'sorted-asc': sortKey === 'total' && sortOrder === 1, 'sorted-desc': sortKey === 'total' && sortOrder === -1 }">
              总题数
              <span v-if="sortKey === 'total'" class="sort-indicator">
                {{ sortOrder === 1 ? '↑' : '↓' }}
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in sortedUsers" :key="user.name">
            <td>{{ user.name }}</td>
            <td>{{ getUserPlatformCount(user.name, 'atcoder') }}</td>
            <td>{{ getUserPlatformCount(user.name, 'codeforces') }}</td>
            <td>{{ getUserPlatformCount(user.name, 'matiji') }}</td>
            <td>{{ getUserTotalCount(user.name) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
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
const currentView = ref('table'); // 'chart' or 'table'
const sortKey = ref(''); // 当前排序的列
const sortOrder = ref(1); // 1 为升序，-1 为降序

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
const dateLabels = computed(() => {
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
});

// 切换视图（图表/表格）
const changeView = (view: string) => {
  currentView.value = view;
};

// 排序方法
const sortBy = (key: string) => {
  if (sortKey.value === key) {
    // 如果当前排序列与点击列相同，切换升序/降序
    sortOrder.value = -sortOrder.value;
  } else {
    // 如果是新的排序列，设置为升序
    sortKey.value = key;
    sortOrder.value = 1;
  }
};

// 计算排序后的用户列表
const sortedUsers = computed(() => {
  if (!sortKey.value) {
    return props.displayUsers;
  }
  
  return [...props.displayUsers].sort((a, b) => {
    let valueA, valueB;
    
    if (sortKey.value === 'name') {
      valueA = a.name;
      valueB = b.name;
    } else if (sortKey.value === 'atcoder') {
      valueA = getUserPlatformCount(a.name, 'atcoder');
      valueB = getUserPlatformCount(b.name, 'atcoder');
    } else if (sortKey.value === 'codeforces') {
      valueA = getUserPlatformCount(a.name, 'codeforces');
      valueB = getUserPlatformCount(b.name, 'codeforces');
    } else if (sortKey.value === 'matiji') {
      valueA = getUserPlatformCount(a.name, 'matiji');
      valueB = getUserPlatformCount(b.name, 'matiji');
    } else if (sortKey.value === 'total') {
      valueA = getUserTotalCount(a.name);
      valueB = getUserTotalCount(b.name);
    } else {
      return 0;
    }
    
    // 确保对字符串和数字的排序处理
    if (typeof valueA === 'string' && typeof valueB === 'string') {
      return valueA.localeCompare(valueB) * sortOrder.value;
    } else {
      // 确保valueA和valueB是数字类型
      const numA = Number(valueA);
      const numB = Number(valueB);
      return (numA - numB) * sortOrder.value;
    }
  });
});

// 获取用户特定平台的计数
const getUserPlatformCount = (userName: string, platform: string): number => {
  const userHistory = props.userData[userName];
  if (!userHistory || !userHistory[platform as keyof StudentData]) {
    return 0;
  }

  const platformData = userHistory[platform as keyof StudentData];
  // 获取最新的日期数据
  const latestDate = getLatestDateFromPlatformData(platformData);
  if (latestDate && platformData[latestDate]) {
    // 新数据格式：{ ac_count: number }
    if (typeof platformData[latestDate] === 'object' && platformData[latestDate].ac_count !== undefined) {
      return platformData[latestDate].ac_count;
    } else {
      // 旧数据格式：直接是数值
      return platformData[latestDate];
    }
  }

  return 0;
};

// 获取用户总数量
const getUserTotalCount = (userName: string): number => {
  const userHistory = props.userData[userName];
  if (!userHistory) {
    return 0;
  }

  let total = 0;
  // 遍历所有平台
  Object.entries(userHistory).forEach(([platform, platformData]) => {
    const latestDate = getLatestDateFromPlatformData(platformData);
    if (latestDate && platformData[latestDate]) {
      // 新数据格式：{ ac_count: number }
      if (typeof platformData[latestDate] === 'object' && platformData[latestDate].ac_count !== undefined) {
        total += platformData[latestDate].ac_count;
      } else {
        // 旧数据格式：直接是数值
        total += platformData[latestDate];
      }
    }
  });

  return total;
};

// 获取平台数据中的最新日期
const getLatestDateFromPlatformData = (platformData: PlatformData): string | null => {
  const dates = Object.keys(platformData);
  if (dates.length === 0) return null;

  // 排序并返回最新的日期
  const sortedDates = dates.sort((a, b) => new Date(b).getTime() - new Date(a).getTime());
  return sortedDates[0];
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
        data = dateLabels.value.map(date => {
          const userHistory = props.userData[user.name];
          if (!userHistory) return 0;
          
          let total = 0;
          // 检查每个平台的数据格式并提取ac_count值
          Object.values(userHistory).forEach(platformData => {
            if (platformData[date]) {
              // 新数据格式：{ ac_count: number }
              if (typeof platformData[date] === 'object' && platformData[date].ac_count !== undefined) {
                total += platformData[date].ac_count;
              } else {
                // 旧数据格式：直接是数值
                total += platformData[date];
              }
            }
          });
          return total;
        });
      } else {
        // 单个平台：获取该平台的历史数据
        const userHistory = props.userData[user.name];
        if (userHistory && userHistory[platform as keyof StudentData]) {
          const platformData = userHistory[platform as keyof StudentData];
          data = dateLabels.value.map(date => {
            if (platformData[date]) {
              // 新数据格式：{ ac_count: number }
              if (typeof platformData[date] === 'object' && platformData[date].ac_count !== undefined) {
                return platformData[date].ac_count;
              } else {
                // 旧数据格式：直接是数值
                return platformData[date];
              }
            } else {
              return 0;
            }
          });
        } else {
          data = dateLabels.value.map(() => 0);
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
          labels: dateLabels.value,
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
                display: false,
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

// 监听属性变化并重绘图表
watch(() => [props.displayUsers, props.currentPlatformFilter, currentChartType.value, currentView.value], () => {
  nextTick(() => {
    if (currentView.value === 'chart') {
      renderChart();
    }
  });
}, { deep: true });

// 生命周期
onMounted(() => {
  nextTick(() => {
    if (currentView.value === 'chart') {
      renderChart();
    }
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
@import '../styles/root.css';
@import '../styles/TrendChart.css';
</style>