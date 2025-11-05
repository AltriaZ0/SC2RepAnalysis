<!-- MessageBox.vue -->
<template>
  <div class="message-box">
    <!-- 标题 -->
    <h3 class="box_title">{{title}}</h3>

    <!-- 正文内容（支持展开/收起） -->
    <div class="box_content" :class="{ collapsed: isCollapsed }">
      {{content}}
    </div>

    <!-- 展开/收起按钮 -->
    <button class="toggle-btn" @click="isCollapsed = !isCollapsed">
      {{ isCollapsed ? '展开' : '收起' }}
    </button>

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 是否折叠正文
const isCollapsed = ref(false)


const props = defineProps({
  title: {
    type: String,
    required: false,
    default: '示例标题'
  },
  content: {
    type: String,
    required: false,
    default: '示例正文'
  }
})

</script>

<style scoped>
.message-box {
  background-color: #1a1a1a;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  color: #e0e0e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}


.box_title {
  font-size: 16px;
  font-weight: bold;
  margin: 8px 0;
  color: #fff;
}

.box_content {
  color: #ccc;
  line-height: 1.5;
  white-space: pre-wrap;
  word-wrap: break-word;
  max-height: 500px;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.box_content.collapsed {
  max-height: 90px;
}

.toggle-btn {
  background: none;
  border: none;
  color: #999;
  font-size: 12px;
  cursor: pointer;
  padding: 4px 0;
  margin-top: 8px;
}

</style>

