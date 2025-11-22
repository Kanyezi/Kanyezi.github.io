<template>
  <div class="controls">
    <div class="filter-group">
      <select class="filter-select" :value="periodFilter" @change="onPeriodFilterChange">
        <option value="all">全部周期</option>
        <option value="last4">最近4期</option>
        <option value="last8">最近8期</option>
      </select>
      
      <select class="filter-select" :value="userFilter" @change="onUserFilterChange">
        <option value="all">全部用户</option>
        <option value="selected">仅选中用户</option>
      </select>
      
      <select class="filter-select" :value="platformFilter" @change="onPlatformFilterChange">
        <option value="all">全部平台</option>
        <option value="atcoder">AtCoder</option>
        <option value="codeforces">Codeforces</option>
        <option value="matiji">Matiji</option>
      </select>
      
      
    </div>
    
    <div class="filter-group">
      <button class="btn" @click="refreshData">刷新数据</button>
    </div>
  </div>
</template>

<script setup lang="ts">
// 定义组件属性
interface Props {
  periodFilter: string;
  userFilter: string;
  platformFilter: string;
}

const props = withDefaults(defineProps<Props>(), {
  periodFilter: 'all',
  userFilter: 'all',
  platformFilter: 'all'
});

// 定义事件
interface Emits {
  (e: 'update:periodFilter', value: string): void;
  (e: 'update:userFilter', value: string): void;
  (e: 'update:platformFilter', value: string): void;
  
  (e: 'refresh-data'): void;
}

const emit = defineEmits<Emits>();

// 方法
const onPeriodFilterChange = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  emit('update:periodFilter', target.value);
};

const onUserFilterChange = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  emit('update:userFilter', target.value);
};

const onPlatformFilterChange = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  emit('update:platformFilter', target.value);
};



const refreshData = () => {
  emit('refresh-data');
};
</script>

<style scoped>
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
</style>