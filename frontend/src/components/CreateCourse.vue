<template>
    <div class="createBox">
        <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        width: 40%;
        height: 80%;
        flex-grow: 0;
      ">
            <div style="
          font-size: 20px;
          font-weight: bold;
          text-align: center;
          margin-bottom: 20px;
        ">
                请输入课程信息
            </div>
            <el-scrollbar style="width: 100%; height: 100%">
                <el-form id="createForm" :model="course_info" style=" text-align: center" :rules="rules" ref="createRef">
                    <el-form-item prop="id">
                        <el-input prefix-icon="Document" v-model="course_info.id" placeholder="请输入课程号"></el-input>
                    </el-form-item>
                    <el-form-item prop="title">
                        <el-input prefix-icon="infoFilled" v-model="course_info.title" placeholder="请输入课程名"></el-input>
                    </el-form-item>

                    <el-row>
                        <el-col :span="13">
                            <el-form-item prop="year">
                                <el-input prefix-icon="Calendar" v-model="course_info.year"
                                    placeholder="请输入授课学年"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="10" :offset="1">
                            <el-select prefix-icon="Calendar" v-model="course_info.session" placeholder="选择授课学期">
                                <el-option v-for="item in sessionOptions" :key="item.value" :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-col>
                    </el-row>
                    <el-form-item prop="students">
                        <el-input prefix-icon="Avatar" v-model="course_info.students"
                            placeholder="请输入选课学生学号，用,隔开"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button id="createButton" type="primary" style="width: 100%" @click="EventCreate">
                            创建
                        </el-button>
                    </el-form-item>
                    <div style="display: flex">
                        <div style="flex: 1; text-align: center">
                            还没有想好：返回
                            <span style="color: rgb(92, 214, 92); cursor: pointer" @click="Switch2Home">主页</span>
                        </div>
                    </div>
                </el-form>

            </el-scrollbar>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
export default {
    data() {
        return {
            course_info: {
                id: '',
                title: '',
                year: '',
                session: '',
                teacher: '',
                students: [],
            },
            sessionOptions: [
                {
                    value: 'Spring',
                    label: '春季',
                },
                {
                    value: 'Fall',
                    label: '秋季',
                }],

            rules: {

            },
        }
    },

    methods: {

        async EventCreate() {
            let senddata = {
                action: 'create',
                id: this.course_info.id,
                title: this.course_info.title,
                year: this.course_info.year,
                session: this.course_info.session,
                students: this.course_info.students.split(','),
            }

            this.$refs.createRef.validate(async (valid) => {
                if (valid) {
                    console.log(senddata);
                    let token = localStorage.getItem('token');
                    await axios
                        .post('/api/course/', senddata, {
                            headers: {
                                'Authorization': `Bearer ${token}`
                            }
                        })
                        .then(res => {
                            console.log(res);
                            if (res.status === 200) {
                                this.$message({
                                    message: '注册成功',
                                    type: 'success'
                                });
                                this.$router.push('/teacher/home')
                            } else {
                                alert(res.data.id);
                                this.$message({
                                    message: res.data.message,
                                    type: 'error'
                                });
                            }
                        })
                        .catch((err) => {
                            console.log(err);
                        });
                } else {
                    this.$message({
                        message: '请检查输入',
                        type: 'error'
                    });
                    return false;
                }
            });
        },
        Switch2Home() {
            this.$router.push('/teacher/home')
        },

    }
}
</script>




<style scoped>
.createBox {
    position: absolute;
    top: 50px;
    left: 150px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;

    background-color: white;
    width: 80%;
    height: 80%;
    border-radius: 4px;

}
</style>