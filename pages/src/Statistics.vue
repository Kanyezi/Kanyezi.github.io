<template>
  <div class="container">
    <!-- 侧边栏 - 用户列表 -->
    <div class="sidebar">
      <div class="sidebar-header">
        <h2>用户列表</h2>
        <input 
          type="text" 
          class="user-search" 
          placeholder="搜索用户..." 
          v-model="searchTerm"
        >
      </div>
      <div class="user-list">
        <div 
          v-for="user in filteredUsers"
          :key="user.name"
          class="user-item"
          :class="{ active: selectedUsers.includes(user.name) }"
          @click="toggleUser(user.name)"
        >
          <div class="user-info">
            <div class="user-name">{{ user.name }}</div>
            <div class="user-stats">
              <span>atcoder: {{ user.atcoder }}</span>
              <span>codeforces: {{ user.codeforces }}</span>
              <span>matiji: {{ user.matiji }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 主内容区 -->
    <div class="main-content">
      <header>
        <h1>多用户刷题数据统计</h1>
      </header>
      
      <div class="controls">
        <div class="filter-group">
          <select class="filter-select" v-model="currentPeriodFilter">
            <option value="all">全部周期</option>
            <option value="last4">最近4期</option>
            <option value="last8">最近8期</option>
          </select>
          
          <select class="filter-select" v-model="currentUserFilter">
            <option value="all">全部用户</option>
            <option value="selected">仅选中用户</option>
          </select>
          
          <select class="filter-select" v-model="currentPlatformFilter">
            <option value="all">全部平台</option>
            <option value="atcoder">AtCoder</option>
            <option value="codeforces">Codeforces</option>
            <option value="matiji">Matiji</option>
          </select>
          
          <button class="btn" @click="compareMode">对比模式</button>
        </div>
        
        <div class="filter-group">
          <button class="btn" @click="refreshData">刷新数据</button>
        </div>
      </div>
      
      <div class="stats-cards">
        <div class="card">
          <h3>活跃用户数</h3>
          <div class="value">{{ activeUsersCount }}</div>
        </div>
        <div class="card">
          <h3>总刷题数量</h3>
          <div class="value">{{ totalCount.toLocaleString() }}</div>
        </div>
        <div class="card">
          <h3>平均刷题数</h3>
          <div class="value">{{ averageCount }}</div>
        </div>
        <div class="card">
          <h3>最高刷题数</h3>
          <div class="value">{{ maxCount }}</div>
        </div>
      </div>
      
      <div class="chart-container">
        <div class="chart-title">
          <span>用户刷题数量趋势</span>
          <div class="chart-actions">
            <button @click="trendChartType = 'line'" :class="{ active: trendChartType === 'line' }">折线图</button>
            <button @click="trendChartType = 'bar'" :class="{ active: trendChartType === 'bar' }">柱状图</button>
          </div>
        </div>
        <canvas ref="trendChart"></canvas>
      </div>
      
      <footer>
        <p>数据每10天更新一次 | 最后更新: <span>{{ lastUpdate }}</span></p>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, onBeforeUnmount, watch } from 'vue';
import Chart from 'chart.js/auto';

// 全局防抖超时变量，用于管理图表渲染的防抖
let chartRenderTimeout: ReturnType<typeof setTimeout> | null = null;

// 防抖函数
const debounce = <T extends (...args: any[]) => any>(func: T, wait: number) => {
  return (...args: Parameters<T>) => {
    if (chartRenderTimeout) clearTimeout(chartRenderTimeout);
    chartRenderTimeout = setTimeout(() => func(...args), wait);
  };
};

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

interface AppData {
  users: User[];
  data: Record<string, StudentData>;
}

// 响应式数据
const users = ref<User[]>([]);
const userData = ref<Record<string, StudentData>>({});
const lastUpdate = ref<string>(new Date().toISOString().split('T')[0] || '');
const searchTerm = ref<string>('');
const selectedUsers = ref<string[]>(['孙叶', '陈宣扬', '杜光明']);
const currentPeriodFilter = ref<string>('all');
const currentUserFilter = ref<string>('selected');
const currentPlatformFilter = ref<string>('all');
const trendChartType = ref<string>('line');
const trendChartInstance = ref<Chart | null>(null);
const trendChart = ref<HTMLCanvasElement | null>(null);

