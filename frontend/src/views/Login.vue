<template>
  <BlogHeader />


    <div>
      <div id="signin">
        <h3>登录账号</h3>
        <form>
          <div class="form-elem">
            <span>账号：</span>
            <input v-model="signinName" type="text" placeholder="输入用户名" />
          </div>

          <div class="form-elem">
            <span>密码：</span>
            <input v-model="signinPwd" type="password" placeholder="输入密码" />
          </div>

          <div class="form-elem">
             <router-link to="/register" class="login-link">没有账号，跳转注册</router-link>
            <button class="form-login" v-on:click.prevent="signin">登录</button>
          </div>
        </form>
      </div>
  </div>

  <BlogFooter />
</template>

<script>
import axios from "axios";
import BlogHeader from "@/components/BlogHeader.vue";
import BlogFooter from "@/components/BlogFooter.vue";

export default {
  name: "Login",
  components: { BlogHeader, BlogFooter },
  data: function () {
    return {
      signinName: "",
      signinPwd: "",
    };
  },
  methods: {
    signin() {
      const that = this;
   axios
        .post("/api/token/", {
          username: that.signinName,
          password: that.signinPwd,
        })
        .then(function (response) {
          const storage = localStorage;
          // Date.parse(...) 返回1970年1月1日UTC以来的毫秒数
          // Token 被设置为1分钟，因此这里加上60000毫秒
          const expiredTime = Date.parse(response.headers.date) + 360000;
          // 设置 localStorage
          storage.setItem("access.myblog", response.data.access);
          storage.setItem("refresh.myblog", response.data.refresh);
          storage.setItem("expiredTime.myblog", expiredTime);
          storage.setItem("username.myblog", that.signinName);
          // 路由跳转
          // 登录成功后回到博客首页

          that.$router.push({ name: "Home" });
        })
      // 读者自行补充错误处理
        .catch(
                        function (error) {
                          console.log(error)
          alert('账号或密码错误:');
          // Handling Error here...
          // https://github.com/axios/axios#handling-errors
        }

        )
       axios
            .get("/api/user/" + that.signinName + "/").then(function (response) {
              const storage = localStorage;
              storage.setItem("isSuperuser.myblog", response.data.is_superuser);
      });

    },
  },
};
</script>

<style scoped>


#signin {
  text-align: center;
}

.form-elem {
  padding: 10px;
}

.form-login{
 margin-left:50px;
}

input {
  height: 25px;
  padding-left: 10px;
}
button {
  height: 35px;
  cursor: pointer;
  border: none;
  outline: none;
  background: gray;
  color: whitesmoke;
  border-radius: 5px;
  width: 100px;
}

.login-link {
  color: black;
}
</style>