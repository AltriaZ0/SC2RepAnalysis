# SC2RepAnalysis
A Analysis Tool for starcraft2 replay ,  based of sc2reader.

Communicate with me: *zanjune@163.com*

## Download
下载 SC2RepAnalysis 1.3.3: https://pan.baidu.com/s/1V-115EhV-T00InQX3ucX1w?pwd=alan 

提取码(Password)：alan 


(环境已经整合，无需配置)

(The environment is already integrated, no configuration needed.)

## 使用文档
https://zhuanlan.zhihu.com/p/668752079

## 更新历史
#### 1.0.1更新内容：
引入了pandas库

支持导出为excel格式

修复了重新归类变异时，升级列表的长度不足的问题

#### 1.1更新内容
增加了对泰伦、普陀寺的支持

增加了个别时间点的人口与农民数量

#### 1.1.1更新内容：
增加了关键时间点的存活单位和农民数量

#### 1.1.2更新内容
增加了进度条，支持显示关键时间点的存活单位

txt文件和excel文件会生成在SC2RepAnalysis文件夹中

修复了之前版本的bug

优化了输出txt和excel内容的格式

#### 1.2.0更新内容
修复了之前版本的bug

    1.当没有单位变异发生时报错的bug

    2.Unitposition出现异常情况的bug

    3.变异单位重分类时单位出生的列表可能不够长的bug

目前已经支持批量分析，并支持导出批量rep的流程

由于bug2,修改了sc2reader的一些配置，有可能未来会出现未知的bug

优化了代码架构，使代码可读性增加

优化了GUI，使用更加方便

优化了excel的表现：减去了现在升级科技的*n效果

#### 1.2.1更新内容：
修复了之前版本的bug：

    1.神族能够折跃的单位不会统计单位存活的问题

    2.神族VB科技和VR科技名称互换的问题

    3.虫族存活单位中变异生成的单位统计不正确的问题

#### 1.3.0更新内容
修复了之前版本的bug:

    神族合成白球不会减少单位和记录事件不准确的bug

增加了练习功能demo

增加了悬浮文字小插件demo版本

#### 1.3.1更新内容：
修复了练习功能中时间不准确的问题

#### 1.3.2 更新内容
修复了无法读取韩语ID的Rep的bug

修复了秒退的对局分析报错的bug

修复了开局星空加速产农民的bug(会导致农民时间不准确)

修复了多人游戏、人机游戏无法分析的bug

增加了异常报告，现在遇到分析错误的replay不会中止分析而是会跳过并生成异常报告

优化了练习功能的显示效果

提供了分析选择：是否提供所有时间的信息

#### 1.3.3 更新内容
发布源码至github

提高了代码的耦合性

修复了练习功能中的若干问题