<template>
    <!-- 卡片样式 -->
    <div class="card-grid">
        <div class="card">
            <div class="card-image">
                <img src="" alt="卡片图片" />
            </div>
            <div class="card-content">
                <h3 class="card-title">示例卡片</h3>
                <p class="card-desc">示例描述</p>
                <div class="card-actions">
                <button class="btn-primary">示例描述</button>
                <span class="card-count">示例描述</span>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-image">
                <img src="" alt="卡片图片" />
            </div>
            <div class="card-content">
                <h3 class="card-title">示例卡片</h3>
                <p class="card-desc">示例描述</p>
                <div class="card-actions">
                <button class="btn-primary">示例描述</button>
                <span class="card-count">示例描述</span>
                </div>
            </div>
        </div>
    </div>
</template>

<style>

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-primary:hover {
  background-color: #2563eb;
}


.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.card-image {
  height: 180px;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-content {
  padding: 16px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px;
  color: white;
}

.card-desc {
  font-size: 14px;
  color: #b3b3b3;
  margin: 0 0 12px;
}

.card-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}
.card-count {
  font-size: 12px;
  color: #9ca3af;
}
</style>