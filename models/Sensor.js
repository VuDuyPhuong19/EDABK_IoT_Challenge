// const mongoose = require('mongoose');
// const { format } = require('date-fns');
// const timestamp = format(new Date(), 'yyyy-MM-dd HH:mm:ss');

// // Tạo schema và model cho sensor data
// const sensorSchema = new mongoose.Schema({
//     data: mongoose.Schema.Types.Mixed,
//     timestamp: {
//         type: String,
//         default: timestamp
//     }
// });

// module.exports = mongoose.model('SensorData', sensorSchema);

const mongoose = require('mongoose');

// Sử dụng định dạng thời gian Date để đảm bảo nhất quán
const sensorSchema = new mongoose.Schema({
  data: mongoose.Schema.Types.Mixed,
  time: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model('SensorData', sensorSchema);


