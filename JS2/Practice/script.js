const API_URL = 'https://raw.githubusercontent.com/GeekBrainsTutorial/online-store-api/master/responses';

class CartItem {
    constructor({title, price, count = 1}) {
        this.title = title;
        this.price = price;
        this.count = count;
    }

    render() {
    }
}

class Cart {
    constructor() {
        this.list = [];
    }

    render() {
    }

    // 2. Добавьте в соответствующие классы методы добавления товара в корзину, удаления товара из корзины и получения списка товаров корзины.
    //
    // я чет не совсем понял надо ли писать HTML под все это дело (в методе вроде пишут HTML для чего-то нового - я там этого не увидел).
    // Пока сделал без него. Дальше либо из методы возьму, либо сам напишу.
    addItem({product_name: title, price}) {
        this.list.push(new CartItem({title, price}));
    }

    removeItem({idx}) {
        this.list.splice(idx, 1);
        // тут код удаления DOM CartItem
        //
        // тут возможно Cart.calc(), чтобы обновить сумму корзины, шт., ...
        // ну или что-то более локальное
    }

    getList() {
        return this.list; // если тут имелся ввинду рендер корзины в виде списка - переделаю в следующих ДЗ
    }

    addCount(idx) {
        this.list[idx].count += 1;
        // тут код обновления HTML для данного элекмента
    }

    subCount(idx) {
        this.list[idx].count -= 1;
        // тут код обновления HTML для данного элекмента
    }

    calc() {
    } // тут всякие суммы, шт., ...
}

class GoodsItem {
    constructor({product_name, price}) {
        this.title = product_name;
        this.price = price;
    }

    render() {
        return `<div class="goods-item"><h3>${this.title}</h3><p>${this.price}</p></div>`;
    }
}

class GoodsList {
    constructor() {
        this.goods = [];
    }

    // 3. Переделайте GoodsList так, чтобы fetchGoods() возвращал промис, а render() вызывался в обработчике этого промиса.
    fetchGoods() {
        return makeGETRequest(`${API_URL}/catalogData.json`)
                .then((goods) => {
                    this.goods = JSON.parse(goods);
                });
    }

    render() {
        document.querySelector('.goods-list').innerHTML = this.goods.map(item => new GoodsItem(item).render()).join("");
    }

    calcSum() {
        let sum = 0;
        this.goods.forEach(({price}) => sum += price)
        console.log(sum);
    }
}

// 1. Переделайте makeGETRequest() так, чтобы она использовала промисы.
function makeGETRequest(url) {
    return new Promise((resolve, reject) => {
        let xhr = new XMLHttpRequest(); // мы тут взрослые, адекватные люди =) поддержку IE вообще обещают убрать с середины 2022, так что оставим так. ActiveX буду дежрать в голове.

        xhr.onreadystatechange = () => {
            if (xhr.readyState === 4) {
                resolve(xhr.responseText);
            }
        }

        xhr.timeout = 15000;
        xhr.ontimeout = () => {
            reject('makeGETRequest_ERR');
        }

        xhr.open('GET', url, true);
        xhr.send();
    });
}

const list = new GoodsList();
list.fetchGoods()
    .then(() => list.render());