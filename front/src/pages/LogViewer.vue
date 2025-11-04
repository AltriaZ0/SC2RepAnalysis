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

  const minimize = () => appWindow.minimize();
  const maximize = () => appWindow.toggleMaximize();
  const closeWindow = () => appWindow.close();

  onMounted(async () => {
    unOut = await listen<string>('py:stdout', e => push(e.payload, 'OUT'))
    unErr = await listen<string>('py:stderr', e => push(e.payload, 'ERR'))
  })
  onBeforeUnmount(() => { unOut?.(); unErr?.() })

</script>

<template>
  <!-- 根容器：撑满屏幕，垂直布局 -->
   
  <div class=" h-screen flex flex-col " id="mainBody">

  <div data-tauri-drag-region class="titlebar">
    <div class="titlebar-button" id="titlebar-minimize" @click="minimize">
      <img
        src="https://api.iconify.design/mdi:window-minimize.svg"
        alt="minimize"
      />
    </div>
    <div class="titlebar-button" id="titlebar-maximize" @click="maximize">
      <img
        src="https://api.iconify.design/mdi:window-maximize.svg"
        alt="maximize"
      />
    </div>
    <div class="titlebar-button" id="titlebar-close" @click="closeWindow">
      <img src="https://api.iconify.design/mdi:close.svg" alt="close" />
    </div>
  </div>


    <!-- 主内容：两个大按钮居中 -->
    <div>
      <button @click="startPy" id ="start-button">
        启动分析
      </button>
      <button id ="stop-button" @click="stopPy">
        停止分析
      </button>
    </div>
  </div>
</template>

<style>
  .titlebar {
    height: 30px;
    background: #329ea3;
    user-select: none;
    display: flex;
    justify-content: flex-end;
  }
  .titlebar-button {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    width: 30px;
    height: 30px;
    user-select: none;
    -webkit-user-select: none;
  }
  .titlebar-button:hover {
    background: #5bbec3;
  }
  #mainBody{
    background: rgb(93, 100, 105);
    width: 100%;
    height: 100%;
  }
/* 按钮通用样式 */
  #start-button, #stop-button {
    width: 192px; /* w-48 = 12rem = 192px */
    height: 64px; /* h-16 = 4rem = 64px */
    border-radius: 0.5rem; /* rounded-3xl */
    color: rgb(0, 0, 0);
    background: rgb(75, 101, 87);
    font-size: 1.5rem; /* text-2xl */
    font-weight: bold;
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05); /* shadow-xl */
    border: none;
    outline: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
  }
    #start-button:hover, #stop-button:hover{
    background: rgb(57, 75, 63);
  }
</style>
