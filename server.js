const express = require('express');
const bodyParser = require('body-parser');
const connectDB = require('./config/db');
const connectMQTT = require('./mqtt/connect');
const handleMessage = require('./mqtt/handleMessage');
const path = require('path');
require('dotenv').config({path: path.resolve(__dirname, '.config/config.env')});

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.json({
  extended: true
}));

// Connect to MongoDB 
connectDB();

app.use(require('./routes/user'));

// Kết nối tới MQTT và thiết lập xử lý tin nhắn
const mqttClient = connectMQTT();
mqttClient.on('message', handleMessage);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`.green.bold));

