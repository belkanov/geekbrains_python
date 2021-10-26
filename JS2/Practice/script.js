const API_URL = 'https://raw.githubusercontent.com/GeekBrainsTutorial/online-store-api/master/responses';
// const API_URL = 'http://127.0.0.1'; // для п.3 и вывода "нет данных"

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
        <!--        <button @click="this.$root.addToCart($event, idx)">В корзину</button>-->
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
                this.$root.cartGoods.push({...this.good, count: 1, total: this.good.price})
            }
            this.$emit('calc-total');
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
        goodSub() {
            if (--this.good.count <= 0) {
              this.$root.cartGoods.splice(this.idx, 1);
            } else {
              this.good.total -= this.good.price;
            }
            console.log('call event...');
            this.$emit('calc-total');
        },
        goodPlus() {
            this.good.count++;
            this.good.total += this.good.price;
            console.log('call event...');
            this.$emit('calc-total');
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
        makeGETRequest(url) {
            return new Promise((resolve, reject) => {
                let xhr = new XMLHttpRequest(); // мы тут взрослые, адекватные люди =) поддержку IE вообще обещают убрать с середины 2022, так что оставим так. ActiveX буду дежрать в голове.

                xhr.onreadystatechange = () => {
                    // console.log(new Date(), xhr.readyState);
                    if (xhr.readyState === 4) {
                        if (xhr.status === 200) {
                            resolve(xhr.responseText);
                        } else {
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
        this.makeGETRequest(`${API_URL}/catalogData.json`)
            .then(
                goods => {
                    this.goods = JSON.parse(goods);
                    this.filteredGoods = JSON.parse(goods);
                }
                , error => this.filteredGoods = [{id_product: -1}]);
    }
});