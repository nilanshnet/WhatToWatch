
<template>
  <div>
    <div style="display: flex; justify-content: center" class="search">
      <b-form-input
        style="width: 29%"
        v-model="param"
        type="text"
        placeholder="Search by Genre Or TV Show/Movie Title"
      ></b-form-input>
      <div class="form-group">
        <button
          class="btn btn-success"
          style="margin-left: 15px"
          @click="search"
        >
          Search
        </button>
      </div>
    </div>
    <div v-if= "size == -1">
    <RecTitle />
    
    
    </div>

    <div v-if= "size == 0" class="container">
    <div>
      Search did not return any result
    </div>
    </div>

                  <div v-if= "size>0" class="container">
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
                    </div>
                    <div>
                      <div class="row" style="justify-content: center">
                        <div
                          v-for="(item, index) in result"
                          :key="index"
                          :ref="`card_${index}`"
                          @mouseover="hoverCard(index)"
                          @mouseout="hoverCard(-1)"
                        >
                          <div class="card">
                            >
                            <img
                              class="card-image"
                              :class="{ selected: isSelected(index) }"
                              :src="item.poster_path"
                            />

                            <h3 class="card-title" :class="{ selected: isSelected(index) }">
                              {{ item.title }}
                            </h3>
                            <div class="card-text" :class="{ selected: isSelected(index) }">
                              <div class="card-watchlist">
                                <button
                                  class="btn btn-success"
                                  @click="add(item.id, item.poster_path, item.type, item.release_date)"
                                >
                                  Add to Watchlist
                                </button>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
  </div>
</template>

<script>
import RecTitle from "@/components/RecTitle.vue";
import axios from "axios";
var config = require("../config.js");
export default {
  name: "search",
  components: {
      RecTitle
  },
  data() {
    return {
      selectedCard: -1,
      result: [],
      param: "",
      size: -1
    };
  },
  methods: {
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

    showModal(name) {
      this.$refs[name].show();
    },
    hideModal(name) {
      this.$refs[name].hide();
    },

    search: function () {
      axios({
        method: "GET",
        url: config.api.invokeUrl + "/search",
        headers: {
          Authorization: this.$store.state.auth.token,
        },
        params: {
          q: this.param,
        },
      })
        .then((response) => {
          // handle success
          console.log(response["data"]);
          this.result = response["data"];
          this.size = this.result.length;
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
  },
};
</script>

<style lang="scss" scoped>
.card-row {
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
  height: 370px;
  width: 240px;
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
  height: 370px;
  min-width: 100%;
  transition: height 0.3s, opacity 0.3s;
}
.card-image.selected {
  opacity: 0.3;
  height: 370px;
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

v:deep .my-second-class > .modal-dialog > .modal-content > .modal-header {
  background: black;
  color: white;
}
</style>