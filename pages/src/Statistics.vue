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


const loadData = async () => {
  try {
    // 直接使用导入的数据
    // 筛选2025级数据
    const data: AppData = allData as AppData;
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

const refreshData = () => {
  loadData();
};



// 生命周期
onMounted(() => {
  loadData();
});
</script>

<style scoped>
@import './styles/app.css';
@import './styles/Statistics.css';
</style>