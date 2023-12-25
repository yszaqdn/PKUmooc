import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router.js'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
const app = createApp(App)

app.use(router)
app.use(ElementPlus)
app.mount('#app')
app.config.globalProperties.SERVER = "http://127.0.0.1:8000"

router.beforeEach((to, from, next) => {
    if(to.meta.title) {
        document.title = to.meta.title
    }
    next()
})

import * as ElementPlusIconsVue from '@element-plus/icons-vue'
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}