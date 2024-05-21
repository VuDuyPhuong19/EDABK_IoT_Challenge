const mongoose = require('mongoose');
const { format } = require('date-fns');
const timestamp = format(new Date(), 'yyyy-MM-dd HH:mm:ss');

// Tạo schema và model cho sensor data
const sensorSchema = new mongoose.Schema({
    data: mongoose.Schema.Types.Mixed,
    timestamp: {
        type: String,
        default: timestamp
    }
});

module.exports = mongoose.model('SensorData', sensorSchema);