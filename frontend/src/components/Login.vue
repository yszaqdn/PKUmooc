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
                    <el-form-item prop="IDnum">
                        <el-input prefix-icon="Avatar" v-model="user.IDnum" placeholder="请输入学号/工号"></el-input>
                    </el-form-item>

                    <el-form-item prop="password">
                        <el-input prefix-icon="Lock" show-password v-model="user.password" placeholder="请输入密码"></el-input>
                    </el-form-item>


                    <el-form-item>
                        <el-button id="loginButton" type="primary" style="width: 100%" @click="EventLogin">
                            登录
                        </el-button>
                    </el-form-item>
                    <div style="display: flex">
                        <div style="flex: 1; text-align: center">
                            还没有账号：请
                            <span style="color: rgb(92, 214, 92); cursor: pointer" @click="Switch2Register">注册</span>
                        </div>
                    </div>
                </el-form>
            </el-scrollbar>
        </div>
    </div>
</template>

<script >
import axios from 'axios'

export default {
    data() {
        return {
            user: {
                IDnum: '',
                password: '',

            },
            rules: {
                IDnum: [
                    { required: true, message: "请输入学号/工号", trigger: "blur" },
                    { min: 10, max: 10, message: "长度为10个字符", trigger: ["blur", "change"] },
                    { pattern: /^[0-9]*$/, message: "学号/工号应为纯数字", trigger: ["blur", "change"] },
                ],
                password: [
                    { required: true, message: "请输入密码", trigger: "blur" },
                    { min: 4, max: 20, message: "长度在 4 到 20 个字符", trigger: ["blur", "change"] },
                    { pattern: /.*[a-zA-z].*/, message: "密码应包含字母", trigger: ["blur", "change"] },
                    { pattern: /.*[0-9].*/, message: "密码应包含数字", trigger: ["blur", "change"] },
                ],

            },
        }
    },

    methods: {

        EventLogin() {
            const that = this
            this.$refs.loginRef.validate((valid) => {
                if (valid) {
                    let senddata = {
                        action: 'login',
                        IDnum: this.user.IDnum,
                        password: this.user.password,
                    }
                    axios
                        .post("/api/token/", senddata) // 路径存疑
                        .then((res) => {
                            if (res.status == 200) {
                                that.$message({
                                    message: "登录成功",
                                    type: "success",
                                    duration: 1000,
                                })
                                that.$store.commit('setUser', res.data.data)
                                that.$router.push('/home')
                            }
                            else {
                                alert("学号/工号或密码错误");
                                that.$message({
                                    message: "登录失败",
                                    type: "error",
                                    duration: 1000,
                                })
                            }
                        })
                        .catch((err) => {
                            console.log(err);
                        });
                } else {
                    return false
                }
            })
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
