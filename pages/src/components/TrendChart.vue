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
            <template v-if="props.dataFilter === 'all-data'">
              <!-- 在 all-data 模式下显示 AC 题数、Rating 和总 AC 题数 -->
              <th @click="sortBy('atcoder')" :class="{ 'sortable': true, 'sorted-asc': sortKey === 'atcoder' && sortOrder === 1, 'sorted-desc': sortKey === 'atcoder' && sortOrder === -1 }">
                AtCoder题数
                <span v-if="sortKey === 'atcoder'" class="sort-indicator">
                  {{ sortOrder === 1 ? '↑' : '↓' }}
                </span>
              </th>
              <th @click="sortBy('atcoderRating')" :class="{ 'sortable': true, 'sorted-asc': sortKey === 'atcoderRating' && sortOrder === 1, 'sorted-desc': sortKey === 'atcoderRating' && sortOrder === -1 }">
                AtCoder Rating
                <span v-if="sortKey === 'atcoderRating'" class="sort-indicator">
                  {{ sortOrder === 1 ? '↑' : '↓' }}
                </span>
              </th>
              <th @click="sortBy('codeforces')" :class="{ 'sortable': true, 'sorted-asc': sortKey === 'codeforces' && sortOrder === 1, 'sorted-desc': sortKey === 'codeforces' && sortOrder === -1 }">
                Codeforces题数
                <span v-if="sortKey === 'codeforces'" class="sort-indicator">
                  {{ sortOrder === 1 ? '↑' : '↓' }}
                </span>
              </th>
              <th @click="sortBy('codeforcesRating')" :class="{ 'sortable': true, 'sorted-asc': sortKey === 'codeforcesRating' && sortOrder === 1, 'sorted-desc': sortKey === 'codeforcesRating' && sortOrder === -1 }">
                Codeforces Rating
                <span v-if="sortKey === 'codeforcesRating'" class="sort-indicator">
                  {{ sortOrder === 1 ? '↑' : '↓' }}
                </span>
              </th>
              <th @click="sortBy('matiji')" :class="{ 'sortable': true, 'sorted-asc': sortKey === 'matiji' && sortOrder === 1, 'sorted-desc': sortKey === 'matiji' && sortOrder === -1 }">
                Matiji题数
                <span v-if="sortKey === 'matiji'" class="sort-indicator">
                  {{ sortOrder === 1 ? '↑' : '↓' }}
                </span>
              </th>
              <th @click="sortBy('matijiRating')" :class="{ 'sortable': true, 'sorted-asc': sortKey === 'matijiRating' && sortOrder === 1, 'sorted-desc': sortKey === 'matijiRating' && sortOrder === -1 }">
                Matiji Rating
                <span v-if="sortKey === 'matijiRating'" class="sort-indicator">
                  {{ sortOrder === 1 ? '↑' : '↓' }}
                </span>
              </th>
              <th @click="sortBy('total')" :class="{ 'sortable': true, 'sorted-asc': sortKey === 'total' && sortOrder === 1, 'sorted-desc': sortKey === 'total' && sortOrder === -1 }">
                总AC题数
                <span v-if="sortKey === 'total'" class="sort-indicator">
                  {{ sortOrder === 1 ? '↑' : '↓' }}
                </span>
              </th>
            </template>
            <template v-else-if="props.dataFilter === 'rating'">
              <!-- 在 rating 模式下显示各平台 Rating 但不显示总 Rating -->
              <th @click="sortBy('atcoderRating')" :class="{ 'sortable': true, 'sorted-asc': sortKey === 'atcoderRating' && sortOrder === 1, 'sorted-desc': sortKey === 'atcoderRating' && sortOrder === -1 }">
                AtCoder Rating
                <span v-if="sortKey === 'atcoderRating'" class="sort-indicator">
                  {{ sortOrder === 1 ? '↑' : '↓' }}
                </span>
              </th>
              <th @click="sortBy('codeforcesRating')" :class="{ 'sortable': true, 'sorted-asc': sortKey === 'codeforcesRating' && sortOrder === 1, 'sorted-desc': sortKey === 'codeforcesRating' && sortOrder === -1 }">
                Codeforces Rating
                <span v-if="sortKey === 'codeforcesRating'" class="sort-indicator">
                  {{ sortOrder === 1 ? '↑' : '↓' }}
                </span>
              </th>
              <th @click="sortBy('matijiRating')" :class="{ 'sortable': true, 'sorted-asc': sortKey === 'matijiRating' && sortOrder === 1, 'sorted-desc': sortKey === 'matijiRating' && sortOrder === -1 }">
                Matiji Rating
                <span v-if="sortKey === 'matijiRating'" class="sort-indicator">
                  {{ sortOrder === 1 ? '↑' : '↓' }}
                </span>
              </th>
            </template>
            <template v-else>
              <!-- 在 ac 模式下显示各平台 AC 题数和总 AC 题数 -->
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
                总AC题数
                <span v-if="sortKey === 'total'" class="sort-indicator">
                  {{ sortOrder === 1 ? '↑' : '↓' }}
                </span>
              </th>
            </template>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in sortedUsers" :key="user.name">
            <td>{{ user.name }}</td>
            <template v-if="props.dataFilter === 'all-data'">
              <!-- 在 all-data 模式下显示 AC 题数、Rating 和总 AC 题数 -->
              <td>{{ getUserPlatformCount(user.name, 'atcoder') }}</td>
              <td>{{ getUserPlatformRating(user.name, 'atcoder') }}</td>
              <td>{{ getUserPlatformCount(user.name, 'codeforces') }}</td>
              <td>{{ getUserPlatformRating(user.name, 'codeforces') }}</td>
              <td>{{ getUserPlatformCount(user.name, 'matiji') }}</td>
              <td>{{ getUserPlatformRating(user.name, 'matiji') }}</td>
              <td>{{ getUserTotalACCount(user.name) }}</td>
            </template>
            <template v-else-if="props.dataFilter === 'rating'">
              <!-- 在 rating 模式下显示各平台 Rating 但不显示总 Rating -->
              <td>{{ getUserPlatformRating(user.name, 'atcoder') }}</td>
              <td>{{ getUserPlatformRating(user.name, 'codeforces') }}</td>
              <td>{{ getUserPlatformRating(user.name, 'matiji') }}</td>
            </template>
            <template v-else>
              <!-- 在 ac 模式下显示各平台 AC 题数和总 AC 题数 -->
              <td>{{ getUserPlatformCount(user.name, 'atcoder') }}</td>
              <td>{{ getUserPlatformCount(user.name, 'codeforces') }}</td>
              <td>{{ getUserPlatformCount(user.name, 'matiji') }}</td>
              <td>{{ getUserTotalACCount(user.name) }}</td>
            </template>
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

