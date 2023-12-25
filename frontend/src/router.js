import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import TheWelcome from './components/TheWelcome.vue'
import Register from './components/Register.vue'
import Login from './components/Login.vue'
import HomeStudent from './components/HomeStudent.vue'
import HomeTeacher from './components/HomeTeacher.vue'


import APP from './App.vue'
const router = createRouter({
    history: createWebHistory(),
    routes: [
        { 
            path: '/', 
            component: Login,
            meta: { title: "登录" },
        },
        { path: '/hello', component: HelloWorld },
        { path: '/welcome', component: TheWelcome },
        { 
            path: '/register', 
            component: Register,
            meta: { title: '注册' },
        },
        { 
            path: '/login', 
            component: Login,
            meta: { title: "登录" },
        },
        {
            path: '/home/student',
            component: HomeStudent,
            meta: { title: "学生主页" },
        },
        {
            path: '/home/teacher',
            component: HomeTeacher,
            meta: { title: "教师主页" },
        }
    ]
})

export default router;