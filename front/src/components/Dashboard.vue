<template>
  <div class="dashboard">

    <!-- 主内容区 -->
    <div class="main-container">
      <Topbar class="Topbar" />

      <div class="top-nav">
        <router-link to="/Home/guide" class="nav-item">使用方法</router-link>
        <router-link to="/Home/UpdateHistory" class="nav-item">更新历史</router-link>
        <router-link to="/Home/About" class="nav-item">关于</router-link>
        <!-- <div class="dropdown">
          <span class="nav-item dropdown-toggle">分类导航</span>
          <div class="dropdown-menu">
            <a href="#" class="dropdown-item">游戏</a>
            <a href="#" class="dropdown-item">工具</a>
            <a href="#" class="dropdown-item">社区</a>
          </div>
        </div> -->
      </div>

      <!-- 内容主体 -->
      <main class="content-body">
         <router-view></router-view>
      </main>
      
    </div>
  </div>
</template>

<script setup>
import Topbar from './Topbar.vue';
</script>

<style scoped>
.dashboard {
  display: flex;
  height: 100vh;
  background-color: #121517;
  color: #e5e7eb;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}


.Topbar{
  width: 100%;
}

.top-nav {
  display: flex;
  gap: 16px;
  background-color: #0f1012;
  padding: 8px 24px;
  /* border-bottom: 1px solid #2d2d2d */
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}


/* 内容主体 */
.content-body {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}


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
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
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
  background-color: rgba(255,255,255,0.05);
  color: white;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 5px 12px;
  gap: 12px;
  color: #d1d5db;
  text-decoration: none;
  transition: all 0.2s ease;
  border-radius: 4px;
  border: 1px solid #2d2d2d;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
  color: #ffffff;
}

.nav-item.active {
  background-color: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
}
</style>