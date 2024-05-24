const cron = require('node-cron');
const SensorData = require('../models/Sensor');
const Uptime = require('../models/Uptime');
const mongoose = require('mongoose');

// Hàm để tính tổng thời gian bật cho một thiết bị trong một ngày
const calculateDeviceUptime = async (deviceField, startDate) => {
  const data = await SensorData.find({
    time: {
      $gte: startDate
    }
  }).sort({ time: 1 });

  let totalUptime = 0;
  let isDeviceOn = false;
  let lastTimestamp = null;
  let lastDocumentTime = null;

  data.forEach(doc => {
    const deviceStatus = doc.data[deviceField] > 0; // Kiểm tra nếu thiết bị đang bật
    const currentTime = new Date(doc.time);

    // console.log(`Document time: ${doc.time}, Device status: ${deviceStatus}`);

    if (deviceStatus) {
      if (!isDeviceOn) {
        isDeviceOn = true;
        lastTimestamp = currentTime;
        // console.log(`Device turned on at: ${lastTimestamp}`);
      }
    } else {
      if (isDeviceOn) {
        isDeviceOn = false;
        if (lastTimestamp) {
          totalUptime += (currentTime - lastTimestamp);
        //   console.log(`Device turned off at: ${currentTime}, Uptime added: ${(currentTime - lastTimestamp) / 1000 / 60} minutes`);
          lastTimestamp = null;
        }
      }
    }
    lastDocumentTime = currentTime;
  });

  if (isDeviceOn && lastTimestamp && lastDocumentTime) {
    totalUptime += (lastDocumentTime - lastTimestamp);
    // console.log(`Device still on at lastDocumentTime: ${lastDocumentTime}, Uptime added: ${(lastDocumentTime - lastTimestamp) / 1000 / 60} minutes`);
  }

  const totalUptimeMinutes = totalUptime / 1000 / 60;
  console.log(`Total Uptime for ${deviceField}: ${totalUptimeMinutes} minutes`);

  return totalUptimeMinutes; 
};

// Hàm cập nhật thời gian hoạt động
// Hàm cập nhật thời gian hoạt động
const updateDeviceUptime = async () => {
    console.log('updateDeviceUptime called');
    const now = new Date();
    const startDate = new Date(now);
    startDate.setHours(0, 0, 0, 0); // Bắt đầu từ 00:00:00 của ngày hôm nay
  
    try {
      const lightOnTime = await calculateDeviceUptime('light_on', startDate);
      const fanOnTime = await calculateDeviceUptime('fan_on', startDate);
  
      // Lưu kết quả vào cơ sở dữ liệu
      const updateData = {
        date: startDate,
        lightOnTime,
        fanOnTime
      };
  
      console.log('Preparing to update data:', updateData);
  
      const existingData = await Uptime.findOne({ date: startDate });
      if (existingData) {
        console.log('Existing data found, updating:', existingData);
        existingData.lightOnTime = lightOnTime;
        existingData.fanOnTime = fanOnTime;
        await existingData.save();
        console.log('Existing data updated successfully');
      } else {
        console.log('No existing data found, creating new entry');
        const newData = new Uptime(updateData);
        await newData.save();
        console.log('New data saved successfully');
      }
  
      console.log('Device uptime updated:', updateData);
    } catch (err) {
      console.error('Error in updateDeviceUptime:', err);
    }
  };
// Thiết lập cron job để cập nhật mỗi phút
cron.schedule('* * * * *', updateDeviceUptime);
