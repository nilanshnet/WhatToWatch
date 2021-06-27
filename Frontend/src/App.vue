<template>
  <div id="app">
    <div id="nav">
      <Nav/>
    </div>
    <router-view/>
  </div>
</template>

<script>
import Nav from '@/components/Nav.vue'
import {mapActions} from 'vuex';
export default {

  mounted(){
    this.authAction();
  },

  components: {
    Nav,
  },

  methods: {
    ...mapActions("auth", ["authAction"])

  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #ffffff;
  background-color: black;
  min-height: 100vh;

}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color:white;
  margin-right: 5rem;
}

#nav a.router-link-exact-active {
  color:green
}
</style>
