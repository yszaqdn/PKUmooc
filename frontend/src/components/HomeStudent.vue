

<template>
    <div>
      <div v-for="course in courses" :key="course.id">
        <h2>{{ course.title }}</h2>
        <p>{{ course.year }} {{ course.session }}</p>
        <p>Teachers: {{ course.teachers.join(', ') }}</p>
        <p>Students: {{ course.students.join(', ') }}</p>
      </div>
    </div>
  </template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            courses: [],
        };
    },
    async created() {
        let IDnum = localStorage.getItem('IDnum');
        let token = localStorage.getItem('token');
        try {
            const response = await axios.get('/api/course/',{
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            console.log(response);
            this.courses = response.data;
            console.log(this.courses)
        } catch (error) {
            console.error(error);
            // handle error here
        }
    },
}

</script>