const SensorData = require('../models/Sensor');

const handleMessage = (topic, message) => {
  console.log(`Received message: ${message.toString()} on topic: ${topic}`);
  // Chuyển đổi message từ buffer sang JSON
  const data = JSON.parse(message.toString());

  // Lưu trữ dữ liệu vào MongoDB
  const newData = new SensorData({
    data: data
  });

  newData.save()
    .then(() => console.log('Data saved to MongoDB'.yellow.bold))
    .catch(err => console.error('Error saving data to MongoDB:'.red.bold, err));
};

module.exports = handleMessage;
