const express = require('express');
const fs = require('fs');
// const bodyParser = require('body-parser'); // 4.16+ уже включен в express
const app = express();

const SERVER_ADDR = 'http://127.0.0.1';
const SERVER_PORT = 3000;
const CART_FILE = 'cart.json';
const LOG_FILE = 'stats.json';

const log_print = (s) => {
  const now = new Date;
  console.log(`[${now.toLocaleString()}] ${s}`);
}

const recreateFile = (fileName) => {
  fs.unlink(fileName, err => {
    if (err) {
      log_print(err);
    } else {
      log_print(`DEL ${fileName}`);
    }
  });
  fs.open(fileName, 'w', (err, file) => {
    if (err) {
      log_print(err);
    } else {
      log_print(`CREATE ${fileName}`);
    }
  });
}

const writeCart = (res, data) =>{
  fs.writeFile(CART_FILE, JSON.stringify(data), (err) => {
      log_print(` ∟ write cart`);
      if (err) {
        res.send('{"result": 0}');
      } else {
        res.send('{"result": 1}');
      }
    });
}

const wtireLog = (productName, action) => {
  const now = (new Date).toLocaleString();
  fs.appendFile(LOG_FILE, `[${now}] ${action} ${productName}\n`, (err) => {
  });
}

app.use(express.static('.'));
app.use(express.json());

app.get('/catalogData', (req, res) => {
  log_print('GET /catalogData');
  fs.readFile('catalog.json', 'utf8', (err, data) => {
    if (err) {
      log_print(err);
    } else {
      log_print(' ∟ send data');
      res.send(data);
    }
  });
})

app.post('/addToCart', ((req, res) => {
  log_print('POST /addToCart');
  const item = req.body;
  fs.readFile(CART_FILE, 'utf8', (err, data) => {
    let cart = [];
    if (data) {
      cart = JSON.parse(data);
    }

    cart.push(item);

    writeCart(res, cart);
    wtireLog(item.product_name, 'add');
  });
}));

app.post('/editCart', ((req, res) => {
  log_print('POST /editCart');
  const item = req.body;
  fs.readFile(CART_FILE, 'utf8', (err, data) => {
    const cart = JSON.parse(data);

    const itemIdx = cart.map(x=> x.id_product).indexOf(item.id_product);
    cart[itemIdx].count = item.count;
    cart[itemIdx].total = item.total;

    writeCart(res, cart);
    wtireLog(cart[itemIdx].product_name, 'edit');
  });
}));

app.post('/delFromCart', ((req, res) => {
  log_print('POST /delFromCart');
  const item = req.body;
  fs.readFile(CART_FILE, 'utf8', (err, data) => {
    const cart = JSON.parse(data);

    const itemIdx = cart.map(x=> x.id_product).indexOf(item.id_product);
    const productName = cart[itemIdx].product_name;
    cart.splice(itemIdx, 1);

    writeCart(res, cart);
    wtireLog(productName, 'del');
  });
}));

app.listen(SERVER_PORT, () => {
  log_print(`Server UP on ${SERVER_ADDR}:${SERVER_PORT}`);
  // пересоздаем файл, чтобы старые покупки не отображались в корзине при добавлении
  recreateFile(CART_FILE);
})