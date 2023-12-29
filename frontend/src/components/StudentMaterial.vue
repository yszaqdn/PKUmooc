<template>
    <div class="material-box">
        <div class="title">
            {{ material.title }}
        </div>

        <div class="subtitle">
            {{ material.course }} {{ material.teacher }} {{ formatted_time(material.updated_time) }}
        </div>

        <div class="body">
            {{ material.content }}
        </div>
    </div>
</template >

<script>
import axios from 'axios'

export default {
    data() {
        return {
            material: [],
        }
    },
    methods: {
        formatted_time: function (iso_date_string) {
            const date = new Date(iso_date_string);
            return date.toLocaleDateString()
        }
    },
    async created() {
        let token = localStorage.getItem('token');
        try {
            const response = await axios.get('/api/course/' + this.$route.params.id + '/material/' + this.$route.params.materialID, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            console.log("this is material", response.data);

            this.material = response.data;
            console.log(this.material);
        }
        catch (error) {
            console.error(error);
            // handle error here
        }
    },

}
</script>

<style scoped>
.material-box{
    position: absolute;
    top: 5%;
    left: 10%;
    width: 80%;
    height: 80%;
}
.title {
    display: block;
    font-size: 30px;
    font-weight: bold;
    margin: 20px;
    text-align: center;
}

.subtitle {
    display: block;
    font-size: 20px;
    margin: 20px;
    text-align: center;
}

.body {
    display: block;
    font-size: 15px;
    margin: 20px;
    text-align: left;
}
</style>