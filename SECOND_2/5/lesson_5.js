'use strict';

class ProductItem {
    cnt;
    price;
    name;

    constructor(cnt, price, name = null) {
        this.cnt = cnt;
        this.price = price;
        if (name) {
            this.name = name;
        } else {
            this.name = `product-${cnt}-${price}`;
        }
    }

    static countBasketPrice(arr) {
        let total = 0;
        let cnt = 0;
        for (let arrElement of arr) {
            cnt += arrElement.cnt
            total += arrElement.cnt * arrElement.price;
        }
        return {cnt, total};
    }

    toHTML() {
        const elem = document.createElement('DIV');
        elem.classList.add('product-elem');

        const elemName = document.createElement('DIV');
        elemName.classList.add('product-name');
        elemName.textContent = `NAME: ${this.name}`;
        elem.appendChild(elemName);

        const elemCount = document.createElement('DIV');
        elemCount.classList.add('product-count');
        elemCount.textContent = `COUNT: ${this.cnt}`;
        elem.appendChild(elemCount);

        const elemPrice = document.createElement('DIV');
        elemPrice.classList.add('product-price');
        elemPrice.textContent = `PRICE: ${this.price}`;
        elem.appendChild(elemPrice);

        return elem;
    }

    static createCatalogHTML(arr) {
        const base = document.createElement('DIV');
        base.classList.add('product-container');

        for (let elem in arr) {
            base.appendChild(arr[elem].toHTML());
            if ((elem + 1) % 3 === 0) {
                const elemBreak = document.createElement('DIV');
                elemBreak.classList.add('product-elem-break');
                base.appendChild(elemBreak);
            }
        }

        return base;
    }
}

function randomInteger(min, max) {
    let rand = min + Math.random() * (max + 1 - min);
    return Math.floor(rand);
}

// Создать функцию, генерирующую шахматную доску. Можно использовать любые html-теги.
// Доска должна быть верно разлинована на черные и белые ячейки.
// Строки должны нумероваться числами от 1 до 8, столбцы — латинскими буквами A, B, C, D, E, F, G, H.

function part_1() {

    function createCell(txt, ...classes) {
        const divElement = document.createElement('DIV');
        divElement.classList.add('cell');
        if (classes) {
            divElement.classList.add(...classes);
        }
        if (txt) {
            divElement.textContent = txt;
        }

        return divElement;
    }

    const board = document.createElement('DIV');
    board.classList.add('chessboard');

    // col names
    board.appendChild(createCell(null, 'row-name'));
    board.appendChild(createCell('A', 'col-name'));
    board.appendChild(createCell('B', 'col-name'));
    board.appendChild(createCell('C', 'col-name'));
    board.appendChild(createCell('D', 'col-name'));
    board.appendChild(createCell('E', 'col-name'));
    board.appendChild(createCell('F', 'col-name'));
    board.appendChild(createCell('G', 'col-name'));
    board.appendChild(createCell('H', 'col-name'));

    // rows
    for (let i = 1; i <= 8; i++) {
        board.appendChild(createCell(i.toString(), 'row-name'));
        for (let j = 0; j < 8; j++) {
            board.appendChild(createCell(null, 'chess-cell'));
        }
    }

    document.querySelector('#part-1').appendChild(board);
}

// Сделать генерацию корзины динамической: верстка корзины не должна находиться в HTML-структуре.
// Там должен быть только div, в который будет вставляться корзина, сгенерированная на базе JS:
// - Пустая корзина должна выводить строку «Корзина пуста»;
// - Наполненная должна выводить «В корзине: n товаров на сумму m рублей».

function part_2() {
    console.log('--- part_2');

    const basketElement = document.createElement('DIV');
    const rslt = ProductItem.countBasketPrice(arrProduct);
    if (rslt) {
        basketElement.textContent = `В корзине: ${rslt.cnt} товаров на сумму ${rslt.total} рублей`;
        console.log(rslt);
    } else {
        basketElement.textContent = `Корзина пуста`;
    }

    document.querySelector('#part-2').appendChild(basketElement);
}

// * Сделать так, чтобы товары в каталоге выводились при помощи JS:
// - Создать массив товаров (сущность Product);
// - При загрузке страницы на базе данного массива генерировать вывод из него.
//   HTML-код должен содержать только div id=”catalog” без вложенного кода. Весь вид каталога генерируется JS.

function part_3() {
    // я буду цеплять код к <div id="part-3">, просто чтоб картину не портить =)
    console.log('--- part_3');

    const rslt = ProductItem.createCatalogHTML(arrProduct);
    document.querySelector('#part-3').appendChild(rslt);
}

let arrProduct = [];
for (let i = 0; i < 5; i++) {
    arrProduct.push(new ProductItem(randomInteger(1, 5), randomInteger(10, 20)))
}
console.log(arrProduct);

part_1();
part_2();
part_3();