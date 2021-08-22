'use strict';

// С помощью цикла while вывести все простые числа в промежутке от 0 до 100.

function part_1() {
 console.log('--- part_1');

 f1: for (let i = 2; i <= 100; i++) {  // 0 и 1 мимо по определению простого числа
  for (let j = 2; j < i; j++) { // на 1 и так все делится - нет смысла начинать с него
   if (i % j === 0) {
    continue f1;
   }
  }
  console.log(i);
 }
}

//С этого урока начинаем работать с функционалом интернет-магазина. Предположим, есть сущность корзины. Нужно реализовать функционал подсчета стоимости корзины в зависимости от находящихся в ней товаров.
// Товары в корзине хранятся в массиве. Задачи:
// Организовать такой массив для хранения товаров в корзине;
// Организовать функцию countBasketPrice, которая будет считать стоимость корзины.

function part_2(){
 console.log('--- part_2');

 class BasketItem {
  cnt;
  price;

  constructor(cnt, price){
   this.cnt = cnt;
   this.price = price;
  }

  static countBasketPrice(arr) {
   let total = 0;
   for (const arrElement of arr) {
    total += arrElement.cnt * arrElement.price;
   }
   return total;
  }
 }

 function randomInteger(min, max) {
  let rand = min + Math.random() * (max + 1 - min);
  return Math.floor(rand);
 }

 let arr = [];
 for (let i = 0; i < 3; i++) {
  arr.push(new BasketItem(randomInteger(1, 5), randomInteger(10, 20)))
 }
 console.log(arr);
 console.log(BasketItem.countBasketPrice(arr));
}

// * Вывести с помощью цикла for числа от 0 до 9, не используя тело цикла. Выглядеть это должно так:
// for(...){// здесь пусто}

function part_3() {
 console.log('--- part_3');

 for(let i = 0; i <= 9; console.log(i++)){}
}

// * Нарисовать пирамиду с 20 рядами с помощью console.log, как показано на рисунке:
function part_4(){
 console.log('--- part_4');

 for(let i = 1; i <= 20; console.log('x'.repeat(i++))){}
}

part_1();
part_2();
part_3();
part_4();
