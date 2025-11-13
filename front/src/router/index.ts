import { createRouter, createWebHistory } from 'vue-router'

import Dashboard from '../components/DashBoard.vue'


import Homepage from '../components/Home/Homepage.vue'
import Guide from '../components/Home/Guide.vue'
import UpdateHistory from '../components/Home/UpdateHistory.vue'
import About from '../components/Home/About.vue'

import Mydata from '../components/Mydata/Mydata.vue'
import Single from '../components/Single/SingleA.vue'
import Batch from '../components/Batch/BatchA.vue'
import Reminder from '../components/Reminder/ReminderS.vue'
import Practice from '../components/Practice/Practice.vue'

import Settings from '../components/Settings/Settings.vue'
import floatingBanner from '../components/Reminder/FloatingBanner.vue'
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Dashboard,
    children: [
      {
        path: 'Home',
        component: Homepage,
        children: [
          { path: 'guide', component: Guide },
          { path: 'UpdateHistory', component: UpdateHistory },
          { path: 'About', component: About },
          // 默认重定向到 guide
          { path: '', redirect: 'Home/guide' }
        ]
      },
      { path: 'my-data', component: Mydata }, // 根路径默认跳转到 /Home
      { path: 'single', component: Single },
      { path: 'batch', component: Batch },
      { path: 'reminder', component: Reminder },
      { path: 'practice', component: Practice },
      { path: 'settings', component: Settings }
    ]
  },
    {
    path: '/floating-banner',
    component: floatingBanner,
    meta: { noLayout: true },  // 用来关掉全局布局
  },
  // 如果有登录页等非 dashboard 页面，可放在这里（无 layout）
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router