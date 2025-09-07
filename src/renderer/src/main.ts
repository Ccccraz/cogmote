import 'element-plus/dist/index.css'
// if you just want to import css
import 'element-plus/theme-chalk/dark/css-vars.css'
import '@/assets/main.css'
import '@/assets/electron.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'

const app = createApp(App)
const pinia = createPinia()
app.use(router)
app.use(pinia)
app.use(ElementPlus)
app.mount('#app')
