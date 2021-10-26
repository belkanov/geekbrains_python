const API_URL = 'https://raw.githubusercontent.com/GeekBrainsTutorial/online-store-api/master/responses';
// const API_URL = 'http://127.0.0.1'; // для п.3 и вывода "нет данных"

const app = new Vue({
  el: '#app',
  data: {
    goods: [],
    filteredGoods: [],
    cartGoods: [],
    searchLine: '',
    isVisibleCart: false,
    cartTotal: null,
  },
  methods: {
    makeGETRequest(url) {
      return new Promise((resolve, reject) => {
        let xhr = new XMLHttpRequest(); // мы тут взрослые, адекватные люди =) поддержку IE вообще обещают убрать с середины 2022, так что оставим так. ActiveX буду дежрать в голове.

        xhr.onreadystatechange = () => {
          console.log(new Date(), xhr.readyState);
          if (xhr.readyState === 4) {
            if (xhr.status === 200) {
              resolve(xhr.responseText);
            }
            else {
              reject('makeGETRequest_ERR');
            }
          }
        }

        xhr.timeout = 15000;
        xhr.ontimeout = () => {
          reject('makeGETRequest_ERR');
        }

        xhr.onerror = () => {
          reject('makeGETRequest_ERR');
        }

        xhr.open('GET', url, true);
        xhr.send();
      });
    },
    filterGoods() {
      console.log(this.searchLine);
      this.filteredGoods = [];
      this.goods.forEach((item) => {
        if (item.product_name.includes(this.searchLine) || this.searchLine.length === 0) {
          this.filteredGoods.push(item);
        }
      });
    },
    switchShowCart() {
      this.isVisibleCart = !this.isVisibleCart;
    },
    calcCartTotal() {
      this.cartTotal = this.cartGoods.map(item => item.total).reduce((a, b) => a + b);
    },
    addToCart(e, idx) {
      const good = this.goods[idx];
      const cartIdx = this.cartGoods.map(x => x.id_product).indexOf(good.id_product);
      if (cartIdx >= 0) {
        this.cartGoods[cartIdx].count++;
        this.cartGoods[cartIdx].total += this.cartGoods[cartIdx].price;
      } else {
        this.cartGoods.push({ ...good, count: 1, total: good.price })
      }
      this.calcCartTotal();
    },
    cartGoodPlus(e, idx) {
      this.cartGoods[idx].count++;
      this.cartGoods[idx].total += this.cartGoods[idx].price;
      this.calcCartTotal();
    },
    cartGoodSub(e, idx) {
      if (--this.cartGoods[idx].count <= 0) {
        this.cartGoods.splice(idx, 1);
      } else {
        this.cartGoods[idx].total -= this.cartGoods[idx].price;
      }
      this.calcCartTotal();
    }
    
  },
  mounted() {
    this.makeGETRequest(`${API_URL}/catalogData.json`)
      .then(
        goods => {
          this.goods = JSON.parse(goods);
          this.filteredGoods = JSON.parse(goods);
        }
        , error => this.filteredGoods = [{ id_product: -1 }]);
  },

});
