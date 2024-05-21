const mqtt = require('mqtt');
const path = require('path');
require('dotenv').config({path: path.resolve(__dirname, './config.env')});

const connectMQTT = () => {
    const mqttClient = mqtt.connect(process.env.MQTT_BROKER_URL, {
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

    mqttClient.on('error', (err) => {
        console.error('Connection error:'.red.bold, err);
    });

    return mqttClient;
};

module.exports = connectMQTT;
