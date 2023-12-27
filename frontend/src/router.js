import { createRouter, createWebHistory } from 'vue-router'

import Register from './components/Register.vue'
import Login from './components/Login.vue'
import HomeStudent from './components/HomeStudent.vue'
import HomeTeacher from './components/HomeTeacher.vue'
import StudentCourse from './components/StudentCourse.vue'

import APP from './App.vue'
const router = createRouter({
    history: createWebHistory(),
    routes: [
        { 
            path: '/', 
            component: Login,
            meta: { title: "登录" },
        },
        
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
            path: '/student/home',
            component: HomeStudent,
            meta: { title: "学生主页" },
        },
        {
            path: '/student/course/:id',
            component: StudentCourse,
            name: 'StudentCourse',
            meta: { title: "课程" },
        },
        {
            path: '/teacher/home',
            component: HomeTeacher,
            meta: { title: "教师主页" },
        }
    ]
})

export default router;