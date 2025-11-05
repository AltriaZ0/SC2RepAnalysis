<!-- src/components/Sidebar.vue -->
<template>
  <aside class="sidebar">
    <!-- Logo -->
    <div class="logo-container">
      <img src="../assets/logo.ico" alt="Logo" class="logo" />
    </div>

    <!-- 导航菜单 -->
    <nav class="nav">
      <!-- 一级菜单 -->
      <router-link to="/" class="nav-item active">
        <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        <span>首页</span>
      </router-link>

      <router-link to="/my-data" class="nav-item">
        <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
        <span>我的数据</span>
      </router-link>

      <!-- 数据分析（子菜单） -->
      <div class="nav-group">
        <div class="nav-group-header">
          <span>Replay分析</span>
        </div>
        
        <router-link to="/analyze/single" class="nav-item sub-item">
          <span>单文件分析</span>
        </router-link>

        <router-link to="/analyze/batch" class="nav-item sub-item">
          <span>批量分析</span>
        </router-link>
        <div class="nav-group-header">
          <span>其他小工具</span>
        </div>
        <router-link to="/analyze/reminder" class="nav-item sub-item">
          <span>屏幕提醒</span>
        </router-link>

        <router-link to="/analyze/practice" class="nav-item sub-item">
          <span>流程练习</span>
        </router-link>
      </div>
    </nav>


    <div class="settings">
      设置
    </div>
  </aside>
</template>

<script setup>
</script>

<style scoped>

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
  align-items: center;
  padding: 12px 24px;
  gap: 12px;
  color: #d1d5db;
  text-decoration: none;
  transition: all 0.2s ease;
  border-radius: 4px;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
  color: #ffffff;
}

.nav-item.active {
  background-color: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
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
  padding-left: 40px; /* 缩进 */
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

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #374151;
  color: white;
  line-height: 40px;
  font-size: 14px;
  display: inline-block;
}
</style>