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
                <div class="course-tag">
                    Teachers: {{ course.teachers.join(', ') }}
                </div>

            </div>
            <div class="course-title">
                <router-link :to="{ name: 'StudentCourse', params: { id: course.id } }">
                    {{ course.title }}
                </router-link>
            </div>


        </div>
    </div>

    <div id="material-box">
        <div style="
            display: flex;
            font-size: bolder;
            font-family: Tahoma,Arial;
            padding: 5px 0px 5px 15px;
            
        ">
            <h1>Recent Materials</h1>
        </div>
        <div v-for="material in this.materials" :key="material.id" class="materials">
            <div class="material-info">
                <div class="material-tag">
                    course: {{ material.course }}
                </div>
                <div class="material-tag">
                    updated time: {{ formatted_time(material.updated_time) }}
                </div>
            </div>
            <div class="material-title">
                <router-link :to="{
                    name: 'StudentMaterial',
                    params: { id: getCourseIdFromUrl(material.url), materialID: material.id }
                }">
                {{ material.title }}
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { RouterLink } from 'vue-router';

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
        getCourseIdFromUrl(url) {
            const parts = url.split('/');
            const courseIndex = parts.indexOf('course');
            return parts[courseIndex + 1];
        },
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
        try {
            for (let course of this.courses) {
                const response2 = await axios.get('/api/course/' + course.id + '/material/', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }

                });

                if (typeof this.materials === 'undefined') {
                    this.materials = response2.data;
                } else {
                    for (let material of response2.data) {
                        this.materials.push(material);
                    }

                }

                console.log("materials", response2.data);
            }
            this.materials.sort((a, b) => {
                if (a.updated_time < b.updated_time) {
                    return 1;
                } else if (a.updated_time > b.updated_time) {
                    return -11;
                } else {
                    return 0;
                }
            });
        }
        catch (error) {
            console.error(error);
            // handle error here
        }
        console.log("materials_all", this.materials);
    },
    components: { RouterLink }
}

</script>

<style scoped>
#course-box {
    position: absolute;
    top: 50px;
    left: 50px;
    background: #f0f0f0;
    border: 2px solid rgb(195, 190, 190);
    border-radius: 5px;
    width: 40%;

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

.material-info {
    display: flex;
}

.material-title {
    font-size: large;
    font-weight: bolder;
    font-family: Georgia, Arial, sans-serif;
    color: black;
    text-decoration: none;
    padding: 5px 5px 5px 0;
}

.material-tag {
    padding: 2px 5px 2px 5px;
    margin: 5px 5px 5px 0;
    font-family: Georgia, Arial, sans-serif;
    font-size: small;
    background-color: #4e4e4e;
    color: whitesmoke;
    border-radius: 5px;
}

#material-box {
    position: absolute;
    top: 50px;
    left: 700px;
    background: #f0f0f0;
    border: 2px solid rgb(195, 190, 190);
    border-radius: 5px;
    width: 40%;
}
</style>