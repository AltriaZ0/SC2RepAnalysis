<template>
  <div class="dashboard">
    <!-- 主内容区 -->
    <div class="main-container">
      <Topbar class="Topbar" />
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

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.content-body {
  flex: 1;
  padding: 0px 0px;
  overflow-y: hidden;
}

</style>