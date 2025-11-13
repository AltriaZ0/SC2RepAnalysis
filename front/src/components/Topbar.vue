<script setup lang="ts">
  import { Window } from '@tauri-apps/api/window';
  const appWindow = new Window('main');
  const minimize = () => appWindow.minimize();
  const maximize = () => appWindow.toggleMaximize();
  const closeWindow = () => appWindow.close();
</script>

<template>
    <div data-tauri-drag-region class="titlebar">
        <div class="titlebar-button" id="titlebar-minimize" @click="minimize">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14" /></svg>
        </div>
        <div class="titlebar-button" id="titlebar-maximize" @click="maximize">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M4 4h16v16H4z" />
                    <path d="M8 8h8v8H8z" /></svg>
        </div>
        <div class="titlebar-button" id="titlebar-close" @click="closeWindow">
                <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 6L6 18" />
                <path d="M6 6l12 12" />
              </svg>
        </div>

    </div>  
</template>

<style>

  .icon {
    width: 16px;
    height: 16px;
  }

  .titlebar {
    height: 30px;
    background: #121517;
    user-select: none;
    display: flex;
    justify-content: flex-end;
      border-bottom: 1px solid #2d2d2d;
  }
  .titlebar-button {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    width: 30px;
    height: 30px;
    user-select: none;
    -webkit-user-select: none;
    transition: all 0.2s ease;
  }
  
  .titlebar-button:hover {
    background: #333333;
  }
</style>
