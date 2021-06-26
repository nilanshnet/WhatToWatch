<template>
  <div>
    <div id="moviesSocial">
      <h1>Friends Are Watching </h1>
      <div id="slide">
      <div v-show="showLoading" id="loadingSocial">
        <Spinner />
      </div>
      <div v-if="size == 0" class="container">
        Add more friends to see what they are watching
      </div>


               <carousel
                :per-page="6"
                :navigate-to="0"
                :mouse-drag="false"
                :paginationEnabled="false"
                :navigationEnabled="true"
                :navigationClickTargetSize="6"
              >
                <slide v-for="(item, index) in friendsWatching" :key="index">
                  <div
                    class="card"
                    :ref="`card_${index}`"
                    @mouseover="hoverCard(index)"
                    @mouseout="hoverCard(-1)"
                  >
                    <img
                      class="card-image"
                      :src="item.poster_path"
                      :class="{ selected: isSelected(index, 'ml_rec') }"
                    />
                    <img
                      class="card-image"
                      :class="{ selected: isSelected(index) }"
                      :src="item.poster_path"
                    />
                    <h4 class="card-title" :class="{ selected: isSelected(index) }">
                      {{ item.name }}
                    </h4>
                  </div>
                </slide>
              </carousel>
      </div>
    </div>

    <b-modal
      ref="event_declined"
      centered
      hide-header
      hide-footer
      body-bg-variant="dark"
      body-text-variant="white"
      body-border-variant="dark"
    >
      <div class="d-block text-center" style="font-szie = 30px">
        Event has been declined
      </div>
      <div class="d-block text-right">
        <b-button class="btn btn-success" @click="hideModal('event_declined')">
          Ok
        </b-button>
      </div>
    </b-modal>

    <b-modal
      ref="event_created"
      centered
      hide-header
      hide-footer
      body-bg-variant="dark"
      body-text-variant="white"
      body-border-variant="dark"
    >
      <div class="d-block text-center" style="font-szie = 30px">
        Your event has been created and invites have been sent out.
      </div>
      <div class="d-block text-right">
        <b-button class="btn btn-success" @click="hideModal('event_created')">
          Ok
        </b-button>
      </div>
    </b-modal>
    <b-modal
      ref="event_accepted"
      centered
      hide-header
      hide-footer
      body-bg-variant="dark"
      body-text-variant="white"
      body-border-variant="dark"
    >
      <div class="d-block text-center" style="font-szie = 30px">
        Event has been accepted
      </div>
      <div class="d-block text-right">
        <b-button class="btn btn-success" @click="hideModal('event_accepted')">
          Ok
        </b-button>
      </div>
    </b-modal>

    <div id="eventsSection" style="padding-top: 4%; align-items: center">
      <b-row no-gutters>
        <b-col md="5" style="margin-left: 8%">
          <h1>Pending Events</h1>
          <br />
          <div v-if="sizePendingEvents == 0">There are no pending events</div>
          <ul class="list group">
            <li
              id="rcorners2"
              v-for="event in pendingEvents"
              :key="event"
              class="list-group-item d-flex justify-content-between align-items-start"
            >
              <div class="ms-2 me-auto">
                <div>
                  <h5>{{ event.description }}</h5>
                </div>
                <h6>
                  by <br />
                  {{ event.creator }} at '{{ event.time }}'
                </h6>
              </div>
              <div class="btn-group-vertical">
                <button
                  type="button"
                  class="btn btn-success"
                  v-on:click="eventAccept(event)"
                >
                  Accept
                </button>
                <button
                  type="button"
                  class="btn btn-danger"
                  v-on:click="eventReject(event)"
                >
                  Decline
                </button>
              </div>
            </li>
          </ul>
        </b-col>
        <b-col md="5">
          <h1>Confirmed Events</h1>
          <br />

          <div v-if="sizeConfirmedEvents == 0">
            <div>There are no confirmed events</div>
          </div>
          <ul class="list group">
            <li
              id="rcorners2"
              v-for="event in confirmedEvents"
              :key="event"
              class="list-group-item d-flex justify-content-between align-items-start"
            >
              <div class="ms-2 me-auto">
                <div>
                  <h5>{{ event.description }}</h5>
                </div>
                <h6>
                  by <br />
                  {{ event.creator }} at '{{ event.time }}'
                </h6>
              </div>
              <div class="btn-group-vertical">
                <a :href="event.url" class="btn btn-success">Join</a>
                <button
                  type="button"
                  class="btn btn-danger"
                  v-on:click="eventReject(event)"
                >
                  Decline
                </button>
              </div>
            </li>
          </ul>
        </b-col>
      </b-row>
    </div>
    <div id="createWatchParty" style="padding-top: 3%">
      <h1>Create Watch Party</h1>
      <br />
      <div class="CreateWP">
        <b-form
          @submit="onSubmit"
          @reset="onReset"
          style="
            padding-top: 10px;
            padding-bottom: 20px;
            justify-content: center;
            align-items: center;
          "
        >
          <label for="watch-party-name">Title</label><br />
          <input required
            style="
              padding: 7px;
              width: 20%;
              align: center;
              box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.5);
            "
            v-model="form.description"
          />
          <b-form-text style="padding-bottom: 20px"> </b-form-text>

          <label for="watch-party-time">Date & Time</label><br />
          <input required
            style="
              padding: 7px;
              width: 20%;
              align: center;
              box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.5);
            "
            v-model="form.time"
          />
          <b-form-text style="padding-bottom: 20px"> </b-form-text>

          <label for="watch-party-emails">Email(s)</label><br />
          <input required
            style="
              padding: 7px;
              width: 20%;
              align: center;
              box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.5);
            "
            v-model="form.inviteList"
          />
          <b-form-text style="padding-bottom: 20px"> </b-form-text>

          <label for="watch-party-time">Invitation Link</label><br />
          <input required
            style="
              padding: 7px;
              width: 20%;
              align: center;
              box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.5);
            "
            v-model="form.inviteUrl"
          />
          <b-form-text style="padding-bottom: 20px"> </b-form-text>

          <b-button type="submit" variant="success" style="margin: 10px"
            >Submit</b-button
          >
          <b-button type="reset" variant="danger" style="margin: 10px"
            >Reset</b-button
          >
        </b-form>
      </div>
    </div>
  </div>
