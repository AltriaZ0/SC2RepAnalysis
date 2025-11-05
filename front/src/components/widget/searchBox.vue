<template>
    <!-- 顶部搜索栏 -->
      <header class="topbar">
        <div class="search-box">
          <input type="text" placeholder="搜索..." class="search-input" />
          <button class="search-icon">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      </header>
</template>

<style>

/* 顶部搜索栏 */
.topbar {
  background-color: #1a1a1a;
  border-bottom: 1px solid #2d2d2d;
  padding: 16px 24px;
  display: flex;
  justify-content: center;
}

.search-box {
  position: relative;
  width: 400px;
}

.search-input {
  width: 100%;
  padding: 10px 40px 10px 16px;
  border: 1px solid #374151;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.05);
  color: white;
  font-size: 14px;
  outline: none;
}

.search-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.search-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
}
.icon {
  width: 20px;
  height: 20px;
}

</style>