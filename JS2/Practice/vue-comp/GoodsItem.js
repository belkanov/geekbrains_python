export default {
  name: 'GoodsItem',
  // props: ['good', 'idx'],
  props: ['good'],
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
              } else if (r.result === 0) {
                alert(`Не получилось добавить "${item.product_name}" в корзину`);
              }
            }, err => {
              alert(err); // так конечно не круто делать =) просто заглушка
            });
      }
    }
  }
}
