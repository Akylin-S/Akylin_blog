<template>


    <ArticleList/>

    <BlogFooter/>

</template>

<script>
    import logout from "@/utils/logout";
    export default {
        name: 'Logout',
      mounted() {
          const that = this;
        logout().then((data) => ([this.hasLogin, this.username,this.isSuperuser] = data));
                  that.$router.push({ name: "Home" });

  },
    }
</script>