</template>

<script>
import { Carousel, Slide } from "vue-carousel";
import axios from "axios";
import Spinner from "@/components/Spinner";
import { Auth } from "aws-amplify";
import { mapGetters } from "vuex";
var config = require("../config.js");

export default {
  name: "app",
  data() {
    return {
      friendsWatching: [],
      confirmedEvents: [],
      pendingEvents: [],
      sizeConfirmedEvents: -1,
      sizePendingEvents: -1,
      selectedCard: -1,
      result: [],
      showLoading: true,
      size: -1,
      form: {
        description: "",
        time: "",
        inviteList: "",
        inviteUrl: "",
      },
    };
  },
  mounted() {
    this.loadSocial("");
  },
  components: {
    Carousel,
    Slide,
    Spinner,
  },
  computed: {
    ...mapGetters({
      user: "auth/user",
    }),
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();
      axios({
        method: "POST",
        url: config.api.invokeUrl + "/social/eventcreate",
        headers: {
          Authorization: this.$store.state.auth.token,
        },
        data: {
          creator: this.$store.state.auth.user.attributes.email,
          description: this.form.description,
          invitee: this.form.inviteList,
          time: this.form.time,
          url: this.form.inviteUrl,
        },
      })
        .then((response) => {
          // handle success
          console.log(response["data"]);
          if (response["data"] == "Event created successfully") {
                      this.showModal("event_created");
                    }
          this.form.description = "";
          this.form.time = "";
          this.form.inviteList = "";
          this.form.inviteUrl = "";
          this.loadSocial("")
        })
        .catch(function (error) {
          alert("Error Occurred");
          console.error("Error: ", error);
        });
    },
    onReset(event) {
      event.preventDefault();
      this.form.description = "";
      this.form.time = "";
      this.form.inviteList = "";
      this.form.inviteUrl = "";
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
    eventAccept: function (event) {
      axios({
        method: "POST",
        url: config.api.invokeUrl + "/social/eventstatus",
        headers: {
          Authorization: this.$store.state.auth.token,
        },
        data: {
          eventid: event.eventid,
          status: "accepted",
        },
      })
        .then((response) => {
          // handle success
          console.log(response["data"]);
          if (response["data"] == "Event updated successfully.") {
            this.showModal("event_accepted");
          }
          this.loadSocial("");
        })
        .catch(function (error) {
          // handle error
          alert("Error Occurred");
          console.error("Error: ", error);
        });
    },
    eventReject: function (event) {
      axios({
        method: "POST",
        url: config.api.invokeUrl + "/social/eventstatus",
        headers: {
          Authorization: this.$store.state.auth.token,
        },
        data: {
          eventid: event.eventid,
          status: "rejected",
        },
      })
        .then((response) => {
          // handle success
          console.log(response["data"]);
          if (response["data"] == "Event updated successfully.") {
            this.showModal("event_declined");
          }
          this.loadSocial("");
        })
        .catch(function (error) {
          // handle error
          console.error("Error: ", error);
        });
    },

    hoverCard(selectedIndex) {
      this.selectedCard = selectedIndex;
    },
    isSelected(cardIndex) {
      return this.selectedCard === cardIndex;
    },
    async loadSocial(caller) {
      this.showLoading = true;
      await Auth.currentSession().then((data) =>
        axios({
          method: "GET",
          url: config.api.invokeUrl + "/social",
          headers: {
            Authorization: data.idToken.jwtToken,
          },
          params: {
            userid: this.$store.state.auth.user.username,
            useremail: this.$store.state.auth.user.attributes.email,
          },
        })
          .then((response) => {
            console.log(response);
            // handle success
            this.friendsWatching = response["data"]["friend_watchlist"];
            this.pendingEvents = response["data"]["pending_events"];
            this.confirmedEvents = response["data"]["confirmed_events"];
            this.size = this.friendsWatching.length;
            this.sizePendingEvents = this.pendingEvents.length;
            this.sizeConfirmedEvents = this.confirmedEvents.length;
            this.showLoading = false;
            if (caller == "api") {
              console.log("here");
              location.reload();
            }
          })
          .catch(function (error) {
            // handle error
            console.error("Error: ", error);
          })
      );
    },
    showModal(name) {
      this.$refs[name].show();
    },
    hideModal(name) {
      this.$refs[name].hide();
    },
  },
};
</script>

