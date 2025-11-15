<!-- MessageBox.vue -->
<template>
  <div class="card">
    <!-- 标题 -->
    <div class="buildBox_title">
      <h3 class="box_title">建造顺序</h3> 
      <div class="title-actions">
        <div class="toggle-btn" @click="copyBO(content)">
          复制建造顺序
        </div>
        <div class="toggle-btn" id="openResult" @click="openExportDir_player(outputPath)">
          打开分析结果
        </div>
      </div>
    </div>
    <!-- 正文内容（支持展开/收起） -->
    <div class="box_content" :class="{ collapsed: isCollapsed }">
        <ul class="bo-list">
            <li v-for="(step, i) in content" :key="i">
            <span class="time">{{ step.t }}</span>
            <span class="what">{{ step.action }}</span>
            </li>
        </ul>
    </div>
    <!-- 展开/收起按钮 -->
    <button class="toggle-btn" @click="isCollapsed = !isCollapsed">
      {{ isCollapsed ? '展开' : '收起' }}
    </button>

  </div>

</template>

<script setup lang="ts">
import { ref } from 'vue'
import { openPath } from '@tauri-apps/plugin-opener';

async function openExportDir_player(dir: string) {
  console.log("result.value.playersInfo.output_dir:",dir)

  try {
    await openPath(dir)
    console.log("✅ 已打开导出目录:", dir)
  } catch (e) {
    console.error("❌ 打开目录失败:", e)
  }
}



// 是否折叠正文
const isCollapsed = ref(true)

interface BoStep {
  t: string
  action: string
}

const props = defineProps({
  title: {
    type: String,
    required: false,
    default: '示例标题'
  },
  race:{
    type: String,
    required: false,
    default: '示例标题'
  },
  result:{
    type: String,
    required: false,
    default: '示例标题'
  },
  content: {
    type: Array<BoStep>,
    required: false,
    default: '示例正文'
  },
  outputPath:{
    type: String,
    required: false,
    default: '示例正文'
  }
})


async function copyBO(steps: BoStep[] | undefined) {
  if (!steps || !steps.length) {
    console.log('没有可复制的建造顺序')
    return
  }

  const text = steps
    .map(s => `${s.t}\t${s.action}`)
    .join('\n')

  try {
    await navigator.clipboard.writeText(text)
    console.log('✅ 建造顺序已复制到剪贴板')
  } catch (err) {
    console.error('❌ 复制建造顺序失败:', err)
  }
}

</script>


<style scoped>
.title-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

#openResult {
  background: var(--success); 
  border-color: transparent;
  color: #0b1b10;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.buildBox_title {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.message-box {
background: var(--panel); border: 1px solid var(--border); border-radius: 16px; padding: 14px; margin-top: 12px; }



.box_title {
  font-size: 16px;
  font-weight: bold;
  margin: 2px 2px;
  color: #fff;
}

.box_content {
  color: #ccc;
  line-height: 1.5;
  white-space: pre-wrap;
  word-wrap: break-word;
  overflow: hidden;
  transition: all 0.3s ease;
}

.box_content.collapsed {
  max-height: 90px;
}

.toggle-btn {
  border: 1px solid var(--border);
  background: none;
  border: none;
  color: #999;
  font-size: 12px;
  cursor: pointer;
  padding: 2px 0;
  margin-top: 2px;
  margin: 5px
}



#openResult:hover {
  background-color: #25d967;
}

.bo-list {
  margin: 0px 0px;
  padding:5px  5px;
  display: grid;
  gap: 3px;
}

.bo-list li {
  display: flex;
  gap: 5px;
}

.bo-list .time {
  color: var(--muted);
  width: 40px;
  flex-shrink: 0;
}

</style>

