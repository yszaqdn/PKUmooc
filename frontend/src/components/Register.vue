<template>
    <div class="registerBox">
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
                欢迎注册
            </div>
            <el-scrollbar style="width: 100%; height: 100%">
                <el-form id="registerForm" :model="user" style=" text-align: center" :rules="rules" ref="registerRef">
                    <el-form-item prop="IDnum">
                        <el-input prefix-icon="Avatar" v-model="user.IDnum" placeholder="请输入学号/工号"></el-input>
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

                    <el-form-item prop="phonenum">
                        <el-input prefix-icon="Iphone" v-model="user.phonenum" placeholder="请输入电话号码"></el-input>
                    </el-form-item>


                    <el-row>
                        <el-col :span="13">
                            <el-form-item prop="name">
                                <el-input prefix-icon="UserFilled" v-model="user.name" placeholder="请输入姓名"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="10" :offset="1">
                            <el-select v-model="user.sex" placeholder="请选择性别">
                                <el-option v-for="item in sexOptions" :key="item.value" :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-col>
                    </el-row>


                    <el-row>
                        <el-col :span="13">
                            <el-form-item prop="dept">
                                <el-input prefix-icon="School" v-model="user.dept" placeholder="请输入学院"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="10" :offset="1">
                            <el-select v-model="user.identity" placeholder="请选择身份">
                                <el-option v-for="item in identityOptions" :key="item.value" :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-col>
                    </el-row>
                    <el-form-item prop="grade">
                        <el-input v-model="user.grade" placeholder="请输入年级（如果是教师，请输入0）"></el-input>
                    </el-form-item>

                    <el-form-item>
                        <el-button id="registerButton" type="primary" style="width: 100%" @click="EventRegister">
                            注册
                        </el-button>
                    </el-form-item>
                    <div style="display: flex">
                        <div style="flex: 1; text-align: center">
                            已经有账号：请
                            <span style="color: rgb(92, 214, 92); cursor: pointer" @click="Switch2Login">登录</span>
                        </div>
                    </div>
                </el-form>
            </el-scrollbar>
        </div>
    </div>
</template>

<script >
import axios from "axios";

export default {
    data() {
        return {
            sexOptions: [
                {
                    value: 'Male',
                    label: '♂',
                },
                {
                    value: 'Female',
                    label: '♀',
                }],
            identityOptions: [
                {
                    value: 'teacher',
                    label: 'teacher',
                },
                {
                    value: 'student',
                    label: 'student',
                }],
            user: {
                IDnum: '', // 学号/工号
                password: '',   // 密码
                confirmpassword: '',    // 确认密码
                email: '',  // 邮箱
                phonenum: '',   // 电话号码
                name: '',       // 姓名
                sex: '',    // 性别
                dept: '',   // 学院
                identity: '', // 身份
                grade: '',  // 年级
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
                phonenum: [
                    { required: true, message: '请输入电话号码', trigger: 'blur' },
                    {
                        pattern: /^1[3456789]\d{9}$/,
                        message: "电话号码格式错误",
                        trigger: ["blur", "change"],
                    }
                ],
                grade: [
                    { required: true, message: '请输入年级', trigger: 'blur' },
                    {
                        pattern: /^(20[0-9]{2}|0)$/,
                        message: "请按格式输入，如2020",
                        trigger: ["blur", "change"],
                    }
                ]
            },
        }
    },

    methods: {

        async EventRegister() {
            let senddata = {
                action: 'register',
                id: this.user.IDnum,
                password: this.user.password,
                confirmpassword: this.user.confirmpassword,
                email: this.user.email,
                phone: this.user.phonenum,
                name: this.user.name,
                sex: this.user.sex,
                dept: this.user.dept,
                identity: this.user.identity,
                grade: this.user.grade,
            };

            this.$refs.registerRef.validate(async (valid) => {
                if (valid) {
                    console.log(senddata);
                    await axios
                        .post('/api/register/', senddata)
                        .then(res => {
                            console.log(res);
                            if (res.status === 201) {
                                this.$message({
                                    message: '注册成功',
                                    type: 'success'
                                });
                                this.$router.push('/login')
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
        Switch2Login() {
            this.$router.push('/login')
        }
    }
}
</script>

<style scoped>
.registerBox {
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
