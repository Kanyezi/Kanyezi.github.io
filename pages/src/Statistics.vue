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
        :data-filter="currentDataFilter"
        @update:period-filter="updatePeriodFilter"
        @update:user-filter="updateUserFilter"
        @update:platform-filter="updatePlatformFilter"
        @update:data-filter="updateDataFilter"
        
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
        :data-filter="currentDataFilter"
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
import { ref, computed, onMounted, nextTick } from 'vue';
import UserListSidebar from './components/UserListSidebar.vue';
import StatsCards from './components/StatsCards.vue';
import TrendChart from './components/TrendChart.vue';
import FilterControls from './components/FilterControls.vue';
import allData from './all_data.json';
console.log(allData)

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
  lastUpdate?: string;
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
const currentDataFilter = ref<string>('ac');
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
    return displayUsers.value.reduce((sum, user) => {
      const userHistory = userData.value[user.name];
      if (!userHistory) return sum;
      
      // 获取最新的日期
      const latestDate = getLatestDateFromUserHistory(userHistory);
      if (!latestDate) return sum;
      
      let userTotal = 0;
      // 计算该用户在各个平台的总题数
      if (userHistory.atcoder[latestDate]?.ac_count !== undefined) {
        userTotal += userHistory.atcoder[latestDate].ac_count;
      } else if (typeof userHistory.atcoder[latestDate] === 'number') {
        userTotal += userHistory.atcoder[latestDate];
      }
      
      if (userHistory.codeforces[latestDate]?.ac_count !== undefined) {
        userTotal += userHistory.codeforces[latestDate].ac_count;
      } else if (typeof userHistory.codeforces[latestDate] === 'number') {
        userTotal += userHistory.codeforces[latestDate];
      }
      
      if (userHistory.matiji[latestDate]?.ac_count !== undefined) {
        userTotal += userHistory.matiji[latestDate].ac_count;
      } else if (typeof userHistory.matiji[latestDate] === 'number') {
        userTotal += userHistory.matiji[latestDate];
      }
      
      return sum + userTotal;
    }, 0);
  } else {
    // 单个平台
    return displayUsers.value.reduce((sum, user) => {
      const userHistory = userData.value[user.name];
      if (!userHistory) return sum;
      
      // 获取最新的日期
      const latestDate = getLatestDateFromUserHistory(userHistory);
      if (!latestDate) return sum;
      
      const platformData = userHistory[platform as keyof StudentData];
      if (platformData && platformData[latestDate]) {
        // 新数据格式：{ ac_count: number }
        if (typeof platformData[latestDate] === 'object' && platformData[latestDate].ac_count !== undefined) {
          return sum + platformData[latestDate].ac_count;
        } else {
          // 旧数据格式：直接是数值
          return sum + platformData[latestDate];
        }
      }
      return sum;
    }, 0);
  }
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
    const userSums = displayUsers.value.map(user => {
      const userHistory = userData.value[user.name];
      if (!userHistory) return 0;
      
      // 获取最新的日期
      const latestDate = getLatestDateFromUserHistory(userHistory);
      if (!latestDate) return 0;
      
      let userTotal = 0;
      // 计算该用户在各个平台的总题数
      if (userHistory.atcoder[latestDate]?.ac_count !== undefined) {
        userTotal += userHistory.atcoder[latestDate].ac_count;
      } else if (typeof userHistory.atcoder[latestDate] === 'number') {
        userTotal += userHistory.atcoder[latestDate];
      }
      
      if (userHistory.codeforces[latestDate]?.ac_count !== undefined) {
        userTotal += userHistory.codeforces[latestDate].ac_count;
      } else if (typeof userHistory.codeforces[latestDate] === 'number') {
        userTotal += userHistory.codeforces[latestDate];
      }
      
      if (userHistory.matiji[latestDate]?.ac_count !== undefined) {
        userTotal += userHistory.matiji[latestDate].ac_count;
      } else if (typeof userHistory.matiji[latestDate] === 'number') {
        userTotal += userHistory.matiji[latestDate];
      }
      
      return userTotal;
    });
    return Math.max(...userSums);
  } else {
    // 单个平台
    const platformValues = displayUsers.value.map(user => {
      const userHistory = userData.value[user.name];
      if (!userHistory) return 0;
      
      // 获取最新的日期
      const latestDate = getLatestDateFromUserHistory(userHistory);
      if (!latestDate) return 0;
      
      const platformData = userHistory[currentPlatformFilter.value as keyof StudentData];
      if (platformData && platformData[latestDate]) {
        // 新数据格式：{ ac_count: number }
        if (typeof platformData[latestDate] === 'object' && platformData[latestDate].ac_count !== undefined) {
          return platformData[latestDate].ac_count;
        } else {
          // 旧数据格式：直接是数值
          return platformData[latestDate];
        }
      }
      return 0;
    });
    return Math.max(...platformValues);
  }
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

const updateDataFilter = (value: string) => {
  currentDataFilter.value = value;
};


const loadData = async () => {
  try {
    // 直接使用导入的数据
    // 筛选2025级数据
    const data: AppData = allData as AppData;
    const data25:AppData = {users:[],data:{}};
    // 收集所有日期以确定最后更新日期
    const allDates = new Set<string>();
    
    for(let i=0;i<data.users.length;i++){
      const u = {...data.users[i]};   // 创建副本以修改数据
      if (!u || u.grade !== 2025) continue;

      // 根据新数据格式，从嵌套对象中提取最新数值
      const userHistory = data.data[u.name];
      if (userHistory) {
        // 获取最新的日期
        const latestDate = getLatestDateFromUserHistory(userHistory);
        if (latestDate) {
          u.atcoder = userHistory.atcoder[latestDate]?.ac_count || 0;
          u.codeforces = userHistory.codeforces[latestDate]?.ac_count || 0;
          u.matiji = userHistory.matiji[latestDate]?.ac_count || 0;
        } else {
          u.atcoder = 0;
          u.codeforces = 0;
          u.matiji = 0;
        }
      }

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
    console.log(data25.users)
    userData.value = data25.data;
    
    // 从收集的日期中找出最新的日期
    if (allDates.size > 0) {
      const sortedDates = Array.from(allDates).sort((a, b) => new Date(b).getTime() - new Date(a).getTime());
      const latestDate = sortedDates[0];
      if (latestDate) {
        lastUpdate.value = latestDate; // 最新的日期
      }
    }
    
    // 使用JSON数据中的lastUpdate字段
    if (data.lastUpdate) {
      const lastUpdateData = data.lastUpdate;
      const datePart = lastUpdateData.split('T')[0];
      lastUpdate.value = datePart || ''; // 确保提供一个默认值
    }
    
    await nextTick();
  } catch (error) {
    console.error('加载数据失败:', error);
  }
};

// 辅助函数：从用户历史数据中获取最新日期
const getLatestDateFromUserHistory = (userHistory: StudentData): string | null => {
  const allDates = new Set<string>();
  
  // 收集所有平台的日期
  Object.values(userHistory).forEach(platformData => {
    Object.keys(platformData).forEach(date => allDates.add(date));
  });
  
  if (allDates.size === 0) return null;
  
  // 排序并返回最新的日期
  const sortedDates = Array.from(allDates).sort((a, b) => new Date(b).getTime() - new Date(a).getTime());
  return sortedDates[0];
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
@import './styles/root.css';
@import './styles/Statistics.css';
</style>