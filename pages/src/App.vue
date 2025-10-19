<template>
    <div class="app">
        <div class="page">
            <Statistics />
        </div>
    </div>
</template>
<script setup lang="ts">
    import Statistics from './Statistics.vue';
</script>
<style>
.app {
    width: 100%;
    height: 100vh;
    overflow: hidden;
}
.page {
    width: 100%;
    height: 100%;
}
</style>