const mongoose = require('mongoose');

const uptimeSchema = new mongoose.Schema({
  date: {
    type: Date,
    required: true,
  },
  lightOnTime: {
    type: Number,
    required: true,
  },
  fanOnTime: {
    type: Number,
    required: true,
  },
});

const Uptime = mongoose.model('Uptime', uptimeSchema);
module.exports = Uptime;
