<template>
    <div class="material-box">
        <div v-for="material in materials" :key="material.id" class="materials">
            <div class="material-info">
            <div class="tag">
                ID: {{ material.id }}
            </div>
            </div>
            <div class="title">
                {{ material.title }}
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
            materials: [],
            assignments: [],
        };
    },
    async created() {
        let token = localStorage.getItem('token');
        try {
            const response = await axios.get('/api/course/' + this.$route.params.id + '/material/', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            console.log(response);

            this.materials = response.data;
            this.materials.sort((a, b) => a.id - b.id);
            console.log(this.materials);
        }
        catch (error) {
            console.error(error);
            // handle error here
        }
    },
    components: { RouterLink }
}
</script>

<style scoped>
.material-box {
    position: absolute;
    top: 50px;
    left: 20px;
    border: 2px solid black;
    border-radius: 5px;
    width:40%;
    
}
.title {
    font-size: large;
    font-weight: bolder;
    font-family: Georgia, Arial, sans-serif;
    color: black;
    text-decoration: none;
    padding: 5px 5px 5px 0;
}
.material-info {
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
}
</style>