<template>
  <div class="container">
    <!-- 侧边栏 - 用户列表 -->
          <UserListSidebar
        :users="users"
        :selected-users="selectedUsers"
        :search-term="searchTerm"
        @toggle-user="toggleUser"
        @update:searchTerm="handleSearchChange"
      />
    
    <!-- 主内容区 -->
    <div class="main-content">
      <header>
        <h1>多用户刷题数据统计</h1>
      </header>
      
      <FilterControls
        :period-filter="currentPeriodFilter"
        :user-filter="currentUserFilter"
        :platform-filter="currentPlatformFilter"
        @update:period-filter="updatePeriodFilter"
        @update:user-filter="updateUserFilter"
        @update:platform-filter="updatePlatformFilter"
        
        @refresh-data="refreshData"
      />
      
      <StatsCards
        :active-users-count="activeUsersCount"
        :total-count="totalCount"
        :average-count="averageCount"
        :max-count="maxCount"
      />
      
      <TrendChart
        :display-users="displayUsers"
        :user-data="userData"
        :current-platform-filter="currentPlatformFilter"
        :chart-type="trendChartType"
        @chart-type-change="handleChartTypeChange"
      />
      
      <footer>
        <p>数据每10天更新一次 | 最后更新: <span>{{ lastUpdate }}</span></p>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue';
import UserListSidebar from './components/UserListSidebar.vue';
import StatsCards from './components/StatsCards.vue';
import TrendChart from './components/TrendChart.vue';
import FilterControls from './components/FilterControls.vue';

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

// 计算属性
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

// 方法
const toggleUser = (userName: string) => {
  const index = selectedUsers.value.indexOf(userName);
  if (index > -1) {
    selectedUsers.value.splice(index, 1);
  } else {
    selectedUsers.value.push(userName);
  }
};

const handleSearchChange = (searchValue: string) => {
  searchTerm.value = searchValue;
};

const handleFilterChange = (filters: { period: string; user: string; platform: string }) => {
  currentPeriodFilter.value = filters.period;
  currentUserFilter.value = filters.user;
  currentPlatformFilter.value = filters.platform;
};

const handleChartTypeChange = (chartType: string) => {
  trendChartType.value = chartType;
};

const updatePeriodFilter = (value: string) => {
  currentPeriodFilter.value = value;
};

const updateUserFilter = (value: string) => {
  currentUserFilter.value = value;
};

const updatePlatformFilter = (value: string) => {
  currentPlatformFilter.value = value;
};

// 直接导入数据而不是通过fetch请求，避免CORS问题
// 由于all_data.json在public目录下，需要使用动态导入
const loadAllData = async () => await fetch('/all_data.json').then(res => res.json());

const loadData = async () => {
  try {
    // 使用导入的数据而不是fetch
    // 筛选2025级数据
    const data: AppData = await loadAllData();
    const data25:AppData = {users:[],data:{}};
    // 收集所有日期以确定最后更新日期
    const allDates = new Set<string>();
    for(let i=0;i<data.users.length;i++){
      const u = data.users[i];   // ← 一次性收窄
      if (!u || u.grade !== 2025) continue;

      data25.users.push(u);
      const d = data.data[u.name];
      if (d) {
        data25.data[u.name] = d;   // 防止 data 里没有这个人
        // 收集所有平台的日期
        Object.values(d).forEach(platformData => {
          Object.keys(platformData).forEach(date => allDates.add(date));
        });
      }
    }
    users.value = data25.users;
    userData.value = data25.data;
    
    // 从收集的日期中找出最新的日期
    if (allDates.size > 0) {
      const sortedDates = Array.from(allDates).sort((a, b) => new Date(b).getTime() - new Date(a).getTime());
      lastUpdate.value = sortedDates[0]; // 最新的日期
    }
    
    await nextTick();
  } catch (error) {
    console.error('加载数据失败:', error);
  }
};

const refreshData = () => {
  loadData();
};



// 生命周期
onMounted(() => {
  loadData();
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