// Platform data can be either a number (old format) or an object with ac_count and rating (new format)
interface PlatformDataValue {
  ac_count?: number;
  rating?: string | number;
  highest_rating?: string | number;
}

interface PlatformData {
  [date: string]: number | PlatformDataValue;
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
  dataFilter: string;
  chartType: string;
}

const props = withDefaults(defineProps<Props>(), {
  displayUsers: () => [],
  userData: () => ({}),
  currentPlatformFilter: 'all',
  dataFilter: 'ac',
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
  const platformTitles = {
    'atcoder': 'AtCoder',
    'codeforces': 'Codeforces',
    'matiji': 'Matiji'
  };
  
  const platformTitle = platformTitles[props.currentPlatformFilter as keyof typeof platformTitles] || '全部平台';
  
  let dataType = '';
  // 对于图表，all-data 模式不改变显示内容，保持之前的模式
  let currentDataFilter = props.dataFilter;
  if (currentDataFilter === 'all-data') {
    // 如果当前是 all-data 模式，使用默认的 ac 模式标题
    currentDataFilter = 'ac';
  }
  
  switch (currentDataFilter) {
    case 'ac':
      dataType = '刷题数量';
      break;
    case 'rating':
      dataType = 'Rating';
      break;
    default:
      dataType = '刷题数量';
  }
  
  return `${platformTitle} ${dataType}趋势`;
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
    } else if (sortKey.value === 'atcoderRating') {
      valueA = getUserPlatformRating(a.name, 'atcoder');
      valueB = getUserPlatformRating(b.name, 'atcoder');
    } else if (sortKey.value === 'codeforces') {
      valueA = getUserPlatformCount(a.name, 'codeforces');
      valueB = getUserPlatformCount(b.name, 'codeforces');
    } else if (sortKey.value === 'codeforcesRating') {
      valueA = getUserPlatformRating(a.name, 'codeforces');
      valueB = getUserPlatformRating(b.name, 'codeforces');
    } else if (sortKey.value === 'matiji') {
      valueA = getUserPlatformCount(a.name, 'matiji');
      valueB = getUserPlatformCount(b.name, 'matiji');
    } else if (sortKey.value === 'matijiRating') {
      valueA = getUserPlatformRating(a.name, 'matiji');
      valueB = getUserPlatformRating(b.name, 'matiji');
    } else if (sortKey.value === 'total') {
      // 总是使用总 AC 题数进行排序
      valueA = getUserTotalACCount(a.name);
      valueB = getUserTotalACCount(b.name);
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
    // 根据数据过滤类型获取相应的值
    const platformDataValue = platformData[latestDate];
    if (props.dataFilter === 'rating') {
      // 获取Rating值
      if (typeof platformDataValue === 'object' && 'rating' in platformDataValue && platformDataValue.rating !== undefined) {
        return parseInt(platformDataValue.rating as string) || 0;
      }
    } else if (props.dataFilter === 'all-data') {
      // 获取AC题数
      if (typeof platformDataValue === 'object' && 'ac_count' in platformDataValue && platformDataValue.ac_count !== undefined) {
        return platformDataValue.ac_count;
      }
    } else {
      // 默认为AC题数
      if (typeof platformDataValue === 'object' && 'ac_count' in platformDataValue && platformDataValue.ac_count !== undefined) {
        return platformDataValue.ac_count;
      } else if (typeof platformDataValue === 'number') {
        // 旧数据格式：直接是数值
        return platformDataValue;
      } else {
        // 如果是对象但没有ac_count，返回0
        return 0;
      }
    }
  }

  return 0;
};

