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
import allData from '../public/all_data.json';

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
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

:root {
  --primary-color: #4361ee;
  --primary-light: #4895ef;
  --secondary-color: #6c757d;
  --success-color: #4cc9f0;
  --success-light: #4cc9f0;
  --warning-color: #f72585;
  --danger-color: #e63946;
  --light-bg: #f8f9fa;
  --dark-bg: #212529;
  --border-color: #e0e0e0;
  --card-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  --card-shadow-hover: 0 20px 40px rgba(67, 97, 238, 0.15);
  --border-radius: 16px;
  --sidebar-width: 320px;
  --transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f4f8 0%, #e6eef5 50%, #dae6f2 100%);
  color: #333;
  line-height: 1.6;
  position: relative;
  overflow-x: hidden;
}

.container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at top left, rgba(67, 97, 238, 0.05) 0%, transparent 40%);
  z-index: -1;
}

.container::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(72, 149, 239, 0.08) 0%, transparent 70%);
  border-radius: 50%;
  z-index: -1;
  filter: blur(20px);
}

/* 主内容区样式 */
.main-content {
  flex: 1;
  padding: 25px;
  overflow-y: auto;
}

header {
  background: white;
  padding: 25px;
  border-radius: var(--border-radius);
  box-shadow: var(--card-shadow);
  margin-bottom: 25px;
  background: linear-gradient(120deg, #ffffff 0%, #f8fbff 100%);
  border: 1px solid var(--border-color);
}

h1 {
  font-size: 2rem;
  margin-bottom: 10px;
  color: var(--primary-color);
  font-weight: 700;
}

footer {
  text-align: center;
  margin-top: 40px;
  padding: 25px;
  color: var(--secondary-color);
  font-size: 0.9rem;
  background: white;
  border-radius: var(--border-radius);
  box-shadow: var(--card-shadow);
  margin-left: 25px;
  margin-right: 25px;
}

</style>

<style scoped>
/* Import all styles */
@import './styles/app.css';
</style>