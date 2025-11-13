<template>
  <div class="layout-container">
    <div class="top-nav">
      <router-link to="/Home/guide" class="nav-item">使用方法</router-link>
      <router-link to="/Home/UpdateHistory" class="nav-item">更新历史</router-link>
      <router-link to="/Home/About" class="nav-item">关于</router-link>
      
      <div class="dropdown">
        <span class="nav-item dropdown-toggle">筛选</span>
        <div class="dropdown-menu">
          <a href="#" class="dropdown-item">A</a>
          <a href="#" class="dropdown-item">B</a>
          <a href="#" class="dropdown-item">C</a>
        </div>
      </div> 
     
    </div>

    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>

.layout-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  --nav-height: 50px;
}

.top-nav {
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

.content {
  flex: 1;
  height: calc(100vh - var(--nav-height));
  margin-top: var(--nav-height);
  overflow-y: auto;
  overflow-x: hidden;
  padding: 16px 5px;
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
  background-color: #343638b9;
  color: #ffffff;
}

.router-link-active {
  background-color: #8a5252b9;
  color: #ffffff;
}
</style>