<style lang="scss" scoped>
#moviesSocial {
  width: 96%;
  height: 100%;
  text-align: center;
  margin: auto;
}
#loadingSocial {
  display: flex;

  align-items: center;
}

#slide {
  width: 95%;
  height: 100%;
  text-align: center;
  margin: auto;
}

#buttonNexts {
  color: #f1f;
}

#movieDiv {
  margin-top: 23px;
  padding-left: 20px;
  flex: 1;
}

.VueCarousel-navigation-button {
                position: relative;
}

#rcorners2 {
  border-radius: 8px;
  border: 2px solid;
  color: green;
  text-align: center;
  background: #e4f5e4
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

h5 {
  align-items: left;
  color: #0f0f0f;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 20px;
  font-weight: bold;
  display: flex;
  justify-content: center;
}

h6 {
  align-items: left;
  color: #0f0f0f;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 16px;
  margin-bottom: 10px;
  display: flex;
  justify-content: center;
}

#moviesSocial card-row {
  display: flex;
  justify-content: center;
  align-items: center;
  min-width: 780px;
  width: 100%;
  height: 500px;
}

.card {
  position: relative;
  background-color: #ffffff;
  height: 300px;
  width: 200px;
  margin: 10px;
  overflow: hidden;
  box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.5);
}

.card-image {
  /* center horizontally overflown image */
  position: absolute;
  left: -9999px;
  right: -9999px;
  margin: auto;
  height: 300px;
  min-width: 100%;
  transition: height 0.3s, opacity 0.3s;
}
.card-image.selected {
  opacity: 0.3;
  height: 300px;
}

.card-footer {
  position: absolute;
  bottom: 0;
  height: 130px;
  padding: 10px 15px;
  font-family: Helvetica;
}
.card-text {
  margin-top: 3rem;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.7);
}
.card-title {
  margin-top: 2rem;
  font-weight: bold;
  margin-top: 30px;
  color: black;
}
.card-title.selected {
  margin-top: 2rem;
  font-weight: bold;
  margin-top: 30px;
  color: black;
  z-index: 2;
}
.card-watchlist {
  font-weight: bold;
  font-size: 20px;
  color: #050505;
  transition: color 0.3s;
}
.card-text.selected {
  margin-top: 3rem;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.7);
  z-index: 2;
}
.card {
  /* the other rules */
  transition: height 0.3s, box-shadow 0.3s;
}

.rowoftiles {
  display: flex;
  justify-content: center;
  align-items: center;
  min-width: 780px;
  width: 100%;
  height: 500px;
  margin-top: 0%;
}

.watch-party {
  position: relative;
  margin: 30px;
  padding-top: 100px;
  left: 260px;
  right: 10px;
  justify-content: center;
  width: 70%;
  align-items: center;
  background-color: black;
  text-decoration-color: black;
  box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.5);
}

.CreateWP {
  left: 10px;
  right: 10px;
  top: 100%;
}
v:deep .my-second-class > .modal-dialog > .modal-content > .modal-header {
  background: black;
  color: white;
}
</style>

<style >
.VueCarousel-navigation-button {
  color: green !important;
  outline: none !important;
}
</style>