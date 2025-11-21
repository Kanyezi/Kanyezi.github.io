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
</style>