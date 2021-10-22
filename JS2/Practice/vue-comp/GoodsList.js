import GoodsItem from './GoodsItem.js'

export default {
  name: 'GoodsList',
  props: ['goods'],
  components: {GoodsItem},
  template:`
    <div class="goods-list">
      <GoodsItem v-for="(good, idx) in goods" :good="good" :idx="idx" :key="good.id_product" @calc-total="$root.calcTotal"></GoodsItem>
    </div>
  `
}