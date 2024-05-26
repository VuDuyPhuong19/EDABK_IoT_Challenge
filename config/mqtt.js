const mqtt = require('mqtt');
const SensorData = require('../models/Sensor');
const path = require('path');
require('dotenv').config({ path: path.resolve(__dirname, './config.env') });

const connectMQTT = () => {
  // const mqttClient = mqtt.connect(process.env.MQTT_BROKER_URL, {
    const mqttClient = mqtt.connect('mqtts://4cc5961d8ff0416e9956c759300dd3ce.s1.eu.hivemq.cloud:8883', {
    username: process.env.MQTT_USERNAME, // username
    password: process.env.MQTT_PASSWORD, // password
    rejectUnauthorized: true // thêm tùy chọn này nếu không cần xác thực SSL
  });

  mqttClient.on('connect', () => {
    console.log('Connected to MQTT broker'.green.bold);
    mqttClient.subscribe('Device', (err) => {
      if (!err) {
        console.log('Subscribed to topic'.green.bold);
      } else {
        console.error('Error subscribing to topic:'.red.bold, err);
      }
    });
  });

  mqttClient.on('message', async (topic, message) => {
    console.log(`Received message: ${message.toString()} on topic: ${topic}`);
    // Chuyển đổi message từ buffer sang JSON
    const data = JSON.parse(message.toString());

    const newData = new SensorData({ data });
    try {
      await newData.save();
      console.log('Data saved to MongoDB'.yellow.bold);
    } catch (err) {
      console.error('Error saving data to MongoDB:'.red.bold, err);
    }
  });

  mqttClient.on('error', (err) => {
    console.error('Connection error:'.red.bold, err);
  });

  return mqttClient;
};

module.exports = connectMQTT;
