import asyncio
from bleak import BleakScanner, BleakClient

def notification_handler(sender, data):
    """ Xử lý dữ liệu nhận được từ notification và ghi vào file. """
    data_str = f"Notification from {sender}: {data}\n"
    print(data_str.strip())  # In ra màn hình để theo dõi
    with open("notifications_test1.txt", "a") as file:
        file.write(data_str)

async def main():
    # Quét các thiết bị BLE xung quanh
    print("Scanning for devices...")
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Device: {device.name}, {device.address}")

    # Địa chỉ của BGM220P
    bgm220p_address = "80:4B:50:56:8D:7D"

    # Kết nối với thiết bị BGM220P
    async with BleakClient(bgm220p_address) as client:
        connected = client.is_connected
        print(f"Connected: {connected}")

        # UUID của đặc điểm bạn muốn nhận thông báo
        characteristic_uuid = "61a885a4-41c3-60d0-9a53-6d652a70d29c"
        
        # Bật notifications cho đặc điểm
        await client.start_notify(characteristic_uuid, notification_handler)
        
        # Đặt lệnh để thu thập notifications mà không tự động dừng
        print("Collecting notifications indefinitely...")
        while True:
            await asyncio.sleep(0.5)  # Thay đổi tần số kiểm tra

        # Tắt notifications (không bao giờ chạy tới đây nếu không có điều kiện dừng khác)
        await client.stop_notify(characteristic_uuid)

# Chạy hàm main
asyncio.run(main())