// 计算属性
const filteredUsers = computed(() => {
  if (!searchTerm.value) return users.value;
  return users.value.filter(user => 
    user.name.toLowerCase().includes(searchTerm.value.toLowerCase())
  );
});

const displayUsers = computed(() => {
  if (currentUserFilter.value === 'all') {
    return users.value;
  }
  return users.value.filter(user => selectedUsers.value.includes(user.name));
});

const activeUsersCount = computed(() => displayUsers.value.length);

const getPlatformTotal = (platform: string) => {
  if (platform === 'all') {
    return displayUsers.value.reduce((sum, user) => 
      sum + (user.atcoder + user.codeforces + user.matiji), 0
    );
  }
  return displayUsers.value.reduce((sum, user) => 
    sum + (user[platform as keyof User] as number), 0
  );
};

const totalCount = computed(() => {
  return getPlatformTotal(currentPlatformFilter.value);
});

const averageCount = computed(() => {
  if (displayUsers.value.length === 0) return 0;
  return Math.round(totalCount.value / displayUsers.value.length);
});

const maxCount = computed(() => {
  if (displayUsers.value.length === 0) return 0;
  if (currentPlatformFilter.value === 'all') {
    return Math.max(...displayUsers.value.map(user => 
      user.atcoder + user.codeforces + user.matiji
    ));
  }
  return Math.max(...displayUsers.value.map(user => 
    user[currentPlatformFilter.value as keyof User] as number
  ));
});


// 监听平台选择变化
watch(currentPlatformFilter, () => {
  renderCharts();
});

// 方法
const toggleUser = (userName: string) => {
  const index = selectedUsers.value.indexOf(userName);
  if (index > -1) {
    selectedUsers.value.splice(index, 1);
  } else {
    selectedUsers.value.push(userName);
  }
};

// 获取用户在选定平台的数据 - 暂时注释，需要时取消注释
/*
const getUserPlatformData = (userName: string, platform: string) => {
  const user = users.value.find(u => u.name === userName);
  if (!user) return 0;
  
  if (platform === 'all') {
    return user.atcoder + user.codeforces + user.matiji;
  }
  return user[platform as keyof User] as number;
};
*/

