import CartItem from './CartItem.js';

export default {
  name: 'CartList',
  components: {CartItem},
  props: ['goods'],
  template:`
    <div>
      <div>
        <button class="cart-button" type="button" @click="switchShowCart">Корзина</button>
      </div>  
      <div class="cart-list" v-show="isVisibleCart">
        <h3>{{ cartTotal }}</h3>
        <CartItem v-for="(good, idx) in goods" :good="good" :idx="idx" :key="good.id_product" @calc-total="calcTotal"></CartItem>
      </div>
    </div>
  `,
  data() {
    return {
      isVisibleCart: false,
      total: null
    }
  },
  computed: {
    // сделал так, чтобы срабатывал пересчет при добавлении товара в корзину.
    // с текущей реализацией (нет глобальной переменной в $root для суммы в корзине) я не придумал способа
    // достучаться из товаров до корзины через emit, т.к. они не дочерние
    cartTotal : function () {
      this.calcTotal();
      return this.total;
    }
  },
  methods: {
    switchShowCart() {
      this.isVisibleCart = !this.isVisibleCart;
    },
    calcTotal() {
      this.total = 0;
      if (this.goods.length !== 0) {
        // this.total = this.goods.map(x => x.total).reduce((a, b) => a + b);
        this.total = this.goods.reduce((a, b) => a + b.total, 0);
      }
    }
  }
}