<template>
  <div>
    <div id="newMovies"
>
      <div id="slide">
        <h1>Watching Now</h1>
        <div v-show="showLoading" id="loadingMovie">
          <Spinner />
        </div>
        <carousel
          class="carousel"
          :per-page="6"
          :navigate-to="0"
          :mouse-drag="false"
          :paginationEnabled="false"
          :navigationEnabled="true"
          :navigationClickTargetSize="6"
          v-if="watchlistNow.length > 0"
        >
          <slide v-for="(item_now, index) in watchlistNow" :key="index">
            <div
              class="card"
              :ref="`card_${index}`"
              @mouseover="hoverCard(index, 'now')"
              @mouseout="hoverCard(-1, '')"
            >
              <img
                class="card-image"
                :src="item_now.poster_path"
                :class="{ selected: isSelected(index, 'now') }"
              />
              <div
                v-if="item_now.type == 'tv'"
                class="card-header"
                :class="{ selected: isSelected(index, 'now') }"
              >
                {{ "S" + item_now.season + "E" + item_now.episode }}
              </div>
              <!-- <h3 class="card-title" :class="{ selected: isSelected(index) }">
                {{ item.title }}
              </h3> -->
              <div
                class="card-text"
                :class="{ selected: isSelected(index, 'now') }"
              >
                <div class="card-watchlist">
                  <b-button
                    variant="success"
                    style="margin-bottom: 60px; margin-top: 30px"
                    v-b-tooltip.hover
                    title="Mark as Watched"
                    @click="doneNow(item_now)"
                  >
                    Watched
                  </b-button>

                  <b-button
                    variant="success"
                    v-b-tooltip.hover
                    title="Not Interested?"
                    @click="removeNow(item_now.id)"
                  >
                    - Stop Watching
                  </b-button>
                </div>
              </div>
            </div>
          </slide>
        </carousel>

        <div  id ="empty" v-if="this.load == true && watchlistNow.length == 0">
          <div style="padding:6px">You Currently Donot Have Anything To Watch </div>
        </div>
      </div>
    </div>
    <div id="newMovies">
      <div id="slide">
        <h1>Watchlist Movies</h1>
        <div v-show="showLoading" id="loadingMovie">
          <Spinner />
        </div>
        <carousel
          v-if="this.load == true && watchlistMovie.length > 0"
          :per-page="6"
          :navigate-to="0"
          :mouse-drag="false"
          :paginationEnabled="false"
          :navigationEnabled="true"
          :navigationClickTargetSize="6"
        >
          <slide :key="index" v-for="(item_mv, index) in watchlistMovie">
            <div
              class="card"
              :ref="`card_${index}`"
              @mouseover="hoverCard(index, 'mv')"
              @mouseout="hoverCard(-1, '')"
            >
              <img
                class="card-image"
                :src="item_mv.poster_path"
                :class="{ selected: isSelected(index) }"
              />
              <!-- <h3 class="card-title" :class="{ selected: isSelected(index) }">
                {{ item.title }}
              </h3> -->
              <div
                class="card-text"
                :class="{ selected: isSelected(index, 'mv') }"
              >
                <div class="card-watchlist">
                  <b-button
                    variant="success"
                    style="margin-bottom: 60px; margin-top: 30px"
                    v-b-tooltip.hover
                    title="Start Watching"
                    @click="
                      addNow(item_mv.id, item_mv.poster_path, item_mv.type)
                    "
                  >
                    + Watch Now
                  </b-button>

                  <b-button
                    variant="success"
                    v-b-tooltip.hover
                    title="Not Interested? Remove from Watchlist"
                    @click="removeList(item_mv.id)"
                  >
                    - Watchlist
                  </b-button>
                </div>
              </div>
            </div>
          </slide>
        </carousel>
        <div  id ="empty" v-if="this.load == true && watchlistMovie.length == 0" >
          <div style="padding:6px">Add Some Movies To Your Watchlist</div>
          <b-button class="btn btn-secondary" to="/search"> + </b-button>
        </div>
      </div>
    </div>
    <div id="newMovies">
      <div id="slide">
        <h1>Watchlist TV</h1>
        <div v-show="showLoading" id="loadingMovie">
          <Spinner />
        </div>
        <carousel
          :per-page="6"
          :navigate-to="0"
          :mouse-drag="false"
          :paginationEnabled="false"
          :navigationEnabled="true"
          :navigationClickTargetSize="6"
        >
          <slide :key="index" v-for="(item, index) in watchlistTV">
            <div
              class="card"
              :ref="`card_${index}`"
              @mouseover="hoverCard(index, 'tv')"
              @mouseout="hoverCard(-1, '')"
            >
              <img
                class="card-image"
                :src="item.poster_path"
                :class="{ selected: isSelected(index) }"
              />
              <!-- <h3 class="card-title" :class="{ selected: isSelected(index) }">
                {{ item.title }}
              </h3> -->
              <div
                class="card-text"
                :class="{ selected: isSelected(index, 'tv') }"
              >
                <div class="card-watchlist">
                  <b-button
                    variant="success"
                    style="margin-bottom: 60px; margin-top: 30px"
                    v-b-tooltip.hover
                    title="Start Watching"
                    @click="addNow(item.id, item.poster_path, item.type)"
                  >
                    + Watch Now
                  </b-button>

                  <b-button
                    variant="success"
                    v-b-tooltip.hover
                    title="Not Interested? Remove from Watchlist"
                    @click="removeList(item.id)"
                  >
                    - Watchlist
                  </b-button>
                </div>
              </div>
            </div>
          </slide>
        </carousel>

        <div  id ="empty" v-if="this.load == true && watchlistTV.length == 0">
          <div style="padding:6px">Add Some TV Shows To Your Watchlist</div>
          <b-button class="btn btn-secondary" to="/search"> + </b-button>
        </div>
      </div>
    </div>
    <b-modal
      ref="rating-tv"
      centered
      hide-header
      hide-footer
      body-bg-variant="dark"
      body-text-variant="white"
      body-border-variant="dark"
    >
      <div class="d-block text-center" style="font-szie = 20px">
        How would you rate this episode of the TV Show?
      </div>
      <div
        class="d-block text-center"
        style=" margin-top:10px; margion-bottom:10px; font-szie = 20px"
      >
        <b-input-group>
          <b-form-rating v-model="value" color="green"></b-form-rating>
        </b-input-group>
      </div>
      <div class="d-block text-right">
        <b-button class="btn btn-success" @click="addRating(rated_item, value)">
          Ok
        </b-button>
      </div>
    </b-modal>
    <b-modal
      ref="rating-mv"
      centered
      hide-header
      hide-footer
      body-bg-variant="dark"
      body-text-variant="white"
      body-border-variant="dark"
    >
      <div class="d-block text-center" style="font-szie = 20px">
        How would you rate the Movie?
      </div>
      <div class="d-block text-center" style="font-szie = 20px">
        <b-input-group>
          <b-form-rating v-model="value" color="green"></b-form-rating>
        </b-input-group>
      </div>
      <div class="d-block text-right">
        <b-button class="btn btn-success" @click="addRating(rated_item, value)">
          Ok
        </b-button>
      </div>
    </b-modal>
  </div>
