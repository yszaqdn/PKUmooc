<template>
    <div class="loginBox">
        <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
        flex-grow: 0;
        ">
            <div style="
          font-size: 20px;
          font-weight: bold;
          text-align: center;
          margin-bottom: 20px;
            ">
                欢迎登录
            </div>
            <el-scrollbar style="width: 100%; height: 100%">
                <el-form id="loginForm" :model="user" style=" text-align: center" :rules="rules" ref="loginRef">
                    <el-form-item prop="username">
                        <el-input prefix-icon="Avatar" v-model="user.username" placeholder="请输入用户名或邮箱"></el-input>
                    </el-form-item>

                    <el-form-item prop="password">
                        <el-input prefix-icon="Lock" show-password v-model="user.password"
                            placeholder="请输入密码"></el-input>
                    </el-form-item>


                    <el-form-item>
                        <el-button id="loginButton" type="primary" style="width: 100%" @click="EventLogin">
                            登录
                        </el-button>
                    </el-form-item>
                    <div style="display: flex">
                        <div style="flex: 1; text-align: center">
                            还没有账号：请
                            <span style="color: rgb(92, 214, 92); cursor: pointer"
                                @click="Switch2Register">注册</span>
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
            user: {
                username: '',
                password: '',
                
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
                ]
            },
        }
    },

    methods: {
        EventSendVerifyCode() {
            // your code here
        },
        EventRegister() {
            // your code here
        },
        Switch2Register() {
            this.$router.push('/register')
        }
    }
}
</script>

<style>
.loginBox {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    background-color: white;
    width: 130%;
    height: 100%;
    border-radius: 5px;

}
</style>
