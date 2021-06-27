<template>
  <div class="container">
    <div class="row">
      <aside class="col-sm-5" style="margin: auto">
        <div class="card">
          <article class="card-body">
            <h4 class="card-title text-center mb-4 mt-1">Preference</h4>
            <div style="display: flex">
              <div style="margin-right: 10px; font-weight: bold">Username:</div>

              <p style="margin-right: 5px">
                {{ user.username }}
              </p>
            </div>
            <div style="display: flex">
              <div style="margin-right: 10px; font-weight: bold">Name:</div>

              <p style="margin-right: 5px">
                {{ user.attributes.name }}
              </p>
              
            </div>
             <div style="display: flex">
              <div style="margin-right: 10px; font-weight: bold">Email:</div>

              <p style="margin-right: 5px">
                {{ user.attributes.email }}
              </p>
              
            </div>

            <div v-if="!isEditing" style="display: flex">
              <div style="margin-right: 10px; font-weight: bold">Genre(s):</div>

              <p style="margin-right: 5px" v-for="item in selected" :key="item">
                {{ item }};
              </p>
            </div>
            <div v-if="isEditing" style="display: flex">
              <div style="margin-right: 10px; font-weight: bold">Genre(s):</div>
              <multiselect
                id="sel"
                v-model="selected"
                :multiple="true"
                :options="options"
              >
              </multiselect>
            </div>
            <b-card-footer>
              <b-button
                variant="success"
                @click="isEditing = !isEditing"
                v-if="!isEditing"
              >
                Edit
              </b-button>
              <b-button variant="success" @click="save" v-else-if="isEditing">
                Save
              </b-button>

              <b-button
                variant="secondary"
                style="margin-left: 10px"
                v-if="isEditing"
                @click="isEditing = false"
              >
                Cancel
              </b-button>
            </b-card-footer>
          </article>
        </div>
      </aside>
    </div>
  </div>
</template>

<script>
import Multiselect from "vue-multiselect";
import axios from "axios";
import { Auth } from "aws-amplify";
import { mapGetters } from "vuex";
var config = require("../config.js");

export default {
  components: { Multiselect },
  data() {
    return {
      payload: {},
      isEditing: false,
      selected: null,
      options: ["Action", "Adventure", "Animation", "Comedy", "Drama", "Fantasy", "Family", "Horror", "Kids", "Mystery", "Romance", "Science Fiction", "Thriller" ],
    };
  },
  mounted() {
    this.load();
  },
  methods: {
    save() {
      console.log(this.$store.state.auth.user);
      this.payload = {
        genre: this.selected,
        userid: this.$store.state.auth.user.username,
      };
      this.isEditing = !this.isEditing;
      axios({
        method: "POST",
        url: config.api.invokeUrl + "/account/update",
        headers: {
          Authorization: this.$store.state.auth.token,
          "Content-Type": "application/json",
        },
        data: this.payload,
      })
        .then((response) => {
          // handle success
          console.log(response["data"]);
        })
        .catch(function (error) {
          // handle error
          console.error("Error: ", error);
        });
    },
    async load() {
      await Auth.currentSession().then((data) =>
        axios({
          method: "GET",
          url: config.api.invokeUrl + "/account",
          headers: {
            Authorization: data.idToken.jwtToken,
          },
          params: {
            userid: this.$store.state.auth.user.username,
          },
        })
          .then((response) => {
            // handle success
            this.selected = response["data"];
            console.log(this.selected);
          })
          .catch(function (error) {
            // handle error
            console.error("Error: ", error);
          })
      );
    },
  },
  computed: {
    ...mapGetters({
      user: "auth/user",
    }),
  },
};
</script>

     
<style src="vue-multiselect/dist/vue-multiselect.min.css">
</style>
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
  border-radius: 0.25rem;
}
</style>