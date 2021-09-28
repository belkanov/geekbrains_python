const goods = [
  { title: 'Shirt', price: 150 },
  { title: 'Socks', price: 50 },
  { title: 'Jacket', price: 350 },
  { title: 'Shoes', price: 250 },
];

// 2. Добавьте значения по умолчанию для аргументов функции. Как можно упростить или сократить запись функций?
// const renderGoodsItem = (title, price) => {
//   return `<div class="goods-item"><h3>${title}</h3><p>${price}</p></div>`;
// };
const renderGoodsItem = (title = "Название", price = 0) =>  `<div class="goods-item"><h3>${title}</h3><p>${price}</p></div>`;


const renderGoodsList = (list) => {
  // 3. *Сейчас после каждого товара на странице выводится запятая. Из-за чего это происходит? Как это исправить?
  //
  // запятая добавлялась из-за того, что массив при преобразовании в строку автоматически добавляет зпт как разделитель
  // исправляем через join:
  document.querySelector('.goods-list').innerHTML = list.map(item => renderGoodsItem(item.title, item.price)).join("");
}

renderGoodsList(goods);