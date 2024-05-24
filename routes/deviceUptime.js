// const express = require('express');
// const SensorData = require('../models/Sensor');
// const router = express.Router();

// // Hàm để tính tổng thời gian bật cho một thiết bị trong một ngày
// const calculateDeviceUptime = async (deviceField, startDate) => {
//   const data = await SensorData.find({
//     time: {
//       $gte: startDate
//     }
//   }).sort({ time: 1 }); // Sắp xếp theo thời gian tăng dần

//   let totalUptime = 0;
//   let isDeviceOn = false;
//   let lastTimestamp = null;
//   let lastDocumentTime = null;

//   data.forEach(doc => {
//     const deviceStatus = doc.data[deviceField] > 0; // Kiểm tra nếu thiết bị đang bật
//     const currentTime = new Date(doc.time);

//     console.log(`Document time: ${doc.time}, Device status: ${deviceStatus}`);

//     if (deviceStatus) {
//       if (!isDeviceOn) {
//         // Bật thiết bị
//         isDeviceOn = true;
//         lastTimestamp = currentTime;
//         console.log(`Device turned on at: ${lastTimestamp}`);
//       }
//     } else {
//       if (isDeviceOn) {
//         // Tắt thiết bị
//         isDeviceOn = false;
//         if (lastTimestamp) {
//           totalUptime += (currentTime - lastTimestamp);
//           console.log(`Device turned off at: ${currentTime}, Uptime added: ${(currentTime - lastTimestamp) / 1000 / 60} minutes`);
//           lastTimestamp = null;
//         }
//       }
//     }
//     lastDocumentTime = currentTime;
//   });

//   // Nếu thiết bị vẫn đang bật khi kết thúc khoảng thời gian
//   if (isDeviceOn && lastTimestamp && lastDocumentTime) {
//     totalUptime += (lastDocumentTime - lastTimestamp);
//     console.log(`Device still on at lastDocumentTime: ${lastDocumentTime}, Uptime added: ${(lastDocumentTime - lastTimestamp) / 1000 / 60} minutes`);
//   }

//   // Chuyển đổi tổng thời gian từ mili giây sang phút
//   const totalUptimeMinutes = totalUptime / 1000 / 60; // Chuyển đổi mili giây thành phút
//   console.log(`Total Uptime for ${deviceField}: ${totalUptimeMinutes} minutes`); // Logging for debugging

//   return totalUptimeMinutes; 
// };

// router.get('/device-uptime', async (req, res) => {
//   try {
//     // Đặt thời gian bắt đầu cụ thể
//     // const startDate = new Date('2024-05-23T00:00:00Z'); // Thời gian bắt đầu cố định
//     const now = new Date();
//     const startDate = new Date(now);
//     startDate.setHours(0, 0, 0, 0); // Bắt đầu từ 00:00:00 của ngày hôm nay

//     const lightOnTime = await calculateDeviceUptime('light_on', startDate);
//     const fanOnTime = await calculateDeviceUptime('fan_on', startDate);

//     res.json({
//       lightOnTime,
//       fanOnTime
//     });
//   } catch (err) {
//     res.status(500).json({ message: err.message });
//   }
// });

// module.exports = router;

const express = require('express');
const Uptime = require('../models/Uptime');
const router = express.Router();

// Hàm để lấy dữ liệu 7 ngày
const getWeeklyData = async () => {
  const now = new Date();
  const startDate = new Date(now);
  startDate.setDate(now.getDate() - 6); // Lấy dữ liệu từ 6 ngày trước đến hôm nay
  startDate.setHours(0, 0, 0, 0);

  const data = await Uptime.find({
    date: {
      $gte: startDate,
      $lt: now
    }
  }).sort({ date: 1 }); // Sắp xếp theo ngày tăng dần

  const result = [];
  // for (let i = 0; i < 7; i++) {
  //   const date = new Date(now);
  //   date.setDate(now.getDate() - i);
  //   date.setHours(0, 0, 0, 0);

  //   const dayData = data.find(d => d.date.getTime() === date.getTime());
  //   result.push({
  //     date,
  //     lightOnTime: dayData ? dayData.lightOnTime : 0,
  //     fanOnTime: dayData ? dayData.fanOnTime : 0
  //   });
  // }
  for (let i = 0; i < 7; i++) {
    const date = new Date(now);
    date.setDate(now.getDate() - i);
    date.setHours(0, 0, 0, 0);

    const dayData = data.find(d => d.date.getTime() === date.getTime());
    const lightOnTime = dayData ? dayData.lightOnTime : 0;
    const fanOnTime = dayData ? dayData.fanOnTime : 0;

    console.log(`Date: ${date}, Light On Time: ${lightOnTime} minutes, Fan On Time: ${fanOnTime} minutes`);

    result.push({
      date,
      lightOnTime,
      fanOnTime
    });
  }

  return result.reverse(); // Đảo ngược để hiển thị từ ngày cũ đến ngày mới
};

router.get('/weekly-uptime', async (req, res) => {
  try {
    const weeklyData = await getWeeklyData();
    res.json(weeklyData);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

module.exports = router;


