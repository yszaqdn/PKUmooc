<template>
    <div class="registerBox">
        <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        width: 80%;
        height: 100%;
        flex-grow: 0;
      ">
            <div style="
          font-size: 20px;
          font-weight: bold;
          text-align: center;
          margin-bottom: 20px;
        ">
                欢迎注册
            </div>
            <el-scrollbar style="width: 100%; height: 100%">
                <el-form id="registerForm" :model="user" style=" text-align: center" :rules="rules" ref="registerRef">
                    <el-form-item prop="username">
                        <el-input prefix-icon="Avatar" v-model="user.username" placeholder="请输入4-20位用户名"></el-input>
                    </el-form-item>

                    <el-form-item prop="password">
                        <el-input prefix-icon="Lock" show-password v-model="user.password"
                            placeholder="请输入4-20位密码，包含字母与数字"></el-input>
                    </el-form-item>

                    <el-form-item prop="confirmpassword">
                        <el-input prefix-icon="Lock" show-password v-model="user.confirmpassword"
                            placeholder="请确认密码"></el-input>
                    </el-form-item>

                    <el-form-item prop="email">
                        <el-input prefix-icon="Message" v-model="user.email" placeholder="请输入邮箱"></el-input>
                    </el-form-item>

                    
                    <el-row>
                        <el-col :span="13">
                            <el-form-item prop="name">
                                <el-input prefix-icon="UserFilled" v-model="user.name" placeholder="请输入姓名"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="10" :offset="1">
                            <el-select v-model="user.sex" placeholder="请选择性别">
                                <el-option v-for="item in options" :key="item.value" :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-col>
                    </el-row>
                    
                    
                    <el-row>
                        <el-col :span="13">
                            <el-form-item prop="school">
                                <el-input prefix-icon="School" v-model="user.school" placeholder="请输入学院"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="10" :offset="1" >
                            <el-form-item prop="grade">
                                <el-input  v-model="user.grade" placeholder="请输入年级"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    
                    <el-form-item>
                        <el-button id="registerButton" type="primary" style="width: 100%" @click="EventRegister">
                            注册
                        </el-button>
                    </el-form-item>
                    <div style="display: flex">
                        <div style="flex: 1; text-align: center">
                            已经有账号：请
                            <span style="color: rgb(92, 214, 92); cursor: pointer"
                                @click="Switch2Login">登录</span>
                        </div>
                    </div>
                </el-form>
            </el-scrollbar>
        </div>
    </div>
</template>

<script >
export default {
    data() {
        return {
            options: [
                {
                    value: '男',
                    label: '♂',
                },
                {
                    value: '女',
                    label: '♀',
                }],
            user: {
                username: '',
                password: '',
                confirmpassword: '',
                email: '',
                sex: '',
                school: '',
                grade: '',
            },
            rules: {
                username: [
                    { required: true, message: "请输入用户名", trigger: "blur" },
                    { min: 4, max: 20, message: "长度在 4 到 20 个字符", trigger: ["blur", "change"] }
                ],
                password: [
                    { required: true, message: "请输入密码", trigger: "blur" },
                    { min: 4, max: 20, message: "长度在 4 到 20 个字符", trigger: ["blur", "change"] },
                    { pattern: /.*[a-zA-z].*/, message: "密码应包含字母", trigger: ["blur", "change"] },
                    { pattern: /.*[0-9].*/, message: "密码应包含数字", trigger: ["blur", "change"] },
                ],
                confirmpassword: [
                    { required: true, message: '请确认密码', trigger: 'blur' },
                    { min: 4, max: 20, message: '长度在 4 到 20 个字符', trigger: ["blur", "change"] },
                    {
                        validator: (rule, value, callback) => {
                            if (value === this.user.password) {
                                callback();
                            } else {
                                callback(new Error("两次输入密码不一致"));
                            }
                        },
                        message: "两次输入密码不一致",
                        trigger: ["blur", "change"]
                    },

                ],
                email: [
                    { required: true, message: '请输入PKU邮箱', trigger: 'blur' },
                    {
                        pattern: /([0-9a-zA-Z]{1,50})+(@pku.edu.cn|@stu.pku.edu.cn)$/,
                        message: "PKU邮箱格式错误",
                        trigger: ["blur", "change"],
                    }
                ],
                grade: [
                    { required: true, message: '请输入年级', trigger: 'blur' },
                    {
                        pattern: /20[0-9]{2}/,
                        message: "请按格式输入，如2020",
                        trigger: ["blur", "change"],
                    }
                ]
            },
        }
    },

    methods: {
        
        EventRegister() {
            // your code here
        },
        Switch2Login(){
            this.$router.push('/login')
        }
    }
}
</script>

<style>
.registerBox {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;

    background-color: white;
    width: 100%;
    height: 100%;
    border-radius: 4px;

}
</style>
