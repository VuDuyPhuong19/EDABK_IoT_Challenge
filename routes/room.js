const express = require('express');
const Room = require('../models/Room');
const router = express.Router();

// Route thêm room
router.post('/add-room', async (req, res) => {
    const { roomName, roomImage } = req.body;
    try {
        const newRoom = new Room({ roomName, roomImage });
        await newRoom.save();
        console.log(`Saved room: ${newRoom}`);
        res.status(201).send(newRoom);
    } catch (error) {
        res.status(400).send(error);
    }
});

// Route lấy danh sách tất cả các phòng
router.get('/rooms', async (req, res) => {
    try {
        const rooms = await Room.find({});
        res.send(rooms);
    } catch (error) {
        res.status(400).send(error);
    }
});

// Route lấy thông tin chi tiết của một phòng
router.get('/rooms/:roomName', async (req, res) => {
    try {
        const room = await Room.findOne({ roomName: req.params.roomName });
        if (!room) {
            return res.status(404).send('Room not found');
        }
        res.send(room);
    } catch (error) {
        res.status(400).send(error);
    }
});

module.exports = router;
