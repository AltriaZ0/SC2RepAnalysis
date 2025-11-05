// src/main.ts
import { createApp } from 'vue'
import LogViewer from './pages/LogViewer.vue'
import router from './router/index.ts'
import './styles/global.css'

const app = createApp(LogViewer)

app.use(router)

app.mount('#app')