import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import TheWelcome from './components/TheWelcome.vue'

import APP from './App.vue'
const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: APP },
        { path: '/hello', component: HelloWorld },
        { path: '/welcome', component: TheWelcome },
        
    ]
})

export default router