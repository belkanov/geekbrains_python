import SearchItem from "./vue-comp/SearchItem.js";
import CartList from "./vue-comp/CartList.js";
import GoodsList from "./vue-comp/GoodsList.js";

// const API_URL = 'https://raw.githubusercontent.com/GeekBrainsTutorial/online-store-api/master/responses';
const API_URL = 'http://127.0.0.1:3000';

new Vue({
  el: '#app',
  data: {
    goods: [],
    filteredGoods: [],
    cartGoods: []
  },
  components: {
    SearchItem, CartList, GoodsList
  },
  methods: {
    makeRequest(url, type, data = null) {
      return new Promise((resolve, reject) => {
        let xhr = new XMLHttpRequest();

        xhr.onreadystatechange = () => {
          if (xhr.readyState === 4) {
            if (xhr.status === 200) {
              resolve(xhr.responseText);
            } else {
              reject(`make${type}Request_ERR`);
            }
          }
        }

        xhr.timeout = 15000;
        xhr.ontimeout = () => {
          reject(`make${type}Request_ERR`);
        }
        xhr.onerror = () => {
          reject(`make${type}Request_ERR`);
        }

        xhr.open(type, url, true);
        if (type === 'POST') {
          xhr.setRequestHeader("Content-type", "application/json; charset=UTF-8");
        }

        xhr.send(data);
      });
    },
    makeGETRequest(url, data = null) {
      return this.makeRequest(url, 'GET', data);
    },
    makePOSTRequest(url, data = null) {
      return this.makeRequest(url, 'POST', data);
    },
  },
  mounted() {
    this.makeGETRequest(`${API_URL}/catalogData`)
      .then(
        goods => {
          this.goods = JSON.parse(goods);
          this.filteredGoods = JSON.parse(goods);
        }
        , error => this.filteredGoods = [{id_product: -1}]);
  }
});