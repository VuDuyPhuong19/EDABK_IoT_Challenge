const express = require('express');
const router = express.Router();
const mqttClient = require('../mqtt/connect');

// Endpoint để publish message
router.post('/publish', (req, res) => {
  const { topic, message } = req.body;

  try {
    if (mqttClient.isConnected()) {
      mqttClient.publish(topic, message, { qos: 2 }, (err) => {
        if (err) {
          return res.status(500).send({ message: 'Failed to publish message' });
        }
        res.status(200).send({ message: 'Message published successfully' });
      });
    } else {
      res.status(500).send({ message: 'MQTT client is not connected' });
    }
  } catch (error) {
    res.status(500).send({ message: 'Error publishing MQTT message', error });
  }
});

module.exports = router;
