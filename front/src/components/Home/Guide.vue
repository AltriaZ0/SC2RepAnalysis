<!-- src/components/Guide.vue -->
<script setup>
import MessageBox from '../widget/MessageBox.vue';

// 定义消息列表（支持多行字符串、换行等）
const messages = [
  {
    title: '如何进行单个 Replay 文件的分析？',
    content: `将 .replay 文件拖入分析区域即可自动解析。
支持 StarCraft II 4.10+ 版本的回放。
解析完成后可查看单位生产、资源曲线等详细数据。`
  },
  {
    title: '批量分析多个 Replay',
    content: `点击“批量导入”按钮，选择包含多个 .replay 文件的文件夹。
系统将自动并行解析所有文件，并生成汇总报告。`
  },
  {
    title: '常见问题',
    content: `Q: 为什么某些 Replay 无法解析？
A: 可能是版本过低或文件损坏，请确保使用 4.10 以上版本录制。`
  }
]
</script>


<template>

    <MessageBox
      v-for="(msg, index) in messages"
      :key="index"
      :title="msg.title"
      :content="msg.content"
    />
</template>


<style scoped>
.content {
  padding: 24px;
  font-size: 16px;
  line-height: 1.5;
  color: #e0e0e0;
}

</style>