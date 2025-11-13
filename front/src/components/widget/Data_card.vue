<template>
    <!-- 卡片样式 -->
    <div class="card">
        <div class="card-content">
            <h3 class="card-title"> {{title}}-{{ mapName }}-{{race}}-{{date}}-{{ result }}</h3>
            <p class="card-desc">Pimba!</p>
            <div class="card-actions">
            <button class="btn-primary" id="result">分析结果(.xlsx)</button>
            <button class="btn-primary">打开录像(.sc2replay)</button>
            <button class="btn-primary" id="rename">重命名</button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">  
const props = defineProps<{
  title: string
  mapName: string
  race: string
  date: string
  result: string
  xlsxPath: string
}>()

</script>

<style>
#result {
  background-color: #10b981;
}
#rename {
  background-color: #ffffff;
  color: black;
}


.card {
  background: rgba(192, 114, 114, 0.05);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.1s ease;
  margin: 10px;

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
   /* transform: translateY(-4px); */
  box-shadow: 0 0 10px 2px rgba(233, 233, 233, 0.2);
  background-color: rgba(58, 56, 56, 0.61);
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