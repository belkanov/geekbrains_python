'use strict';

// Написать функцию, преобразующую число в объект. Передавая на вход число от 0 до 999, надо получить на выходе объект,
// в котором в соответствующих свойствах описаны единицы, десятки и сотни.
// Например, для числа 245 надо получить следующий объект: {‘единицы’: 5, ‘десятки’: 4, ‘сотни’: 2}.
// Если число превышает 999, необходимо выдать соответствующее сообщение с помощью console.log и вернуть пустой объект.
function part_1() {
    function NumDescription (num){
            let n = Number(num);
            if (n > 999) {
                console.log('Число больше 999');
                return null;
            }
            // в виду наличия строгих рамок входящих данных - сделал так.
            // если бы можно было вводить любое - там уже через цикл и в массив/словарь например
            this.units = n % 10;
            n = Math.floor(n/10); // не сработает с отрицательными
            this.tens = n % 10;
            n = Math.floor(n/10);
            this.hundreds = n % 10;
    }

    let nums = [0, 2, 35, '456', 999, 1000];
    for(let num of nums) {
        console.log(num, new NumDescription(num));
    }


}

// Продолжить работу с интернет-магазином:
// В прошлом домашнем задании вы реализовали корзину на базе массивов. Какими объектами можно заменить их элементы?
// Реализуйте такие объекты.
// Перенести функционал подсчета корзины на объектно-ориентированную базу.

function part_2() {
    // сделано в https://github.com/belkanov/geekbrains_python/pull/22
}

// * Подумать над глобальными сущностями. К примеру, сущность «Продукт» в интернет-магазине актуальна не только для корзины,
// но и для каталога. Стремиться нужно к тому, чтобы объект «Продукт» имел единую структуру для различных модулей сайта,
// но в разных местах давал возможность вызывать разные методы.

function part_3() {
    // User (может быть какойнить счетчик уведомлений/сообщений, баланс/кэшбэк, ... )
    // Category (может содержать подкатегории для реализации выпадающих меню)
    // ProductItem
    //
    // возможно что-то еще.. сильно подозреваю, что появятся другие при проработке архитектуры.
    // мне наверное хватит и этих, т.к. особых пожеланий, кроме норм фильтров (а это исключительно проработка инфы в БД), к интернет-магазину у меня нет.
    //
    // возможно еще что-то по типу PaidItem, где будет описываться кредитка для оплаты..
    // но я хз как дела с интеграцией платежных систем (ПС) обстоят. может это вообще не моя забота будет (все на стороне ПС реализовано например) =)
    //
    // для чатиков можно накинуть MessageItem, где опишем ник, время, статус доставки/прочтения и само сообщение
    // но можно и без чатиков =) как-то так в общем..
}

part_1();