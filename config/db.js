const mongoose = require('mongoose');
const path = require('path');
require('colors');
require('dotenv').config({path: path.resolve(__dirname, './config.env')});

const connectDB = async () => {
  try {
    // const conn = await mongoose.connect(process.env.MONGODB_URI);
    const conn = await mongoose.connect('mongodb+srv://vuduyphuong:Phuong153280@vuduyphuong.odzmo8u.mongodb.net/sensor?retryWrites=true&w=majority&appName=vuduyphuong');
    console.log(`MongoDB connected: ${conn.connection.host}`.green.bold);
  } catch (err) {
    console.error(`Error: ${err.message}`.red.bold);
    process.exit(1); // Dừng ứng dụng nếu không thể kết nối
  }
}

module.exports = connectDB;
