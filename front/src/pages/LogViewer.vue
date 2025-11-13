<script setup lang="ts">
  import { invoke } from '@tauri-apps/api/core'
  import { Window } from '@tauri-apps/api/window';
  import { listen, UnlistenFn } from '@tauri-apps/api/event'

  const appWindow = new Window('main');
  import { ref, onMounted, onBeforeUnmount } from 'vue'

  const lines = ref<string[]>([])
  let unOut: UnlistenFn | null = null
  let unErr: UnlistenFn | null = null

  function push(line: string, tag: 'OUT'|'ERR') {
    const ts = new Date().toLocaleTimeString()
    lines.value.push(`[${ts}] ${tag} ${line}`)
    requestAnimationFrame(() => {
      const box = document.getElementById('log-box')
      if (box) box.scrollTop = box.scrollHeight
    })
  }

  async function startPy() { await invoke('start_python', { logLevel: 'DEBUG' }) }
  async function stopPy() { await invoke('stop_python') }


  onMounted(async () => {
    unOut = await listen<string>('py:stdout', e => push(e.payload, 'OUT'))
    unErr = await listen<string>('py:stderr', e => push(e.payload, 'ERR'))
  })
  onBeforeUnmount(() => { unOut?.(); unErr?.() })

import Sidebar from '../components/Sidebar.vue';

import { RouterView, useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <!-- 根容器 -->
  <div class="mainBody">
      <div class="mainPage">
        <Sidebar class="Sidebar"  v-if="!route.meta.noLayout" />
        <div class="DashBoard">
          <router-view />
        </div>
      </div>
  </div>  
</template>

<style>
:root {
  --bg: #0f1113;
  --panel: #1a1d21;
  --panel-2: #171a1e;
  --muted: #a6adbb;
  --border: #2a2f36;
  --primary: #3b82f6; /* 蓝 */
  --success: #22c55e; /* 绿 */
  --text: #e5e7eb;
  --warn: #f59e0b;
  --bg:#0f1113;
  --panel:#1a1d21;
  --panel-2:#171a1e;
}

  .mainBody{
    width: 100%;
    height: 100%;
  }
  .mainPage{
    display: flex;
    width: 100%;
  }
  .DashBoard{
    flex: 1; /* 占据剩余空间 */
  }


  /* 全局滚动条样式 */
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #2b2a2a;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #9e9e9e;
}

/* 下拉菜单相关样式 */
.dropdown {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background-color: #1a1a1a;
  border: 1px solid #2d2d2d;
  border-radius: 4px;
  min-width: 120px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  opacity: 0;
  visibility: hidden;
  transition: all 0.2s ease;
  z-index: 100;
}

.dropdown-toggle::after {
  content: "▼";
  font-size: 12px;
  margin-left: 2px;
}

.dropdown:hover .dropdown-menu {
  opacity: 1;
  visibility: visible;
}

.dropdown-item {
  display: block;
  padding: 8px 12px;
  color: #d1d5db;
  text-decoration: none;
  border-bottom: 1px solid #2d2d2d;
}

.dropdown-item:last-child {
  border-bottom: none;
}

.dropdown-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
  color: white;
}

.toolbar { 
  position: fixed;
  width: 100%;
  height: var(--nav-height);
  display: flex;
  gap: 16px;
  background-color: #0f1012;
  padding: 8px 12px;
  user-select: none;
  border-bottom: 1px solid #2d2d2d;
  z-index: 10;
}

</style>
