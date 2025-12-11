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
      
      <select class="filter-select" :value="dataFilter" @change="onDataFilterChange">
        <option value="ac">AC题数</option>
        <option value="rating">Rating</option>
        <option value="all-data">全部数据</option>
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
  dataFilter: string;
}

const { periodFilter = 'all', userFilter = 'all', platformFilter = 'all', dataFilter = 'ac' } = defineProps<Props>();

// 定义事件
interface Emits {
  (e: 'update:periodFilter', value: string): void;
  (e: 'update:userFilter', value: string): void;
  (e: 'update:platformFilter', value: string): void;
  (e: 'update:dataFilter', value: string): void;
  
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

const onDataFilterChange = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  emit('update:dataFilter', target.value);
};

const refreshData = () => {
  emit('refresh-data');
};
</script>

<style scoped>
@import '../styles/FilterControls.css';
</style>