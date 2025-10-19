import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: './', // 使用相对路径
  define: {
    'process.env.NODE_ENV': JSON.stringify('production')
  },
  build: {
    target: 'es2015',
    minify: false,
    lib: {
      formats: ['iife'],
      entry: './src/main.ts',
      name: 'App'
    },
    rollupOptions: {
      // 确保正确打包所有依赖
      external: [],
      output: {
        format: 'iife',
        globals: {},
        entryFileNames: 'index.js',
        inlineDynamicImports: true,
        // 重要：确保输出的是浏览器可直接运行的代码
        preserveModules: false
      }
    }
  },
  // 确保没有模块相关配置
  resolve: {
    alias: {},
    preserveSymlinks: false
  }
})
