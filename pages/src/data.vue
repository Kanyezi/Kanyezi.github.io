<template>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue';

// 定义数据类型
interface DataDict {
  [filename: string]: any;
}

// 定义文件列表类型
interface FileList {
  atcoder: string[];
  codeforces: string[];
  matiji: string[];
}

// 响应式数据
const atcoderData = ref<DataDict | null>(null);
const codeforcesData = ref<DataDict | null>(null);
const matijiData = ref<DataDict | null>(null);
const loading = ref<boolean>(false);
const error = ref<string | null>(null);

// 从file_list.json获取文件列表
async function getFileList(): Promise<FileList | null> {
  try {
    const response = await fetch('/file_list.json');
    if (!response.ok) {
      throw new Error('无法加载文件列表');
    }
    return await response.json();
  } catch (err) {
    console.error('获取文件列表失败:', err);
    return null;
  }
}

// 加载指定目录下的所有文件数据
async function loadDirectoryData(directory: string, filenames: string[]): Promise<DataDict> {
  const dataDict: DataDict = {};
  
  // 并行请求所有文件
  const promises = filenames.map(async (filename) => {
    try {
      const response = await fetch(`/${directory}/${filename}`);
      if (!response.ok) {
        console.warn(`无法加载文件: ${directory}/${filename}`);
        return;
      }
      const data = await response.json();
      dataDict[filename] = data;
    } catch (err) {
      console.warn(`加载文件失败: ${directory}/${filename}`, err);
    }
  });
  
  // 等待所有请求完成
  await Promise.all(promises);
  
  return dataDict;
}

// 加载所有数据
async function loadAllData() {
  loading.value = true;
  error.value = null;
  
  try {
    // 获取文件列表
    const fileList = await getFileList();
    
    if (!fileList) {
      // 如果无法获取文件列表，使用硬编码的默认文件列表作为后备
      console.log('使用默认文件列表');
      atcoderData.value = await loadDirectoryData('atcoder', ['2025-10-14.json', '2025-10-19_atcoder.json']);
      codeforcesData.value = await loadDirectoryData('codeforces', ['2025-10-19_atcoder.json']);
      matijiData.value = await loadDirectoryData('matiji', ['2025-10-19_matiji.json']);
    } else {
      // 使用从file_list.json获取的文件列表
      console.log('使用file_list.json中的文件列表');
      atcoderData.value = await loadDirectoryData('atcoder', fileList.atcoder || []);
      codeforcesData.value = await loadDirectoryData('codeforces', fileList.codeforces || []);
      matijiData.value = await loadDirectoryData('matiji', fileList.matiji || []);
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : '加载数据失败';
    console.error('加载数据失败:', err);
  } finally {
    loading.value = false;
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadAllData();
});

// 导出数据供其他组件使用
defineExpose({
  atcoderData,
  codeforcesData,
  matijiData,
  loadAllData
});
</script>

<style scoped>
pre {
  background-color: #f5f5f5;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  font-family: monospace;
}
</style>
