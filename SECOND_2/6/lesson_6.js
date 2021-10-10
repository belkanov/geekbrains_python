'use strict';

class ProductItem {
    price;
    name;

    constructor(name, price) {
        this.price = price;
        this.name = name;
    }

    toHTML(idx) {
        const newElem = document.createElement('DIV');
        newElem.classList.add('product-description');

        const prodDescription = document.createElement('P')
        prodDescription.textContent = `${this.name}, ${this.price} $`;
        newElem.appendChild(prodDescription);

        const btnAdd = document.createElement('button')
        btnAdd.textContent = `В корзину`;
        btnAdd.idx = idx;
        btnAdd.onclick = BasketItem.addProductEvent;
        newElem.appendChild(btnAdd);

        return newElem;
    }
}

class BasketItem{
    static basket = document.querySelector('#part-2 .basket');
    static basketTotal = BasketItem.basket.querySelector('h3 span');
    static arrItems = [];
    static totalPrice = 0;
    static productsCount = 0;

    constructor(){
    }

    static addProduct(i){
        BasketItem.arrItems.push(arrProducts[i]); // в данный момент нам этот массив особо ни к чему, но он пригодится, если надо будет его куда-то передать.
        BasketItem.productsCount += 1;
        BasketItem.totalPrice += arrProducts[i].price;
        BasketItem.basketTotal.textContent = `${BasketItem.productsCount} шт., ${BasketItem.totalPrice} $`;

        let newChild = document.createElement('P');
        newChild.textContent = `${arrProducts[i].name}, ${arrProducts[i].price} $`;
        BasketItem.basket.appendChild(newChild);
    }

    static addProductEvent(event){
        BasketItem.addProduct(event.target.idx);
    }
}

function randomInteger(min, max) {
    let rand = min + Math.random() * (max + 1 - min);
    return Math.floor(rand);
}

// 1. Доработать функцию замены картинки в галерее таким образом, чтобы она проверяла наличие картинки по указанному в src адресу.

function part_1() {
    let imgs = document.querySelectorAll('#part-1>.img-small') // ИД не обязателен, ибо класс уникален. Просто решил уточнить часть ДЗ
    for(let elem of imgs) {
        elem.onclick = function (e) {
            // bigImg можно и глобальной сделать, чтобы ее не искать каждый раз при нажатии
            // я просто решил весь нужный код в кучу собрать
            let bigImg = document.querySelector('#img-big');
            bigImg.src = e.target.src.replace('small', 'big');
        }
    }

    document.querySelector('#img-big').onerror = function(e){
        // в Edge получал ошибку при первой загрузке страницы. В хроме такого не было
        // гугл вывел на затык в endless loop, рекомендовали сделать this.onerror=null;
        // просьба в ответе на ДЗ или на уроке освятить этот момент подробней
        alert(JSON.stringify(`Не получилось найти большую картинку: ${e.target.getAttribute('src')}`));
    }
}

// 2. Реализовать модуль корзины. Создать блок товаров и блок корзины.
// У каждого товара есть кнопка «Купить», при нажатии на которую происходит добавление имени и цены товара в блок корзины.
// Корзина должна уметь считать общую сумму заказа.

const arrProducts = [];
arrProducts.push(new ProductItem('Ноутбук', randomInteger(500, 2000)));
arrProducts.push(new ProductItem('Велосипед', randomInteger(100, 500)));
arrProducts.push(new ProductItem('Смартфон', randomInteger(100, 1000)));

const productsTag = document.querySelector('#part-2 .products')
arrProducts.forEach(function(obj, idx){
    productsTag.appendChild(obj.toHTML(idx));
})


// 3) *Добавить в галерею функцию перехода к следующему изображению.
// По сторонам от большой картинки должны быть стрелки «вперед» и «назад»,
// по нажатию на которые происходит замена изображения на следующее или предыдущее.

const arrImgPaths = ["big/1.jpg", "big/2.jpg", "big/3_.jpg"], // предположим, что мы эту штуку будем получать от бэка
      leftBtn = document.querySelector('#part-3 .left-button'),
      rightBtn = document.querySelector('#part-3 .right-button'),
      img = document.querySelector('#part-3 img');

function part_3() {
    function toLeft(){
        let idx = leftBtn.idx || 0;
        if (Number(idx) <= 0){
            idx = arrImgPaths.length-1;
        } else {
            idx -= 1;
        }
        leftBtn.idx = idx;
        rightBtn.idx = idx;

        img.src = arrImgPaths[idx];
    }

    function toRight(){
        let idx = rightBtn.idx || 0;
        if (Number(idx) >= arrImgPaths.length-1){
            idx = 0;
        } else {
            idx += 1;
        }
        leftBtn.idx = idx;
        rightBtn.idx = idx;

        img.src = arrImgPaths[idx];
    }

    leftBtn.onclick = toLeft;
    rightBtn.onclick = toRight;

}



part_1();
// part_2();
part_3();