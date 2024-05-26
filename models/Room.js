const mongoose = require('mongoose');

const RoomSchema = new mongoose.Schema({
    roomName: {
        type: String,
        required: true
    },
    roomImage: {
        type: String,
        required: true
    }
    // roomDetail: {
    //     type: String,
    //     required: true
    // }
});

const Room = mongoose.model('Room', RoomSchema);
module.exports = Room;
