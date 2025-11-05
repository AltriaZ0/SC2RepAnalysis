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

import DashBoard from '../components/Dashboard.vue';  
import Sidebar from '../components/Sidebar.vue';
import Topbar from '../components/Topbar.vue';
</script>

<template>
  <!-- 根容器：撑满屏幕，垂直布局 -->
  <div class=" h-screen flex flex-col " id="mainBody">

      <div class="mainPage">
        <Sidebar class="Sidebar"/>
        <DashBoard class="DashBoard"/>
      </div>

  </div>  
</template>

<style>
  #mainBody{
    background: rgb(93, 100, 105);
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
</style>
