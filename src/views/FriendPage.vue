<template>
  <div id="moviesSocial" style="background-color: black">
    <b-row no-gutters>
      <b-col md="6" style="padding-left: 10%" :key="reloadFriends">
        <h1>Friends List</h1>
        <br />

        <div v-show="showLoading" id="loadingSocial">
          <Spinner />
        </div>
        <div class="container">
          <b-card-text>
            <ul class="list group">
              <li
                class="list-group-item d-flex justify-content-between align-items-center"
                id="rcorners2"
                v-for="friend in friendsList"
                :key="friend"
              >
                <h4>{{ friend.friendname }}</h4>
                <div>
                  <span class="badge badge-primary badge-pill">
                    {{ friend.friendid }}</span
                  >
                  <b-button
                    variant="danger"
                    style="margin: 10px"
                    class="btn-sm"
                    v-on:click="removeFriend(friend)"
                    >Remove</b-button
                  >
                </div>
              </li>
            </ul>
          </b-card-text>
        </div>
      </b-col>
      <b-col md="5">
        <div style="position: relative; left: 10%">
          <h1>Add Friends</h1>
          <br />
        </div>
        <div class="right-container">
          <b-form
            @submit="onSubmit"
            @reset="onReset"
            v-if="show"
            style="
              padding-top: 10px;
              padding-bottom: 20px;
              justify-content: center;
              align-items: center;
              padding-left: 20%;
            "
          >
            <b-form-group id="input-group-1" label-for="input-1">
              <b-form-input
                id="input-1"
                v-model="form.email"
                type="text"
                placeholder="Enter userid of friend"
                required
              ></b-form-input>
            </b-form-group>
            <b-button
              type="submit"
              variant="success"
              class="AddFriend"
              style="margin: 10px"
              >Add Friend</b-button
            >
            <!--<b-button type="reset" variant="danger" class="RemoveFriend" style="margin:10px">Remove</b-button>-->
          </b-form>
        </div>
      </b-col>
    </b-row>

    <b-modal
      ref="friend_added"
      centered
      hide-header
      hide-footer
      body-bg-variant="dark"
      body-text-variant="white"
      body-border-variant="dark"
    >
      <div class="d-block text-center" style="font-szie = 30px">
        New friend has been added.
      </div>
      <div class="d-block text-right">
        <b-button class="btn btn-success" @click="hideModal('friend_added')">
          Ok
        </b-button>
      </div>
    </b-modal>

    <b-modal
      ref="friend_removed"
      centered
      hide-header
      hide-footer
      body-bg-variant="dark"
      body-text-variant="white"
      body-border-variant="dark"
    >
      <div class="d-block text-center" style="font-szie = 30px">
        Friend has been removed.
      </div>
      <div class="d-block text-right">
        <b-button class="btn btn-success" @click="hideModal('friend_removed')">
          Ok
        </b-button>
      </div>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";
import Spinner from "@/components/Spinner";
import { Auth } from "aws-amplify";
import { mapGetters } from "vuex";
var config = require("../config.js");
export default {
  data() {
    return {
      selectedCard: -1,
      friendsList: [],
      showLoading: true,
      reloadFriends: 0,
      size: -1,
      form: {
        email: "",
      },
      show: true,
    };
  },
  mounted() {
    this.loadSocial();
  },
  components: {
    Spinner,
  },
  computed: {
    ...mapGetters({
      user: "auth/user",
    }),
  },
  methods: {
    showModal(name) {
      this.$refs[name].show();
    },
    hideModal(name) {
      this.$refs[name].hide();
    },

    onSubmit(event) {
      event.preventDefault();
      axios({
        method: "POST",
        url: config.api.invokeUrl + "/friend/add",
        headers: {
          Authorization: this.$store.state.auth.token,
        },
        data: {
          userid: this.$store.state.auth.user.username,
          friendid: this.form.email,
        },
      })
        .then((response) => {
          // handle success
          console.log(response["data"]);
          if (response["data"] == "Friend added successfully.") {
            this.showModal("friend_added");
          }
          // this.reloadFriends += 1;

          this.loadSocial();
        })
        .catch(function (error) {
          alert("Error Occurred");
          console.error("Error: ", error);
        });
    },

    onReset(event) {
      event.preventDefault();
      // Reset our form values
      axios({
        method: "POST",
        url: config.api.invokeUrl + "/friend/remove",
        headers: {
          Authorization: this.$store.state.auth.token,
        },
        data: {
          userid: this.$store.state.auth.user.username,
          friendid: this.form.email,
        },
      })
        .then((response) => {
          // handle success
          console.log(response["data"]);
        })
        .catch(function (error) {
          alert("Error Occurred");
          console.error("Error: ", error);
        });
      this.form.email = "";
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
    removeFriend(friend) {
      // Reset our form values
      axios({
        method: "POST",
        url: config.api.invokeUrl + "/friend/remove",
        headers: {
          Authorization: this.$store.state.auth.token,
        },
        data: {
          userid: this.$store.state.auth.user.username,
          friendid: friend.friendid,
        },
      })
        .then((response) => {
          // handle success
          console.log(response["data"]);
          if (
            response["data"] == "Removed friend from friendlist successfully"
          ) {
            this.showModal("friend_removed");
          }
          this.loadSocial();
        })
        .catch(function (error) {
          alert("Error Occurred");
          console.error("Error: ", error);
        });
    },

    async loadSocial() {
      this.showLoading = true;
      await Auth.currentSession().then((data) =>
        axios({
          method: "GET",
          url: config.api.invokeUrl + "/friend",
          headers: {
            Authorization: data.idToken.jwtToken,
          },
          params: {
            userid: this.$store.state.auth.user.username,
          },
        })
          .then((response) => {
            console.log(response["data"]["friend_list"]);
            // handle success
            this.friendsList = response["data"]["friend_list"];
            this.size = this.friendsList.length;
            this.showLoading = false;
          })
          .catch(function (error) {
            // handle error
            console.error("Error: ", error);
          })
      );
    },
  },
};
</script>
<style lang="scss" scoped>
.moviesSocial {
  position: relative;
  left: 10px;
  right: 10px;
  top: 100%;
  justify-content: center;
  width: 70%;
  align-items: center;
}

#rcorners2 {
  border-radius: 8px;
  border: 2px solid;
  color: green;
  background: #e4f5e4;
}

h1 {
  align-items: center;
  color: #cacaca;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 10px;
  margin-top: 15px;
  display: flex;
  justify-content: center;
}
h4 {
  align-items: center;
  color: #302f2f;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
  margin-top: 15px;
  display: flex;
  justify-content: center;
}
</style>