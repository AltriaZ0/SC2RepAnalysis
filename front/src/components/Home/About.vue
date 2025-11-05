<!-- src/components/About.vue -->
<template>
  <div class="content">
    <div v-html="marked(aboutMd)"></div>
  </div>
</template>

<script setup>
import { marked } from 'marked'
const aboutMd = `
  SC2RepAnalysis是一款免费的能够应用于星际争霸2战术学习、游戏后复盘、数据统计等方面的小程序。

  本程序由Python编写，并基于python的sc2reader库的各个端口对星际争霸2replay文件进行解析，将replay中发生的科技升级、建筑建造、单位建造等事件进行统计并汇总成为表格，使之容易进行学习分析。
  
  联系作者：知乎ID：赞君，bilibili：小赞小赞，sc2韩服id：AIlian#11514。

  如果您有发现bug，或者有任何意见与建议，欢迎在各平台私信告诉我，非常感谢！

  在此宣传一下sc2萌新交流练习Q群924040644，欢迎萌新和大佬加入~

  Github：本项目现已开源，Github仓库地址 https://github.com/AltriaZ0/SC2RepAnalysis"
`
</script>

<style scoped>
.content {
  background-color: #1a1a1a;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  color: #e0e0e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}
</style>