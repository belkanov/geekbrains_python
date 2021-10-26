export default {
  name: 'SearchItem',
  template: `
  <div>
    <input type="text" v-model="searchLine">
    <button class="cart-button" type="button" @click="filterGoods">Поиск</button>
  </div>
  `,
  data() {
    return {
      searchLine: ''
    }
  },
  methods: {
    filterGoods() {
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
};