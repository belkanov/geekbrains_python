// const API_URL = 'https://raw.githubusercontent.com/GeekBrainsTutorial/online-store-api/master/responses';
const API_URL = 'http://127.0.0.1:3000';

Vue.component('goods-list', {
    props: ['goods'],
    template: `
      <div class="goods-list">
        <goods-item v-for="(good, idx) in goods" :good="good" :idx="idx" :key="good.id_product" @calc-total="$root.calcTotal"></goods-item>
      </div>
    `
});

Vue.component('goods-item', {
    props: ['good', 'idx'],
    template: `
      <div class="goods-item">
      <div v-if="good.id_product === -1">
        <h3>Нет данных</h3>  <!-- решил что нет особого смысла вырезать эту строчку отдельно для п.3, чтобы "нет данных" было в отдельном компоненте-->
      </div>
      <div v-else>
        <h3>{{ good.product_name }}</h3>
        <p>{{ good.price }}</p>
        <button @click="addToCart">В корзину</button>
      </div>
      </div>
    `,
    methods: {
        addToCart() {
            const cartIdx = this.$root.cartGoods.map(x => x.id_product).indexOf(this.good.id_product);
            if (cartIdx >= 0) {
                this.$root.cartGoods[cartIdx].count++;
                this.$root.cartGoods[cartIdx].total += this.$root.cartGoods[cartIdx].price;
            } else {
                const item = {...this.good, count: 1, total: this.good.price};
                this.$root.makePOSTRequest('/addToCart', JSON.stringify(item))
                  .then(rslt => {
                      let r = JSON.parse(rslt);
                      if (r.result === 1) {
                          this.$root.cartGoods.push(item);
                          this.$emit('calc-total');
                      } else if (r.result === 0){
                          alert(`Не получилось добавить "${item.product_name}" в корзину`);
                      }
                  }, err => {
                      alert(err); // так конечно не круто делать =) просто заглушка
                  });
            }

        }
    }
});

Vue.component('cart-list', {
    props: ['goods', 'isVisibleCart', 'total'],
    template: `
      <div class="cart-list" v-show="isVisibleCart">
          <h3>{{ total }}</h3>
          <cart-item v-for="(good, idx) in goods" :good="good" :idx="idx" :key="good.id_product" @calc-total="$root.calcTotal"></cart-item>
      </div>
    `,
    methods: {
        calcTotal() {
            console.log('calcTotal');
            this.total = this.goods.map(x => x.total).reduce((a, b) => a + b);
        }
    }
});

Vue.component('cart-item', {
    props: ['good', 'idx'],
    template: `
      <div class="cart-item">
          <h3>{{ good.product_name }}</h3>
          <p>{{ good.price }}</p>
          <p>
            <span class="cart-list-sub" @click="goodSub">- </span>
            {{ good.count }}
            <span class="cart-list-plus" @click="goodPlus"> +</span>
          </p>
          <p>{{ good.total }}</p>
      </div>
    `,
    methods: {
        update(id_product, count, total) {
            this.$root.makePOSTRequest('/editCart', JSON.stringify({id_product:id_product, count:count, total:total}))
                  .then(rslt => {
                      const r = JSON.parse(rslt);
                      if (r.result === 1) {
                          this.good.count = count;
                          this.good.total = total;
                          this.$emit('calc-total');
                      } else if (r.result === 0){
                          alert(`Не получилось обновить "${item.product_name}" в корзине`);
                      }
                  }, err => {
                      alert(err); // так конечно не круто делать =) просто заглушка
                  });
        },
        delete(id_product) {
            this.$root.makePOSTRequest('/delFromCart', JSON.stringify({id_product:id_product}))
                  .then(rslt => {
                      const r = JSON.parse(rslt);
                      if (r.result === 1) {
                          this.$root.cartGoods.splice(this.idx, 1);
                          this.$emit('calc-total');
                      } else if (r.result === 0){
                          alert(`Не получилось удалить "${item.product_name}" из корзине`);
                      }
                  }, err => {
                      alert(err); // так конечно не круто делать =) просто заглушка
                  });
        },
        goodSub() {
            let {id_product, count, price, total} = this.good;
            count--;
            total -= price;

            if (count <= 0) {
                this.delete(id_product);
            } else {
                this.update(id_product, count, total);
            }
        },
        goodPlus() {
            let {id_product, count, price, total} = this.good;
            count++;
            total += price;
            this.update(id_product, count, total);
        }
    }
});

Vue.component('search-item', {
    data: () => (
        {
            searchLine: ''
        }
    ),
    template:`
      <div>
        <input type="text" v-model="searchLine">
        <button class="cart-button" type="button" @click="filterGoods">Поиск</button>
      </div>
    `,
    methods: {
        filterGoods(){
            this.$root.filteredGoods = [];
            console.log(this.searchLine.toLowerCase());
            this.$root.goods.forEach((item) => {
                console.log(item);
                if (this.searchLine.length === 0 || item.product_name.toLowerCase().includes(this.searchLine.toLowerCase())) {
                    this.$root.filteredGoods.push(item);
                }
            });
        }
    }
});

const app = new Vue({
    el: '#app',
    data: {
        goods: [],
        filteredGoods: [],
        cartGoods: [],
        cartTotal: null,
        isVisibleCart: false
    },
    methods: {
        makeRequest(url, type, data=null) {
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
        makeGETRequest(url, data=null) {
            return this.makeRequest(url, 'GET', data);
        },
        makePOSTRequest(url, data=null) {
            return this.makeRequest(url, 'POST', data);
        },
        switchShowCart() {
            this.isVisibleCart = !this.isVisibleCart;
        },
        calcTotal() {
            if (this.cartGoods.length !== 0) {
                this.cartTotal = this.cartGoods.map(x => x.total).reduce((a, b) => a + b);
            } else {
                this.cartTotal = 0;
            }
        }
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