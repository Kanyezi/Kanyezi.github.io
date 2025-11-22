<template>
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
</template>

<script setup lang="ts">
// 定义组件属性
interface Props {
  activeUsersCount: number;
  totalCount: number;
  averageCount: number;
  maxCount: number;
}

withDefaults(defineProps<Props>(), {
  activeUsersCount: 0,
  totalCount: 0,
  averageCount: 0,
  maxCount: 0
});
</script>

<style scoped>
/* Import base framework styles */
@import '../styles/base-framework.css';

/* Import stats cards styles */
@import '../styles/stats-cards.css';
</style>