// 获取所有日期标签
const getDateLabels = () => {
  // 从所有用户的数据中获取所有唯一日期并排序
  const allDates = new Set<string>();
  
  displayUsers.value.forEach(user => {
    const userHistory = userData.value[user.name];
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

// 直接导入数据而不是通过fetch请求，避免CORS问题
import allData from '../public/all_data.json';

const loadData = async () => {
  try {
    // 使用导入的数据而不是fetch
    const data: AppData = allData;
    users.value = data.users;
    userData.value = data.data;
    await nextTick();
    // 使用立即渲染，不使用防抖
    immediateRenderCharts();
  } catch (error) {
    console.error('加载数据失败:', error);
  }
};

// renderTrendChart函数已移至文件下方并优化

// 获取平台显示名称
const getPlatformName = () => {
  switch (currentPlatformFilter.value) {
    case 'atcoder': return 'AtCoder';
    case 'codeforces': return 'Codeforces';
    case 'matiji': return 'Matiji';
    default: return '全部平台';
  }
};



// 直接渲染函数，用于非防抖场景（如初始化）
const renderCharts = () => {
  if (trendChart.value) {
    renderTrendChart();
  }
};

// 立即执行的渲染函数，用于初始加载和用户主动刷新
const immediateRenderCharts = () => {
  // 清除任何待处理的防抖调用
  if (chartRenderTimeout) {
    clearTimeout(chartRenderTimeout);
    chartRenderTimeout = null;
  }
  // 直接渲染，不使用防抖
  nextTick(() => {
    renderCharts();
  });
};

const refreshData = () => {
  lastUpdate.value = new Date().toISOString().split('T')[0] || '';
  loadData();
};

const compareMode = () => {
  // 可以在这里实现更复杂的对比模式逻辑
  alert(`对比模式已激活！当前平台: ${getPlatformName()}`);
};

// 使用防抖函数创建防抖版本的渲染函数
const debouncedRenderCharts = debounce(() => {
  nextTick(() => {
    renderCharts();
  });
}, 200); // 200ms的防抖延迟

// 优化监听逻辑，确保切换用户时图表能正确更新，使用防抖避免快速切换导致的错误
watch([currentUserFilter, selectedUsers, trendChartType], () => {
  debouncedRenderCharts();
}, { deep: true }); // 深度监听以确保用户选择变化时能触发更新

// 优化图表渲染函数，增强错误处理和实例管理
const renderTrendChart = () => {
  // 再次确保防抖执行期间组件仍然存在
  if (!trendChart.value) return;
  
  try {
    // 确保彻底销毁旧的图表实例，增加安全检查
    if (trendChartInstance.value) {
      // 检查图表实例是否有效
      if (trendChartInstance.value.destroy) {
        trendChartInstance.value.destroy();
      }
      trendChartInstance.value = null;
    }
    
    // 确保Canvas元素仍然在DOM中
    if (!document.body.contains(trendChart.value)) {
      console.warn('Canvas元素已从DOM中移除，跳过图表渲染');
      return;
    }
    
    const dateLabels = getDateLabels();
    const platform = currentPlatformFilter.value;
    
    const colors = [
      '#4a6cf7', '#28a745', '#ffc107', '#dc3545', 
      '#6f42c1', '#20c997', '#fd7e14', '#e83e8c'
    ];
    
    // 根据平台选择处理数据
    const datasets = displayUsers.value.map((user, index) => {
      let data: number[] = [];
      
      if (platform === 'all') {
        // 全部平台：计算每个日期的总和
        data = dateLabels.map(date => {
          const userHistory = userData.value[user.name];
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
        const userHistory = userData.value[user.name];
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
        backgroundColor: trendChartType.value === 'bar' ? colors[index % colors.length] : 'transparent',
        borderColor: colors[index % colors.length],
        borderWidth: 2,
        pointBackgroundColor: colors[index % colors.length],
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 5,
        tension: 0.3
      };
    });
    
    // 重新获取上下文，确保有效
    const ctx = trendChart.value.getContext('2d');
    if (ctx) {
      try {
        // 清除canvas内容，确保干净的绘制环境
        ctx.clearRect(0, 0, trendChart.value.width, trendChart.value.height);
        
        trendChartInstance.value = new Chart(ctx, {
          type: trendChartType.value as 'line' | 'bar',
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
                text: `${getPlatformName()} 刷题数量趋势`
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
            // 禁用动画以减少Canvas上下文错误风险
            animation: false
          }
        });
      } catch (error) {
        console.error('创建图表时出错:', error);
        // 清理可能部分创建的实例
        trendChartInstance.value = null;
      }
    }
  } catch (error) {
    console.error('图表渲染过程中出现未预期错误:', error);
    // 确保实例被清理
    if (trendChartInstance.value) {
      try {
        trendChartInstance.value.destroy();
      } catch (e) {
        console.warn('销毁图表实例时出错:', e);
      }
      trendChartInstance.value = null;
    }
  }
};

// 移除原有的renderTrendChart函数定义（已在上面重新定义）

// 生命周期
onMounted(() => {
  loadData();
});

onBeforeUnmount(() => {
    // 清理图表实例
    if (trendChartInstance.value) {
      trendChartInstance.value.destroy();
    }
    // 清理防抖超时
    if (chartRenderTimeout) {
      clearTimeout(chartRenderTimeout);
    }
  });
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

:root {
  --primary-color: #4a6cf7;
  --secondary-color: #6c757d;
  --success-color: #28a745;
  --warning-color: #ffc107;
  --danger-color: #dc3545;
  --light-bg: #f8f9fa;
  --dark-bg: #343a40;
  --border-color: #dee2e6;
  --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.container {
  display: flex;
  min-height: 100vh;
  background-color: #f5f7fa;
  color: #333;
  line-height: 1.6;
}

/* 侧边栏样式 */
.sidebar {
  width: 400px;
  background: white;
  box-shadow: var(--card-shadow);
  padding: 20px;
  overflow-y: auto;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border-color);
}

.sidebar-header h2 {
  color: var(--primary-color);
}

.user-search {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
}

.user-list {
  overflow-y: auto;
}

.user-item {
  display: flex;
  align-items: center;
  padding: 12px 10px;
  border-bottom: 1px solid var(--border-color);
  cursor: pointer;
  transition: background-color 0.2s;
}

.user-item:hover {
  background-color: var(--light-bg);
}

.user-item.active {
  background-color: rgba(74, 108, 247, 0.1);
  border-left: 3px solid var(--primary-color);
}

.user-info {
  flex: 1;
}

.user-name {
  font-weight: 600;
  margin-bottom: 4px;
}

.user-stats {
  font-size: 0.85rem;
  color: var(--secondary-color);
}
.user-stats span {
  background-color: var(--light-bg);
  padding: 2px 6px;
}
/* 主内容区样式 */
.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

header {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: var(--card-shadow);
  margin-bottom: 25px;
}

h1 {
  font-size: 1.8rem;
  margin-bottom: 10px;
  color: var(--dark-bg);
}


.controls {
  display: flex;
  justify-content: space-between;
  margin-bottom: 25px;
  flex-wrap: wrap;
  gap: 15px;
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: var(--card-shadow);
}

.filter-group {
  display: flex;
  gap: 15px;
  align-items: center;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 1rem;
  min-width: 150px;
}

.btn {
  padding: 8px 16px;
  background-color: var(--primary-color);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #3a5ce5;
}

.btn-outline {
  background-color: transparent;
  border: 1px solid var(--primary-color);
  color: var(--primary-color);
}

.btn-outline:hover {
  background-color: rgba(74, 108, 247, 0.1);
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: var(--card-shadow);
  text-align: center;
}

.card h3 {
  font-size: 0.9rem;
  color: var(--secondary-color);
  margin-bottom: 10px;
}

.card .value {
  font-size: 1.8rem;
  font-weight: bold;
  color: var(--primary-color);
}

.chart-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: var(--card-shadow);
  margin-bottom: 30px;
  position: relative;
  height: 500px;
}

.chart-container canvas {
  max-height: 450px !important;
  width: 100% !important;
}

.chart-title {
  font-size: 1.3rem;
  margin-bottom: 15px;
  color: var(--dark-bg);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-actions {
  display: flex;
  gap: 10px;
}

.chart-actions button {
  background: none;
  border: 1px solid var(--border-color);
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s;
}

.chart-actions button.active {
  background-color: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: var(--card-shadow);
}

.data-table th, .data-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.data-table th {
  background-color: var(--light-bg);
  font-weight: 600;
  color: var(--dark-bg);
}

.data-table tr:hover {
  background-color: var(--light-bg);
}

.period-badge {
  display: inline-block;
  padding: 4px 8px;
  background-color: var(--light-bg);
  border-radius: 4px;
  font-size: 0.85rem;
}

.trend-up {
  color: var(--success-color);
}

.trend-down {
  color: var(--danger-color);
}

footer {
  text-align: center;
  margin-top: 40px;
  padding: 20px;
  color: var(--secondary-color);
  font-size: 0.9rem;
}

/* 响应式设计 */
@media (max-width: 992px) {
  .container {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    max-height: 300px;
  }
}

@media (max-width: 768px) {
  .controls {
    flex-direction: column;
  }
  
  .filter-group {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .stats-cards {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 576px) {
  .stats-cards {
    grid-template-columns: 1fr;
  }
  
  .chart-actions {
    flex-direction: column;
  }
}
</style>