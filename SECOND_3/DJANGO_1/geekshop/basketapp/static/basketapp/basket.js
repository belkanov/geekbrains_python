const TableRender = {
  delimiters: ['[[', ']]'],
  data() {
    return {
      basketObjs: [],
      totalCount: null,
      totalPrice: null
    }
  },
  methods: {
    basketEdit(id, value) {
      return fetch(`/basket/edit/${id}/${value}`, {headers: {"X-Requested-With": "XMLHttpRequest"}}) // заголовок нужен, чтобы работал is_ajax()
        .then(response => response.json());
    },
    getTotalCount() {
      return this.basketObjs.reduce((previousValue, currentValue) => previousValue + currentValue.quantity, 0);
    },
    getTotalPrice() {
      return this.basketObjs.reduce((previousValue, currentValue) => previousValue + currentValue.quantity * currentValue.product__price, 0);
    },
    toCurrency(value) {
      return value.toFixed(2);
    },
    quantityAdd(idx) {
      const newValue = this.basketObjs[idx].quantity + 1;
      const id = this.basketObjs[idx].id;
      this.basketEdit(id, newValue)
        .then(data => {
          if (!!data.editResultIsOK) {
            this.basketObjs[idx].quantity = newValue;
          }
        });
    },
    quantitySub(idx) {
      const newValue = this.basketObjs[idx].quantity - 1;
      const id = this.basketObjs[idx].id;
      if (newValue <= 0) {
        this.removeItem(idx, id);
      } else {
        this.basketEdit(id, newValue)
          .then(data => {
            if (!!data.editResultIsOK) {
              this.basketObjs[idx].quantity = newValue;
            }
          });
      }
    },
    removeItem(idx, id=null) {
      const pk = id ? id : this.basketObjs[idx].id;
      this.basketEdit(pk, 0)
        .then(data => {
          if (!!data.editResultIsOK) {
            this.basketObjs.splice(idx, 1);
          }
        })

    }
  },
  mounted() {
    fetch('/basket/data', {headers: {"X-Requested-With": "XMLHttpRequest"}})
      .then(response => response.json())
      .then(data => this.basketObjs = data.basket_objs);
  }
}

Vue.createApp(TableRender).mount('#vue-app');