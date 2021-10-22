export default {
  name: 'CartItem',
  props: ['good'],
  template:`
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
      this.$root.makePOSTRequest('/editCart', JSON.stringify({id_product: id_product, count: count, total: total}))
          .then(rslt => {
            const r = JSON.parse(rslt);
            if (r.result === 1) {
              this.good.count = count;
              this.good.total = total;
              this.$emit('calc-total');
            } else if (r.result === 0) {
              alert(`Не получилось обновить "${item.product_name}" в корзине`);
            }
          }, err => {
            alert(err); // так конечно не круто делать =) просто заглушка
          });
    },
    delete(id_product) {
      this.$root.makePOSTRequest('/delFromCart', JSON.stringify({id_product: id_product}))
          .then(rslt => {
            const r = JSON.parse(rslt);
            if (r.result === 1) {
              this.$root.cartGoods.splice(this.idx, 1);
              this.$emit('calc-total');
            } else if (r.result === 0) {
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
}