</template>

<script>
import { Carousel, Slide } from "vue-carousel";
import Spinner from "@/components/Spinner";
import axios from "axios";
import { Auth } from "aws-amplify";
import { mapGetters } from "vuex";
var config = require("../config.js");

export default {
  name: "Titles",

  data() {
    return {
      load: false,
      value: null,
      rated_item: [],
      selectedCard: -1,
      selectedCat: "",
      watchlistNow: [],
      watchlistTV: [],
      watchlistMovie: [],
      showLoading: true,
    };
  },
  components: {
    Carousel,
    Slide,
    Spinner,
  },
  mounted() {
    this.loadHome();
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
    hoverCard(selectedIndex, category) {
      this.selectedCard = selectedIndex;
      this.selectedCat = category;
    },
    isSelected(cardIndex, category) {
      return this.selectedCard === cardIndex && this.selectedCat == category;
    },

    async loadHome() {
      this.showLoading = true;
      await Auth.currentSession().then((data) =>
        axios({
          method: "GET",
          url: config.api.invokeUrl + "/watch",
          headers: {
            Authorization: data.idToken.jwtToken,
          },
          params: {
            userid: this.$store.state.auth.user.username,
          },
        })
          .then((response) => {
            // handle success
            this.watchlistNow = response["data"]["watchnow"];
            this.watchlistTV = response["data"]["watchlisttv"];
            this.watchlistMovie = response["data"]["watchlistmovie"];
            this.load = true;
            this.showLoading = false;
          })
          .catch(function (error) {
            // handle error
            console.error("Error: ", error);
          })
      );
    },
    addNow(id, poster, type) {
      axios({
        method: "POST",
        url: config.api.invokeUrl + "/watch/addnow",
        headers: {
          Authorization: this.$store.state.auth.token,
        },
        data: {
          userid: this.$store.state.auth.user.username,
          name: this.$store.state.auth.user.attributes.name,
          id: id,
          poster_path: poster,
          type: type,
        },
      })
        .then((response) => {
          // handle success
          console.log(response["data"]);
          this.loadHome();
        })
        .catch(function (error) {
          // handle error
          console.error("Error: ", error);
        });
    },
    getDate() {
      var today = new Date();
      var date =
        today.getFullYear() +
        "-" +
        ("0" + today.getDate()).slice(-2) +
        "-" +
        ("0" + (today.getMonth() + 1)).slice(-2);
      return date;
    },

    addRating(item, rating) {
      console.log(rating);
      var date = this.getDate();
      axios({
        method: "POST",
        url: config.api.invokeUrl + "/rating",
        headers: {
          Authorization: this.$store.state.auth.token,
        },
        data: {
          userid: this.$store.state.auth.user.username,
          session_id:
            String(date) + String(this.$store.state.auth.user.username),
          item_id: item.id,
          rating: rating,
        },
      })
        .then((response) => {
          console.log(response["data"]);
          // handle success
          if (response && item.type == "tv") {
            this.hideModal("rating-tv");
          }
          if (response && item.type == "movie") {
            this.hideModal("rating-mv");
          }
          this.value = "";
          this.loadHome();
        })
        .catch(function (error) {
          // handle error
          console.error("Error: ", error);
          if (item.type == "tv") {
            this.hideModal("rating-tv");
          }
          if (item.type == "movie") {
            this.hideModal("rating-mv");
            this.value = "";
          }
        });
    },

    removeNow(id) {
      axios({
        method: "POST",
        url: config.api.invokeUrl + "/watch/removenow",
        headers: {
          Authorization: this.$store.state.auth.token,
        },
        data: {
          userid: this.$store.state.auth.user.username,
          id: id,
        },
      })
        .then((response) => {
          // handle success
          console.log(response["data"]);
          this.loadHome();
        })
        .catch(function (error) {
          // handle error
          console.error("Error: ", error);
        });
    },

    removeList(id) {
      axios({
        method: "POST",
        url: config.api.invokeUrl + "/watch/removelist",
        headers: {
          Authorization: this.$store.state.auth.token,
        },
        data: {
          userid: this.$store.state.auth.user.username,
          id: id,
        },
      })
        .then((response) => {
          // handle success
          console.log(response["data"]);
          this.loadHome();
        })
        .catch(function (error) {
          // handle error
          console.error("Error: ", error);
        });
    },

    doneNow(item) {
      this.rated_item = item;
      console.log(this.rated_item);
      axios({
        method: "POST",
        url: config.api.invokeUrl + "/watch/donenow",
        headers: {
          Authorization: this.$store.state.auth.token,
        },
        data: {
          userid: this.$store.state.auth.user.username,
          id: item.id,
          episode: item.episode,
          season: item.season,
        },
      })
        .then((response) => {
          if (response && item.type == "tv") {
            this.showModal("rating-tv");
          }
          if (response && item.type == "movie") {
            this.showModal("rating-mv");
          }
          console.log(response["data"]);
        })
        .catch(function (error) {
          // handle error
          console.error("Error: ", error);
        });
    },
  },
};
</script>
<style lang="scss" scoped>
#empty{
    display: flex;
    justify-content: center;
    padding: 100px
}
#slide {
  width: 95%;
  height: 100%;
  text-align: center;
  margin: auto;
}
#newMovies {
  width: 96%;
  height: 100%;
  text-align: center;
  margin:auto,
  // padding: 20px;
}
#buttonNexts {
  color: #f1f;
}
#newMovies h1 {
  color: #cacaca;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 10px;
  margin-top: 15px;
  padding-left: 20px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
}
#loadingMovie {
  display: flex;
  justify-content: center;
  align-items: center;
}
#movieDiv {
  margin-top: 23px;
  padding-left: 20px;
  flex: 1;
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
.card-header {
  position: absolute;
  padding: 6px;
  background-color: rgb(91, 172, 91);
  right: 0;
  border-radius: 10px;
  color: white;
  opacity: 0.8;
}
.card-header.selected {
  opacity: 0.3;
  position: absolute;
  padding: 6px;
  background-color: rgb(91, 172, 91);
  right: 0;
  border-radius: 10px;
  color: white;
}
.card {
  /* the other rules */
  transition: height 0.3s, box-shadow 0.3s;
}
.form-control {
  display: block;
  width: 100%;
  height: calc(1.5em + 0.75rem + 2px);
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
  color: #495057;
  background-color: #343a40;
  background-clip: padding-box;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  border: none;
}
</style>

<style >
.VueCarousel-navigation-button {
  color: green !important;
  outline: none !important;
}
</style>
