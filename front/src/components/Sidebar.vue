<!-- src/components/Sidebar.vue -->
<template data-tauri-drag-region >
  <aside data-tauri-drag-region class="sidebar">
    <!-- Logo -->
    <!-- <div class="logo-container">
      <img src="../assets/logo.ico" alt="Logo" class="logo" />
    </div> -->

    <!-- 导航菜单 -->
    <nav data-tauri-drag-region class="nav">
      <!-- 一级菜单 -->
      <router-link  to="/Home" class="nav-item" active-class="active">
        <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        <span>首页</span>
      </router-link>

      <router-link to="/my-data" class="nav-item" active-class="active">
        <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
        <span>我的数据</span>
      </router-link>

      <!-- 子菜单 -->
      <div data-tauri-drag-region class="nav-group">
        <div data-tauri-drag-region class="nav-group-header">
          <span>Replay分析</span>
        </div>
        
        <router-link to="/single" class="nav-item sub-item"  active-class="active">
          <span>单文件分析</span>
        </router-link>

        <router-link to="/batch" class="nav-item sub-item" active-class="active">
          <span>批量分析</span>
        </router-link>
        <div  data-tauri-drag-region class="nav-group-header">
          <span>其他小工具</span>
        </div>
        <router-link to="/reminder" class="nav-item sub-item" active-class="active">
          <span>屏幕提醒</span>
        </router-link>

        <router-link to="/practice" class="nav-item sub-item" active-class="active">
          <span>流程练习</span>
        </router-link>
      </div>
    </nav>


    <div data-tauri-drag-region class="settings">
      <router-link  id="set" to="/settings"> 设置</router-link>
    </div>
  </aside>
</template>

<script setup lang="ts">
defineProps<{ active?: boolean }>()
</script>

<style scoped>
#set{
  padding: 12px 24px;
  background-color: None;
  background:None;
  color: #9ca3af;
  text-decoration: none;
}


.sidebar{
  --bg-1: #1d1f22;
  --accent-1: #77a9ff;
  --accent-2: #4199d3;
  --glow: rgba(125, 190, 216, 0.459);
}

.icon {
  width: 24px;
  height: 24px;
  fill: currentColor;
}


.sidebar {
  flex: 0 0 175px;
  background-color: #070809;
  position: relative;
  color: #e5e7eb;
  border-right: 1px solid #2d2d2d;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  user-select: none;

}

.logo-container {
  padding: 32px 24px;
  text-align: center;
}

.logo {
  width: 64px;
  height: 64px;
  display: inline-block;
}

.nav {
  padding: 24px 0;
  flex: 1;
}

.nav-item {
  display: flex;
  position: relative;
  align-items: center;
  padding: 12px 24px;
  gap: 12px;
  margin : 3px 5px;
  color: #d1d5db;
  text-decoration: none;
    transition: 
    color .2s ease,
    background-color .2s ease,
    box-shadow .2s ease,
    transform .15s ease;
  border-radius: 4px;
}

.nav-item:hover {
  background-color: rgb(32, 33, 34);
  color: #f0f0f0;
  
}

.nav-item::before{
  content: "";
  position: absolute;
  left: -6px;
  top: 8px;
  bottom: 8px;
  width: 0;
  border-radius: 5px;
  background: linear-gradient(180deg, var(--accent-1), var(--accent-2));
  box-shadow:
    0 0 30px var(--glow),
    0 0 2px rgba(0, 0, 0, 0.678) inset;
  opacity: 0;
  transition: width .20s ease, opacity .20s ease;
}

.nav-item::after{
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  pointer-events: none;
  background:
    radial-gradient(120% 120% at 0% 50%, rgba(170, 224, 255, 0.3) 0%, rgba(245,163,79,0.0) 60%),
    linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
  opacity: 0;
  transition: opacity .20s ease;
}

.nav-item.active::before{
  width: 6px;
  opacity: 1;
}
.nav-item.active::after{
  opacity: 1;
}

.nav-item.active{
  background: color-mix(in oklab, var(--bg-1) 85%, white 15%);
  box-shadow:
    0 0px 3px 0.1px var(--glow);
    /* inset 0 1px 0 rgba(255,255,255,0.08); */
  transform: translateZ(0);
  color: #f0f0f0;
}

.nav-item.active::before{
  width: 6px;
  opacity: 1;
}
.nav-item.active::after{
  opacity: 1;
}

.router-link-active {
  padding: 12px 24px;
  margin: 3px 8px;
  background-color: #202122;
  color: #ffffff;
}
.nav-group {
  margin-top: 16px;
}

.nav-group-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 24px;
  font-size: 14px;
  font-weight: 500;
  color: #9ca3af;
  cursor: default;
}

.sub-item {
  padding-left: 40px;
  padding-right: 24px;
  font-size: 14px;
}

.settings {
  bottom:0px;
  width: 100%;
  position: absolute;
  padding: 12px;
  border-top: 1px solid #2d2d2d;
  text-align: center;
  font-size: 14px;
}



/* 兼容处理 */
/* 支持 backdrop-filter 的浏览器（Chromium/Edge/WebView2/现代 Safari） */
@supports ((backdrop-filter: blur(8px)) or (-webkit-backdrop-filter: blur(8px))){
  .nav-item.active{
    background: rgba(66, 66, 66, 0.336);
    backdrop-filter: blur(8px) saturate(160%);
    -webkit-backdrop-filter: blur(8px) saturate(160%);
  }

}

/* 不支持时的降级方案：用半透明填充 + 更强的阴影模拟 */
@supports not ((backdrop-filter: blur(8px)) or (-webkit-backdrop-filter: blur(8px))){
  .nav-item.active{
    background: rgba(255,255,255,0.06);
    box-shadow:
      0 14px 30px -12px var(--glow),
      inset 0 1px 0 rgba(255,255,255,0.08);
  }
}

</style>