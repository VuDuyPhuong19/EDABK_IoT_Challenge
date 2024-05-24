const express = require('express');
const bodyParser = require('body-parser');
const connectDB = require('./config/db');
const connectMQTT = require('./config/mqtt');
const path = require('path');
require('dotenv').config({path: path.resolve(__dirname, '.config/config.env')});

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.json({
  extended: true
}));

// Connect to MongoDB 
connectDB();
// Connect to HiveMQ 
connectMQTT();

// Routes cho User
app.use(require('./routes/user'));

// Route cho MQTT
// app.use(require('./routes/mqtt'));

// Route cho dữ liệu cảm biến
app.use(require('./routes/sensor'));

// Route cho phân tích dữ liệu
app.use (require('./routes/deviceUptime'));

// Khởi động cron jobs
require('./schedules/cronJobs');

// Route cho thêm room trên app
app.use(require('./routes/room'));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`.green.bold));

