<!-- frontend/src/views/ArticleCreate.vue -->

<template>
  <BlogHeader />
  <div id="article-create">
    <h3>发表文章</h3>
    <form>
      <div class="form-elem">
        <span>标题：</span>
        <input v-model="title" type="text" placeholder="输入标题" />
      </div>
      <div class="form-elem">
        <span>标签：</span>
        <input v-model="tags" type="text" placeholder="输入标签，用逗号分隔" />
      </div>
      <editor v-model="body"  :toolbarsExclude="toolbarsExclude" @onUploadImg="onFileChange" />
      <div class="form-elem">
        <button v-on:click.prevent="submit">提交</button>
      </div>
    </form>
  </div>
  <BlogFooter />
</template>

<script lang='typescrip'>
import BlogHeader from "@/components/BlogHeader.vue";
import BlogFooter from "@/components/BlogFooter.vue";
import axios from "axios";
import authorization from "@/utils/authorization";
import Editor from "md-editor-v3";
import "md-editor-v3/lib/style.css";

//表格显示

export default {
  name: "ArticleCreate",
  components: { BlogHeader, Editor, BlogFooter },
  data: function () {
    return {
 
      // 文章标题
      title: "",
      // 文章正文
      body: "",
      // 数据库中所有的分类
      categories: [],
      // 选定的分类
      selectedtopic: null,
      // 标签
      tags: "",
      // 标题图 id
      avatarID: null,
      text: "",
      // toolbarsExclude:['github'],
    };
  },
  mounted() {
    // 页面初始化时获取所有分类
    axios
      .get("/api/topic/")
      .then((response) => (this.categories = response.data));
  },
  methods: {
  async onUploadImg(files: FileList, callback: (urls: string[]) => void) {
  const res = await Promise.all(
    Array.from(files).map((file) => {
      return new Promise((rev, rej) => {
        const form = new FormData();
        form.append('file', file);

        axios
          .post('/api/avatar/', form, {
            headers: {
              'Content-Type': 'multipart/form-data',
            Authorization: "Bearer " + localStorage.getItem("access.myblog"),
            }
          })
          .then((res) => rev(res))
          .catch((error) => rej(error));
      });
    })
  );

  callback(res.map((item: any) => item.data.url));
},
    onFileChange(e) {
      // 将文件二进制数据添加到提交数据中
      const file = e.target.files[0];
      let formData = new FormData();
      formData.append("content", file);

      // 略去鉴权和错误处理的部分
      axios
        .post("/api/avatar/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: "Bearer " + localStorage.getItem("access.myblog"),
          },
        })
        .then((response) => (this.avatarID = response.data.id,console.log(response.data + '')));
    },
    // 根据分类是否被选中，按钮的颜色发生变化
    // 这里可以看出 css 也是可以被 vue 绑定的，很方便
    topicStyle(topic) {
      if (
        this.selectedtopic !== null &&
        topic.id === this.selectedtopic.id
      ) {
        return {
          backgroundColor: "black",
        };
      }
      return {
        backgroundColor: "lightgrey",
        color: "black",
      };
    },
    // 选取分类的方法
    choosetopic(topic) {
      // 如果点击已选取的分类，则将 selectedtopic 置空
      if (
        this.selectedtopic !== null &&
        this.selectedtopic.id === topic.id
      ) {
        this.selectedtopic = null;
      }
      // 如果没选中当前分类，则选中它
      else {
        this.selectedtopic = topic;
      }
    },
    // 点击提交按钮
    submit() {
      const that = this;
      // 前面封装的验证函数又用上了
      authorization().then(function (response) {
        if (response[0]) {
          // 需要传给后端的数据字典
          let data = {
            title: that.title,
            body: that.body,
          };
          // 添加分类
          if (that.selectedtopic) {
            data.topic_id = that.selectedtopic.id;
          }
          // 新增代码
          // 添加标题图 id
          data.avatar_id = that.avatarID;
          // 标签预处理
          data.tags = that.tags
            // 用逗号分隔标签
            .split(/[,，]/)
            // 剔除标签首尾空格
            .map((x) => x.trim())
            // 剔除长度为零的无效标签
            .filter((x) => x.charAt(0) !== "");

          // 将发表文章请求发送至接口
          // 成功后前往详情页面
          const token = localStorage.getItem("access.myblog");
          axios
            .post("/api/article/", data, {
              headers: { Authorization: "Bearer " + token },
            })
            .then(function (response) {
              that.$router.push({
                name: "ArticleDetail",
                params: { id: response.data.id },
              });
            });
        } else {
          alert("令牌过期，请重新登录。");
        }
      });
    },
  },
};
</script>

<style scoped>
.topic-btn {
  margin-right: 10px;
}
#article-create {
  text-align: center;
  font-size: large;
}
form {
  text-align: left;
  padding-left: 100px;
  padding-right: 10px;
}
.form-elem {
  padding: 10px;
  text-align: center;
}
input {
  height: 25px;
  padding-left: 10px;
  width: 90%;
}
button {
  height: 35px;
  cursor: pointer;
  border: none;
  outline: none;
  background: steelblue;
  color: whitesmoke;
  border-radius: 5px;
  width: 60px;
}
</style>
