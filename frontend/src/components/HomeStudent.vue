<template>
    <div class="course-box">
        <div v-for="course in courses" :key="course.id" class="courses">
            <div class="course-info">
                <div class="tag">
                    {{ course.year }}
                </div>
                <div class="tag">
                    {{ course.session }}
                </div>
                <div class="tag">
                    Teachers: {{ course.teachers.join(', ') }}
                </div>
                
            </div>
            <div class="course_title">
                {{ course.title }}
            </div>




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
            const response = await axios.get('/api/course/', {
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

<style>
.course-box {
    position: absolute;
    top: 50px;
    left: 20px;
    border: 2px solid black;
    border-radius: 5px;
    width:40%;
    
}
.courses {
    padding: 10px;
}

.course_title {
    font-size: large;
    font-weight: bolder;
    font-family: Georgia, Arial, sans-serif;
    color: black;
    text-decoration: none;
    padding: 5px 5px 5px 0;
}

.course-info {
    display: flex;
}

.tag {
    padding: 2px 5px 2px 5px;
    margin: 5px 5px 5px 0;
    font-family: Georgia, Arial, sans-serif;
    font-size: small;
    background-color: #4e4e4e;
    color: whitesmoke;
    border-radius: 5px;
}</style>