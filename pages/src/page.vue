<template>
    <div class="page">
        <!-- 学生信息表格 -->
        <div class="tab">
            <div class="titles">
                <div class="page-title" @click="toggle(gt)" v-for="gt in grade" :key=gt.tab>{{ gt.tab }}级</div>
            </div>
            <div class="tables">
                <table class="table" v-show="gt.show" v-for="gt in grade" :key=gt.tab>
                    <thead>
                        <tr>
                            <th>姓名</th>
                            <th>班级</th>
                            <th>Codeforces ID</th>
                            <th>AtCoder ID</th>
                            <th>码题集 ID</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="i in data.filter(i => i.grade === gt.tab)" :key=i.name>
                        <td>{{ i.name }}</td>
                        <td>{{ i.class }}</td>
                        <td>{{ i.codeforces_id }}</td>
                        <td>{{ i.atcoder_id }}</td>
                        <td>{{ i.matiji_id }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <!-- 导入data组件但不显示其UI -->
        <data-component ref="dataComponent" />
    </div>
</template>
<script setup lang="ts">
    import { ref, onMounted } from 'vue';
    import DataComponent from './data.vue';

    // 组件引用
    const dataComponent = ref<any>(null);
    
    // 响应式数据用于展示
    const atcoderData = ref<any>(null);
    const codeforcesData = ref<any>(null);
    const matijiData = ref<any>(null);
    const loading = ref<boolean>(true);
    // const error = ref<string | null>(null); // 暂时注释，需要时取消注释

    // 学生数据
    const data = ref<any[]>([]);
    
    // 加载学生数据
    async function loadStudentData() {
        try {
            const response = await fetch('/data.json');
            if (!response.ok) {
                throw new Error('无法加载学生数据');
            }
            data.value = await response.json();
        } catch (err) {
            console.error('加载学生数据失败:', err);
            // 使用默认数据作为后备
            data.value = [];
        }
    }
    
    // 班级选项卡数据
    const grade = ref([
        {
            tab: 2023,
            show: true
        },
        {
            tab: 2024,
            show: false
        },
        {
            tab: 2025,
            show: false
        }
    ]);
    
    // 切换选项卡
    function toggle(gt: any) {
        for (let i of grade.value) {
            i.show = false;
        }
        gt.show = true;
    }
    
    // 获取数据组件中的数据
    function fetchDataFromComponent() {
        if (dataComponent.value.atcoderData && dataComponent.value.codeforcesData && dataComponent.value.matijiData ) {
            // 从组件实例中获取数据
            
            atcoderData.value = dataComponent.value.atcoderData;
            codeforcesData.value = dataComponent.value.codeforcesData;
            matijiData.value = dataComponent.value.matijiData;
            loading.value = false;
            
            console.log('AtCoder数据:', atcoderData.value);
            console.log('Codeforces数据:', codeforcesData.value);
            console.log('matiji数据:', matijiData.value);
        }else{
            console.log('数据组件尚未准备好，稍后重试');
            setTimeout(() => {
                fetchDataFromComponent();
            }, 100);
        }
    }
    
    // 组件挂载后获取数据
    onMounted(async () => {
        // 加载学生数据
        await loadStudentData();
        
        // 等待dataComponent完成初始化和数据加载
        setTimeout(() => {
            fetchDataFromComponent();
        }, 100);
    });
</script>
<style scoped>
/* 现有样式保持不变 */
.page {
    padding: 20px;
    font-family: Arial, sans-serif;
}

.tab {
    margin-bottom: 30px;
    cursor: pointer;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    transition: background-color 0.3s;
}

.tab:hover {
    background-color: #f5f5f5;
}

.page-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 15px;
    color: #333;
    display: inline-block;
    padding: 10px;
    margin-right: 10px;
    border: 1px solid #ddd;
}

.table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
}

.table th,
.table td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
}

.table th {
    background-color: #f8f9fa;
    font-weight: bold;
}

.table tr:nth-child(even) {
    background-color: #f8f9fa;
}

.table tr:hover {
    background-color: #e9ecef;
}

/* 新增数据展示样式 */
.data-display {
    margin-top: 40px;
}

.data-section {
    margin-bottom: 30px;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
}

.data-item {
    margin-bottom: 20px;
    padding: 15px;
    background-color: #fff;
    border-radius: 6px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.data-item h4 {
    margin-top: 0;
    color: #333;
    border-bottom: 1px solid #eee;
    padding-bottom: 8px;
}

.data-item pre {
    margin: 10px 0 0 0;
    padding: 10px;
    background-color: #f5f5f5;
    border-radius: 4px;
    overflow-x: auto;
    font-family: monospace;
}
</style>

<style scoped>
.page {
    padding: 20px;
    font-family: Arial, sans-serif;
}

.tab {
    margin-bottom: 30px;
    cursor: pointer;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    transition: background-color 0.3s;
}

.tab:hover {
    background-color: #f5f5f5;
}

.page-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 15px;
    color: #333;
    display: inline-block;
    /* background-color: aqua; */
    padding: 10px;
    margin-right: 10px;
    border: 1px solid #ddd;
}

.table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
}

.table th,
.table td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
}

.table th {
    background-color: #f8f9fa;
    font-weight: bold;
}

.table tr:nth-child(even) {
    background-color: #f8f9fa;
}

.table tr:hover {
    background-color: #e9ecef;
}
</style>