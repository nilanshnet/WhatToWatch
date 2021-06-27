<template>
  <div>
    <b-navbar type="dark" variant="dark">
      <b-navbar-brand>
        <h2 style="font-weight: bold; color: green; margin-left: 250px">
          WHAT TO WATCH
        </h2></b-navbar-brand
      >
      <div v-if="user" class="navbar-nav ml-auto">
        <b-navbar-nav class="navbar-nav ml-auto">
          <b-nav-item to="/home">Home</b-nav-item>
          <b-nav-item to="/search">Search</b-nav-item>
          <!--<b-nav-item to="social">Social</b-nav-item>!-->
          <b-nav-item-dropdown
            text="Social"
          >
            <b-dropdown-item style="background: black;"  to="/social">Events</b-dropdown-item>
            <b-dropdown-item style="background: black;"  to="/friend">Friends</b-dropdown-item>
          </b-nav-item-dropdown>
          <b-nav-item-dropdown
            style="margin-right: 200px"
            v-bind:text="user.attributes.name"
          >
            <b-dropdown-item style="background: black;"  to="/account">Preference</b-dropdown-item>
            <b-dropdown-item style="background: black;"  @click="logout">Logout</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </div>

      <div v-if="!user" class="navbar-nav ml-auto">
        <div class="navbar-nav ml-auto" style="margin-right: 200px">
          <b-nav-item to="/">Log In</b-nav-item>
          <b-nav-item to="/signup">Register</b-nav-item>
        </div>
      </div>
    </b-navbar>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  methods: {
    async logout() {
      await this.$store.dispatch("auth/logout");
      this.$router.push("/");
    },
  },
  computed: {
    ...mapGetters({
      user: "auth/user",
    }),
  },
};
</script>
<style lang="scss">

.navbar.navbar-dark.bg-dark {
  background-color: black !important;
}
.dropdown-menu.show {
    display: block;
    background-color:black !important;
        border: inset #fbfbfb;
}


.navbar-expand .navbar-nav .dropdown-menu {
    position: absolute;
    background: black;
    
}
.dropdown-item:hover{
    background-color: green;
 }

</style>