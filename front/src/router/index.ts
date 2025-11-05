import { createRouter, createWebHistory } from 'vue-router'

import Guide from '../components/Home/Guide.vue'
import UpdateHistory from '../components/Home/UpdateHistory.vue'
import About from '../components/Home/About.vue'

const routes = [
  // {
  //   path: '/board',
  //   // component: Dashboard,
  //   children: [
  //     { path: 'recommended', component: Recommended, name: 'Recommended' },
  //   ]
  // },
  { path: '/Home/guide', component: Guide },
  { path: '/Home/UpdateHistory', component: UpdateHistory },
  { path: '/Home/About', component: About }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router