// 获取用户特定平台的Rating
const getUserPlatformRating = (userName: string, platform: string): number => {
  const userHistory = props.userData[userName];
  if (!userHistory || !userHistory[platform as keyof StudentData]) {
    return 0;
  }

  const platformData = userHistory[platform as keyof StudentData];
  // 获取最新的日期数据
  const latestDate = getLatestDateFromPlatformData(platformData);
  if (latestDate && platformData[latestDate]) {
    // 获取Rating值
    const platformDataValue = platformData[latestDate];
    if (typeof platformDataValue === 'object' && 'rating' in platformDataValue && platformDataValue.rating !== undefined) {
      return parseInt(platformDataValue.rating as string) || 0;
    }
  }

  // 如果没有找到Rating数据，返回0
  return 0;
};

// 获取用户总AC题数（不包含Rating）
const getUserTotalACCount = (userName: string): number => {
  const userHistory = props.userData[userName];
  if (!userHistory) {
    return 0;
  }

  let total = 0;
  // 遍历所有平台，只计算AC题数，不计算Rating
  Object.entries(userHistory).forEach(([/* platform */, platformData]) => {
    const latestDate = getLatestDateFromPlatformData(platformData);
    if (latestDate && platformData[latestDate]) {
      const platformDataValue = platformData[latestDate];
      // 获取AC题数
      if (typeof platformDataValue === 'object' && 'ac_count' in platformDataValue && platformDataValue.ac_count !== undefined) {
        total += platformDataValue.ac_count;
      } else {
        // 旧数据格式：直接是数值
        total += platformDataValue;
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
  return sortedDates[0] || null;
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
          // 检查每个平台的数据格式并提取相应的值
          Object.entries(userHistory).forEach(([/* plat */, platformData]) => {
            // 检查当前日期是否有数据
            if (platformData[date]) {
              // 根据数据过滤类型获取相应值
              const platformDataValue = platformData[date];
              if (props.dataFilter === 'rating') {
                // 获取Rating值，如果不存在则为0
                if (typeof platformDataValue === 'object' && 'rating' in platformDataValue && platformDataValue.rating !== undefined) {
                  total += parseInt(platformDataValue.rating as string) || 0;
                } else {
                  // 如果没有Rating数据，则加0
                  total += 0;
                }
              } else if (props.dataFilter === 'all-data') {
                // 在all-data模式下，图表显示AC题数
                if (typeof platformDataValue === 'object' && 'ac_count' in platformDataValue && platformDataValue.ac_count !== undefined) {
                  total += platformDataValue.ac_count;
                } else if (typeof platformDataValue === 'number') {
                  // 旧数据格式
                  total += platformDataValue;
                } else {
                  // 如果没有AC题数数据，则加0
                  total += 0;
                }
              } else {
                // 默认获取AC题数
                if (typeof platformDataValue === 'object' && 'ac_count' in platformDataValue && platformDataValue.ac_count !== undefined) {
                  total += platformDataValue.ac_count;
                } else if (typeof platformDataValue === 'number') {
                  // 旧数据格式
                  total += platformDataValue;
                } else {
                  // 如果没有AC题数数据，则加0
                  total += 0;
                }
              }
            } else {
              // 如果该日期没有数据，则加0
              total += 0;
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
              const platformDataValue = platformData[date];
              // 根据数据过滤类型获取相应值
              if (props.dataFilter === 'rating') {
                // 获取Rating值，如果不存在则为0
                if (typeof platformDataValue === 'object' && 'rating' in platformDataValue && platformDataValue.rating !== undefined) {
                  return parseInt(platformDataValue.rating as string) || 0;
                } else {
                  // 如果没有Rating数据，返回0
                  return 0;
                }
              } else if (props.dataFilter === 'all-data') {
                // 在all-data模式下，图表显示AC题数
                if (typeof platformDataValue === 'object' && 'ac_count' in platformDataValue && platformDataValue.ac_count !== undefined) {
                  return platformDataValue.ac_count;
                } else if (typeof platformDataValue === 'number') {
                  // 旧数据格式
                  return platformDataValue;
                } else {
                  // 如果没有AC题数数据，返回0
                  return 0;
                }
              } else {
                // 默认获取AC题数
                if (typeof platformDataValue === 'object' && 'ac_count' in platformDataValue && platformDataValue.ac_count !== undefined) {
                  return platformDataValue.ac_count;
                } else if (typeof platformDataValue === 'number') {
                  // 旧数据格式
                  return platformDataValue;
                } else {
                  // 如果没有AC题数数据，返回0
                  return 0;
                }
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
              beginAtZero: props.dataFilter !== 'rating', // Rating不需要从0开始
              title: {
                display: true,
                text: props.dataFilter === 'rating' ? 'Rating' : '刷题数量'
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

// 监听属性变化并重绘图表 - 但 dataFilter 为 'all-data' 时不重绘
watch(() => [props.displayUsers, props.currentPlatformFilter, props.dataFilter, currentChartType.value, currentView.value], () => {
  nextTick(() => {
    if (currentView.value === 'chart') {
      // 仅在 dataFilter 不是 'all-data' 时重绘图表
      if (props.dataFilter !== 'all-data') {
        renderChart();
      }
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