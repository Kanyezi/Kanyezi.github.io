<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <h2>用户列表</h2>
      <input 
        type="text" 
        class="user-search" 
        placeholder="搜索用户..." 
        :value="searchTerm"
        @input="$emit('update:searchTerm', ($event.target as HTMLInputElement).value)"
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
</template>

<script setup lang="ts">
import { computed } from 'vue';

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

// 定义组件属性
interface Props {
  users: User[];
  selectedUsers: string[];
  searchTerm: string;
}

const props = withDefaults(defineProps<Props>(), {
  users: () => [],
  selectedUsers: () => [],
  searchTerm: ''
});

// 定义事件
interface Emits {
  (e: 'toggle-user', userName: string): void;
  (e: 'update:searchTerm', searchTerm: string): void;
}

const emit = defineEmits<Emits>();

// 计算属性
const filteredUsers = computed(() => {
  if (!props.searchTerm) return props.users;
  return props.users.filter(user => 
    user.name.toLowerCase().includes(props.searchTerm.toLowerCase())
  );
});

// 方法
const toggleUser = (userName: string) => {
  emit('toggle-user', userName);
};
</script>

<style scoped>
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
</style>