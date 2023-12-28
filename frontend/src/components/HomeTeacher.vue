<template>
    <div id="course-box">
        <div style="
            display: flex;
            font-size: bolder;
            font-family: Tahoma,Arial;
            padding: 5px 0px 5px 15px;
            
        ">
            <h1>My Courses</h1>
        </div>

        <div v-for="course in courses" :key="course.id" class="courses">
            <div class="course-info">
                <div class="course-tag">
                    ID: {{ course.id }}
                </div>
                <div class="course-tag">
                    {{ course.year }}
                </div>
                <div class="course-tag">
                    {{ course.session }}
                </div>
                

            </div>
            <div class="course-title">
                <router-link :to="{ name: 'TeacherCourse', params: { id: course.id } }">
                    {{ course.title }}
                </router-link>
            </div>
            

        </div>
        <a-button  type="link" class="create-class" @click="CreateCourse">
            <PlusOutlined />创建新课程
        </a-button>
    </div>

</template>

<script>
import axios from 'axios'
import { RouterLink } from 'vue-router';
import { PlusOutlined } from '@ant-design/icons-vue';

export default {
    data() {
        return {
            courses: [],
            materials: [],
        };
    },
    methods: {
        formatted_time: function (iso_date_string) {
            const date = new Date(iso_date_string);
            return date.toLocaleDateString()
        },
        CreateCourse: function () {
            this.$router.push({ name: 'CreateCourse' });
        }
    },
    async created() {
        let token = localStorage.getItem('token');
        try {
            const response1 = await axios.get('/api/course/', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            console.log(response1);
            this.courses = response1.data;
            console.log(this.courses);
        }
        catch (error) {
            console.error(error);
            // handle error here
        }
        
        
    },
    components: { RouterLink ,
        PlusOutlined,}
}

</script>

<style>
#course-box {
    position: absolute;
    top: 50px;
    left: 100px;
    background: #f0f0f0;
    border: 2px solid rgb(195, 190, 190);
    border-radius: 5px;
    width: 50%;

}

.courses {
    padding: 10px;
}

.course-title {
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

.course-tag {
    padding: 2px 5px 2px 5px;
    margin: 5px 5px 5px 0;
    font-family: Georgia, Arial, sans-serif;
    font-size: small;
    background-color: #4e4e4e;
    color: whitesmoke;
    border-radius: 5px;
}

.create-class {
    
    
    background: #f0f0f0;
   
    width: 10%;
    height: 10%;
    font-size: 30;
    
    font-family: Georgia, Arial, sans-serif;
    color: black;
    text-decoration: none;
    padding: 10px 5px 5px 10px;
}

</style>