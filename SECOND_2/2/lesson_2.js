// Почему код дает именно такие результаты?
function part_1() {
    console.log('--- part_1');
    let a = 1, b = 1, c, d;
    c = ++a; console.log(c);           // 2; результат а+1; a=2
    d = b++; console.log(d);           // 1; результат b, после присваивания увеличиваем b; b=2
    c = (2+ ++a); console.log(c);      // 5; 2+(2+1); a=3
    d = (2+ b++); console.log(d);      // 4; 2+(2); b+1; b=3
    console.log(a);                    // 3
    console.log(b);                    // 3
}

// Чему будет равен x?
function part_2(){
    console.log('--- part_2');
    let a = 2;
    let x = 1 + (a *= 2); // 1+(2*2); a = 4
    console.log(a);
    console.log(x);
}


// Объявить две целочисленные переменные — a и b и задать им произвольные начальные значения. Затем написать скрипт, который работает по следующему принципу:
//  - если a и b положительные, вывести их разность;
//  - если а и b отрицательные, вывести их произведение;
//  - если а и b разных знаков, вывести их сумму;
// Ноль можно считать положительным числом.
function part_3() {
    function someMagic(x, y) {
        console.log(x, y);
        if (x >= 0 && y >= 0) {
            console.log('разность:', (x - y));
        } else if (x < 0 && y < 0) {
            console.log('произведение:', (x * y));
        } else {
            console.log('сумма:', (x + y));
        }
    }

    console.log('--- part_3');
    let a = 3, b = 4;
    someMagic(a, b);
    a = -2; b = -5;
    someMagic(a, b);
    a = -6; b = 7;
    someMagic(a, b);
    a = 8; b = -9;
    someMagic(a, b);
}

// Присвоить переменной а значение в промежутке [0..15]. С помощью оператора switch организовать вывод чисел от a до 15.
function part_4() {
    console.log('--- part_4');
    let a = 1;
    console.log('a =', a);
    switch (a) {
        case 0:
            console.log(0);
        case 1:
            console.log(1);
        case 2:
            console.log(2);
        case 3:
            console.log(3);
        case 4:
            console.log(4);
        case 5:
            console.log(5);
        case 6:
            console.log(6);
        case 7:
            console.log(7);
        case 8:
            console.log(8);
        case 9:
            console.log(9);
        case 10:
            console.log(10);
        case 11:
            console.log(11);
        case 12:
            console.log(12);
        case 13:
            console.log(13);
        case 14:
            console.log(14);
        case 15:
            console.log(15);
    }
}

// Реализовать четыре основные арифметические операции в виде функций с двумя параметрами. Обязательно использовать оператор return.
function add(a, b) {
    return a + b;
}

function sub(a, b) {
    return a - b;
}

function mul(a, b) {
    return a * b;
}

function div(a, b) {
    return a / b;
}

// Реализовать функцию с тремя параметрами: function mathOperation(arg1, arg2, operation), где arg1, arg2 — значения аргументов,
// operation — строка с названием операции.
// В зависимости от переданного значения выполнить одну из арифметических операций (использовать функции из пункта 5) и вернуть полученное значение (применить switch).
function mathOperation(arg1, arg2, operation) {
    switch (operation) {
        case '+':
            return add(arg1, arg2);
        case '-':
            return sub(arg1, arg2);
        case '*':
            return mul(arg1, arg2);
        case '/':
            return div(arg1, arg2);
        default:
            return 'Меня к такому жизнь не готовила..';
    }
}

function part_7() {
    function mathPrint(a, b, op) {
        console.log(`${a} ${op} ${b} = ${mathOperation(a, b, op)}`);
    }

    console.log('--- part_7');
    let a = -2, b = 10;
    mathPrint(a, b, '+');
    mathPrint(a, b, '-');
    mathPrint(a, b, '*');
    mathPrint(a, b, '/');
    mathPrint(a, b, '%');
}

// * Сравнить null и 0. Объяснить результат.
function part_8() {
    console.log('--- part_8');
    // ну тут все ожидаемо..
    console.log('1+0', 1+0); // 1
    console.log('1-0', 1-0); // 1
    console.log('1*0', 1*0); // 0
    console.log('1/0', 1/0); // Infinity
    // тут null ведет себя как 0
    console.log('1+null', 1+null); // 1
    console.log('1-null', 1-null); // 1
    console.log('1*null', 1*null); // 0
    console.log('1/null', 1/null); // Infinity
    // тут тоже как 0
    console.log('null+1', null+1); // 1
    console.log('null-1', null-1); // -1
    console.log('null*1', null*1); // 0
    console.log('null/1', null/1); // 0
    // и тут как 0
    console.log('null>1', null>1); // false
    console.log('null>=1', null>=1); // false
    console.log('null<1', null<1); // true
    console.log('null<=1', null<=1); // true
    console.log('null==1', null==1); // false
    console.log('null===1', null===1); // false
    // а вот тут магия..
    console.log('null>0', null>0); // false
    console.log('null>=0', null>=0); // true
    console.log('null<0', null<0); // false
    console.log('null<=0', null<=0); // true
    console.log('null==0', null==0); // false  хотя по идее должен быть true, исходя из >=,<=
    console.log('null===0', null===0); // false

    // как я понял - такое поведение объясняется тем, что больше/меньше и их вариации делают неявное приведение к 0,
    // а == для null/undefined работает без приведения. отсюда false.
}

// * С помощью рекурсии организовать функцию возведения числа в степень. Формат: function power(val, pow), где val — заданное число, pow –— степень.
function part_9() {
    function power(val, pow) {
        if (pow === 1) return val;
        return val * power(val, pow-1);
    }

    console.log('--- part_9');
    console.log(`2^8 = ${power(2, 8)}`); // 256
    console.log(`6^9 = ${power(6, 9)}`); // 10 077 696
}


part_1();
part_2();
part_3();
part_4();
part_7();
part_8();
part_9();