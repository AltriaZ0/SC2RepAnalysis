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
      <div class="dropdown">
        <span class="search-item dropdown-toggle">排序</span>
        <div class="dropdown-menu">
          <a href="#" class="dropdown-item">对局时间</a>
          <a href="#" class="dropdown-item">游戏时长</a>
          <a href="#" class="dropdown-item">种族</a>
        </div>
      </div> 
        <div class="dropdown">
        <span class="search-item dropdown-toggle">玩家名</span>
        <div class="dropdown-menu">
          <a href="#" class="dropdown-item">Player1</a>
          <a href="#" class="dropdown-item">Player2</a>
        </div>
      </div> 
      </header>

</template>

<style>

  .search-item {
    display: flex;
    align-items: center;
    margin:0px 10px;
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

  /* 激活状态（使用 Vue Router 的类名更好） */
  .router-link-active {
    background-color: #8a5252b9;
    color: #ffffff;
  }

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
  width: 50%;
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