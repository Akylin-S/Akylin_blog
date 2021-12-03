<!--  frontend/src/components/ArticleList.vue  -->

<template>
  <div v-for="article in info.results" v-bind:key="article.url" id="articles">
    <div class="grid" :style="gridStyle(article)">
      <div class="image-container">
        <img :src="imageIfExists(article)" alt="" class="image" />
      </div>
      <div>
        <div>
          <span v-if="article.category !== null" class="category">
            {{ article.category.title }}
          </span>
          <span v-for="tag in article.tags" v-bind:key="tag" class="tag">
            {{ tag }}
          </span>
        </div>
        <!-- <div class="article-title">
            {{ article.title }}
        </div> -->
        <router-link
          :to="{ name: 'ArticleDetail', params: { id: article.id } }"
          class="article-title"
        >
          {{ article.title }}
        </router-link>
        <div>{{ formatted_time(article.created) }}</div>
      </div>
    </div>
  </div>

  <div id="paginator">
    <span v-if="is_page_exists('previous')">
      <router-link :to="get_path('previous')"> Prev </router-link>
    </span>
    <span class="current-page">
      {{ get_page_param("current") }}
    </span>
    <span v-if="is_page_exists('next')">
      <router-link :to="get_path('next')"> Next </router-link>
    </span>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRoute } from "vue-router";
import getArticleData from "@/composables/getArticleData.js";
import pagination from "@/composables/pagination.js";
// 组合式 APi 入口
export default {
  setup() {
    const info = ref("");
    // 创建路由
    const route = useRoute();
    // 获取文章列表数据的方法

    getArticleData(info, route);
    const { is_page_exists, get_page_param, get_path } = pagination(
      info,
      route
    );
    return {
      info,
      is_page_exists,
      get_page_param,
      get_path,
    };
  },

  methods: {
    formatted_time: function (iso_date_string) {
      const date = new Date(iso_date_string);
      return date.toLocaleDateString();
    },
    imageIfExists(article) {
      // console.log(article)
      if (article.avatar) {
        return article.avatar.content;
      }
    },
    gridStyle(article) {
      if (article.avatar) {
        return {
          display: "grid",
          gridTemplateColumns: "1fr 4fr",
        };
      }
    },
  },
};

</script>

<!-- "scoped" 使样式仅在当前组件生效 -->
<style scoped>
.image {
  width: 180px;
  border-radius: 10px;
  box-shadow: darkslategrey 0 0 12px;
}
.image-container {
  width: 200px;
}
.grid {
  padding-bottom: 10px;
}
#articles {
  padding: 10px;
}

.article-title {
  font-size: large;
  font-weight: bolder;
  color: black;
  text-decoration: none;
  padding: 5px 0 5px 0;
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

#paginator {
  text-align: center;
  padding-top: 50px;
}

a {
  color: black;
}

.current-page {
  font-size: x-large;
  font-weight: bold;
  padding-left: 10px;
  padding-right: 10px;
}
.category {
  padding: 5px 10px 5px 10px;
  margin: 5px 5px 5px 0;
  font-family: Georgia, Arial, sans-serif;
  font-size: small;
  background-color: darkred;
  color: whitesmoke;
  border-radius: 15px;
}
</style>