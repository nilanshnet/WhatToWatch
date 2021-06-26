<template>
  <div>
    <b-modal
        ref="success"
        centered
        hide-header
        hide-footer
        body-bg-variant="dark"
        body-text-variant="white"
        body-border-variant="dark"
        >
        <div class="d-block text-center" style="font-szie = 20px">
            Title has been added to your Watchlist
        </div>
        <div class="d-block text-right">
            <b-button class="btn btn-success" @click="hideModal('success')">
            Ok
            </b-button>
        </div>
        </b-modal>

        <b-modal
        ref="exists_watchlist"
        centered
        hide-header
        hide-footer
        body-bg-variant="dark"
        body-text-variant="white"
        body-border-variant="dark"
        >
        <div class="d-block text-center" style="font-szie = 30px">
            Title is already in your Watchlist
        </div>
        <div class="d-block text-right">
            <b-button class="btn btn-success" @click="hideModal('exists_watchlist')">
            Ok
            </b-button>
        </div>
    </b-modal>
    <b-modal
        ref="exists_watchnow"
        centered
        hide-header
        hide-footer
        body-bg-variant="dark"
        body-text-variant="white"
        body-border-variant="dark"
        >
        <div class="d-block text-center" style="font-szie = 30px">
            Title is already being Watched
        </div>
        <div class="d-block text-right">
            <b-button class="btn btn-success" @click="hideModal('exists_watchnow')">
            Ok
            </b-button>
        </div>
    </b-modal>
    <div id="newMovies">
      <div id="slide">
        <h1>Reccommendation Based On Watch History</h1>
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
        >
          <slide v-for="(item, index) in ml_rec" :key="index">
            <div
              class="card"
              :ref="`card_${index}`"
              @mouseover="hoverCard(index, 'ml_rec')"
              @mouseout="hoverCard(-1, '')"
            >
              <img
                class="card-image"
                :src="item.poster_path"
                :class="{ selected: isSelected(index, 'ml_rec') }"
              />
              <div class="card-text" :class="{ selected: isSelected(index, 'ml_rec') }">
                <div class="card-watchlist">
                  <b-button
                    variant="success"
                    style="margin-bottom: 60px; margin-top: 30px"
                    v-b-tooltip.hover
                    title="Add to Watchlist"
                    @click="add(item.id, item.poster_path, item.type, item.release_date)"
                  >
                    + Watchlist
                  </b-button>
                </div>
              </div>
            </div>
          </slide>
        </carousel>
      </div>
    </div>
    <div id="newMovies">
      <div id="slide">
        <h1>Reccommendation Based On Prefered Genres</h1>
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
          <slide v-for="(item, index) in pref_rec" :key="index">
            <div
              class="card"
              :ref="`card_${index}`"
              @mouseover="hoverCard(index, 'pref_rec')"
              @mouseout="hoverCard(-1, '')"
            >
              <img
                class="card-image"
                :src="item.poster_path"
                :class="{ selected: isSelected(index, 'pref_rec') }"
              />

              <div class="card-text" :class="{ selected: isSelected(index, 'pref_rec') }">
                <div class="card-watchlist">
                  <b-button
                    variant="success"
                    style="margin-bottom: 60px; margin-top: 30px"
                    v-b-tooltip.hover
                    title="Add to Watchlist"
                    @click="add(item.id, item.poster_path, item.type, item.release_date)"
                  >
                    + Watchlist
                  </b-button>
                </div>
              </div>
            </div>
          </slide>
        </carousel>
          <div  id ="empty" v-if="this.loading == true && pref_rec.length == 0">
          <div style="padding:6px">Add Some Genres To Your Preference </div>
          <b-button class="btn btn-secondary" to="/account"> + </b-button>
        </div>
      </div>
    </div>
    <div id="newMovies">
      <div id="slide">
        <h1>Trending TV Shows/Movies</h1>
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
          <slide v-for="(item, index) in trending" :key="index">
            <div
              class="card"
              :ref="`card_${index}`"
              @mouseover="hoverCard(index, 'trending')"
              @mouseout="hoverCard(-1, '')"
            >
              <img
                class="card-image"
                :src="item.poster_path"
                :class="{ selected: isSelected(index, 'trending') }"
              />

              <div class="card-text" :class="{ selected: isSelected(index, 'trending') }">
                <div class="card-watchlist">
                  <b-button
                    variant="success"
                    style="margin-bottom: 60px; margin-top: 30px"
                    v-b-tooltip.hover
                    title="Add to Watchlist"
                    @click="add(item.id, item.poster_path, item.type, item.release_date)"
                  >
                    + Watchlist
                  </b-button>


                </div>
              </div>
            </div>
          </slide>
        </carousel>
      </div>
    </div>
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
  name: "RecTitle",

  data() {
    return {
      loading:false,
      selectedCard: -1,
      selectedCat:"",
      ml_rec: [],
      pref_rec: [],
      trending:[],
      showLoading: true,
    };
  },
  props: ["typeDescription"],
  components: {
    Carousel,
    Slide,
    Spinner,
  },
  mounted() {
    this.load("");
  },
  computed: {
    ...mapGetters({
      user: "auth/user",
    }),
  },
  methods: {
    hoverCard(selectedIndex, category) {
      this.selectedCard = selectedIndex;
      this.selectedCat = category;
    },
    isSelected(cardIndex, category) {
      return (this.selectedCard === cardIndex && this.selectedCat === category);
    },
    add: function (id, poster, type, release_d) {
      console.log(this.$store.state.auth.token);
      axios({
        method: "POST",
        url: config.api.invokeUrl + "/watch/addlist",
        headers: {
          Authorization: this.$store.state.auth.token,
        },
        data: {
          userid: this.$store.state.auth.user.username,
          id: id,
          poster_path: poster,
          type: type,
          release_date: release_d
        },
      })
        .then((response) => {
          // handle success
          console.log(response["data"]);
          if (response["data"] == "Success") {
            this.showModal("success");
          }
          if (response["data"] == "Watchlist") {
            this.showModal("exists_watchlist");
          }
        if (response["data"] == "WatchNow") {
            this.showModal("exists_watchnow");
          }
        })
        .catch(function (error) {
          // handle error
          console.error("Error: ", error);
        });
    },
    async load() {
      this.showLoading = true;
      await Auth.currentSession().then((data) =>
        axios({
          method: "GET",
          url: config.api.invokeUrl + "/recommend",
          headers: {
            Authorization: data.idToken.jwtToken,
          },
          params: {
            userid: this.$store.state.auth.user.username,
          },
        })
          .then((response) => {
            // handle success
            console.log(response);
            this.trending = response["data"]["trending"];
            this.pref_rec = response["data"]["preference"];
            this.ml_rec = response["data"]["recommendation"];
            this.loading=true;
            this.showLoading = false;
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
#empty{
    display: flex;
    justify-content: center;
    padding: 120px
}
#slide {
  width: 95%;
  height: 100%;
  text-align: center;
  margin: auto;
}
#newMovies {
  width: 95%;
  height: 100%;
  text-align: center;
  margin: auto;
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

</style>

<style >
.VueCarousel-navigation-button {
  color: green !important;
  outline: none !important;
}
</style>
