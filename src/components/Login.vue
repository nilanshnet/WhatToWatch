<template>
  <div class="container">
    <div class="row">
      <aside class="col-sm-5" style="margin: auto">
        <div class="card">
          <article class="card-body">
            <h4 class="card-title text-center mb-4 mt-1">Sign in</h4>
            <hr />
          <div v-if="error" >
            <b-alert show dismissible variant="danger">
              {{ error.message }}
            </b-alert>
          </div>

            <form class="flex flex-col items-center" @submit.prevent="login">
              <div class="form-group">
                <!-- <label>Username</label> -->
                <input
                  class="form-control form-control-lg"
                  type="text"
                  v-model="username"
                  id="username"
                  placeholder="Username"
                  reqiured
                />
              </div>
              <div class="form-group">
                <!-- <label>Password</label> -->
                <input
                  class="form-control form-control-lg"
                  type="password"
                  v-model="password"
                  placeholder="Password"
                  autocomplete="on"
                  required
                />
              </div>
              <br>
              <div class="form-group">
                <button class="btn btn-success">Sign In</button>
              </div>
            </form>
              <div class="form-group">
                <b-button variant="success"
                  type="submit"
                  to="/signup"
                >Create New Account?
                </b-button>
              </div>
          </article>
        </div>
      </aside>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
export default {
  data: () => ({
    username: "",
    password: "",
    error: "",
  }),
  methods: {
    ...mapActions({
      loginVue: "auth/login",
    }),
    async login() {
      try {
        await this.loginVue({
          username: this.username,
          password: this.password,
        });
        this.$router.push("/home");
      } catch (error) {
        this.error = error;
      }
    },
  },
};
</script>

<style lang="scss" scoped>

.card {
    position: relative;
    display: flex;
    flex-direction: column;
    min-width: 0;
    word-wrap: break-word;
    background-color: black;
    background-clip: border-box;
    border: 1px solid white;
    border-radius: .25rem;
}

</style>