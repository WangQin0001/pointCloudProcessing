<template>
  <div>
    <top></top>

  <div class="login clearfix">
    <div class="login-wrap">
      <el-row type="flex" justify="center">
        <el-form ref="registerFormRef" :model="user" :rules="rules" status-icon label-width="80px" @submit.prevent @keyup.enter.native="doRegister">
          <h3>Register Page</h3>
          <hr>
          <el-form-item prop="username" label="username">
            <el-input v-model="user.username" placeholder="Please enter username"></el-input>
          </el-form-item>
          <el-form-item prop="email" label="e-mail">
            <el-input v-model="user.email" placeholder="Please enter e-mail"></el-input>
            <el-button @click="getCatpcha" type="primary" :disabled="canClick">{{ content }}</el-button>
          </el-form-item>
          <el-form-item prop="catpcha" label="catpcha">
            <el-input v-model="user.catpcha" placeholder="Please enter catpcha "></el-input>
          </el-form-item>
          <el-form-item prop="password" label="password">
            <el-input v-model="user.password" show-password placeholder="Please enter password"></el-input>
          </el-form-item>
          <el-form-item prop="rePassword" label="confirm">
            <el-input v-model="user.rePassword" show-password placeholder="Please enter password again"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" icon @click="doRegister" @keyup.enter="doRegister">Register Now</el-button>
            <router-link to="/login" style="margin-left: 50px;">Login</router-link>
          </el-form-item>
        </el-form>
      </el-row>
  </div>
  </div>
  </div>


</template>
   
<script>
import { register,getCatpcha } from "../network/loginAndRegister.js";
import top from './Top.vue'

export default {
    name: "register",
  components:{
      top
  },
    data() {
        return {
          totalTime: 10,
          canClick: false,
          content:'Get Captcha',
            user: {
                username: "",
                email: "",
                password: "",
                rePassword:"",
                catpcha:""
              // username: "wangqin",
              // email: "wangqinstu@outlook.com",
              // password: "wq111111",
              // rePassword:"wq111111",
              // catpcha:""
            },
            rules:{
              username: [{
                required: true,
                message: 'username is required! ',
                trigger: 'blur'
              },
                {
                  min: 3,
                  max: 20,
                  message: 'between 3 and 20 characters',
                  trigger: 'blur'
                }
              ],
              password:[{
                required: true,
                message: 'password is required! ',
                trigger: 'blur'
              },
                {
                  min: 6,
                  max: 20,
                  message: 'between 6 and 20 characters',
                  trigger: 'blur'
                },
              ],
              rePassword:[{
                required: true,
                message: 'password is required! ',
                trigger: 'blur'
              },
                {
                  min: 6,
                  max: 20,
                  message: 'between 6 and 20 characters',
                  trigger: 'blur'
                },
              ],
              email: [{
                required: true,
                message: 'email is required! ',
                trigger: 'blur'
              },
                {
                  type: 'email',
                  message: 'check your email type',
                  trigger: ['blur', 'change']
                },
              ],
              catpcha: [{
                required: true,
                message: 'catpcha is required! ',
                trigger: 'blur'
              },
                {
                  min: 4,
                  max: 4,
                  message: 'catpcha has 4 characters',
                  trigger: 'blur'
                },
              ],
            }
        };
    },
    methods: {
      getCatpcha() {
        if (this.canClick) return;
        this.canClick = true;
        this.totalTime = 10; // 设置计时器初始值
        this.content = 'resend in ' + this.totalTime + 's';
        let clock = window.setInterval(() => {
          this.totalTime--;
          this.content = 'resend in ' + this.totalTime + 's';
          if (this.totalTime < 0) {
            window.clearInterval(clock);
            this.content = 'resend';
            this.totalTime = 10;
            this.canClick = false;
          }
        }, 1000);

        getCatpcha(this.user.email).then(res => {
          console.log(res);
          if (res.code === 200) {
            this.$message.success('catpcha sent success!');
          }
        }).catch(error => {
          console.log(error);
          this.$message.error('get catpcha failed');
        });
      },

        doRegister() {
          this.$refs.registerFormRef.validate(valid => {
            if (!valid) {
              this.$message.error("input is invalid, please check!")
            } else {
                    register(this.user.username,this.user.email,this.user.catpcha,this.user.password,this.user.rePassword).then(res => {
                      console.log(res)
                      if (res.code === 200) {
                            console.log(res)
                            this.$message.success("register succeed！")
                            this.$router.push('/user/login')
                            this.innerVisible = false
                        } else {
                            this.$message.success(res.data)
                        }
                    }).catch(error => {
                        this.$message.error('register failed！');
                    })
                }
            })
        }
    }
};
</script>
   
  <!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.login {
    width: 100%;
    height: 740px;
    /* background: url("../assets/images/bg1.png") no-repeat; */
    background-size: cover;
    overflow: hidden;
}

.login-wrap {
    /* background: url("../assets/images/login_bg.png") no-repeat; */
    background-size: cover;
    width: 500px;
    height: 600px;
    margin: 215px auto;
    overflow: hidden;
    padding-top: 10px;
    line-height: 20px;
}

a {
    text-decoration: none;
    color: #aaa;
    font-size: 15px;
}

h3 {
    color: #0babeab8;
    font-size: 24px;
}

hr {
    background-color: #444;
    margin: 20px auto;
}

.el-button {
    width: 80%;
    margin-left: -50px;
}
</style>