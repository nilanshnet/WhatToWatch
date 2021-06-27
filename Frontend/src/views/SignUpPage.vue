<template>
  <div>
    <div class="container">
      <div class="row">
        <aside class="col-sm-8" style="margin: auto">
          <div class="card">
            <article class="card-body">
              <h4 class="card-title text-center mb-4 mt-1">
                Create New Account
              </h4>
              <hr />
              <form
                v-if="!confirmPassword"
                class="flex flex-col items-center"
                @submit.prevent="signUp"
              >
            <div v-if="error" class="alert alert-danger">{{ error.message }}</div>
                <div class="form-group">
                  <input
                    class="form-control form-control-lg"
                    type="text"
                    v-model="username"
                    id="username"
                     placeholder="Username"
                    required
                  />
                </div>
                <div class="form-group">
                   <input
                    class="form-control form-control-lg"
                    type="text"
                    id="name"
                    v-model="name"
                    placeholder="Full Name"
                    required
                  />
                </div>
                <div class="form-group">

                  <input
                    class="form-control form-control-lg"
                    type="email"
                    id="email"
                    v-model="email"
                    placeholder="Email"                    
                    required
                  />
                </div>
                <div class="form-group">
                  <input
                    class="form-control form-control-lg"
                    type="password"
                    id="password"
                    v-model="password"
                    placeholder="Password"                    
                    required
                  />
                </div>
                <button class="btn btn-success">Sign Up</button>
              </form>


    

              <form v-if="confirmPassword"
                class="flex flex-col items-center"
                @submit.prevent="confirmSignUp"
              >
              <div v-if="confirmError" class="alert alert-danger">{{ confirmError.message }}</div>
                <div class="form-group">
                  <label
                    class="block text-gray-700 text-sm font-bold mb-2"
                    for="username"> Please check your email and enter the verification
                    code</label>
                  <input
                    class="form-control form-control-lg"
                    type="text"
                    v-model="code"
                    required
                  />
                </div>
                <button class="btn btn-primary">Confirm Code</button>
              </form>
            </article>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    username: "",
    name: "",
    password: "",
    email: "",
    error: "",
    confirmPassword: "",
    code: "",
    confirmError: "",
  }),

  methods: {
    async signUp() {
      try {
        await this.$store.dispatch("auth/signUp", {
          username: this.username,
          name: this.name,
          password: this.password,
          email: this.email,
        });
        this.confirmPassword = true;
      } catch (e) {
        console.log("here");
        console.log(e);
        if (e['name'] == "UserLambdaValidationException"){
          e['message'] = e['message'].slice(28);
        }
        if (e['name'] == "UsernameExistsException"){
          e['message'] = "Username already taken. Please enter a new Username.";
        }
        console.log(e);
        this.error = e;
      }
    },
    async confirmSignUp() {
        try {
          const { username, password, code } = this;
          await this.$store.dispatch("auth/confirmSignUp", {
            username,
            code,
          });
          await this.$store.dispatch("auth/login", {
            username,
            password,
          });
          this.$router.push("/home");
        } catch (e) {
          this.confirmError = e;
          console.log(e);
        }

      }
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