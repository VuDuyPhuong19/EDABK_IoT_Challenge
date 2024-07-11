import matplotlib.pyplot as plt
import re

def extract_numbers_from_bytearray(data_string):
    """Trích xuất số từ chuỗi bytearray biểu diễn trong file."""
    numbers = re.findall(r"\\x00(\d+\.\d+)\\x00", data_string)
    return [float(num) for num in numbers if num]

def plot_values(values):
    """Vẽ biểu đồ cho các giá trị được trích xuất."""
    plt.figure(figsize=(10, 5))
    plt.plot(values, marker='o', linestyle='-', color='b')
    plt.title('temperature')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.grid(True)
    plt.show()

# Đọc dữ liệu từ file
with open('notifications_test1.txt', 'r') as file:
    data = file.readlines()

# Trích xuất các giá trị số từ dữ liệu và lọc các giá trị lớn hơn 100
values = []
for line in data:
    numbers = extract_numbers_from_bytearray(line)
    filtered_numbers = [num for num in numbers if num < 100]  # Lọc ra các số nhỏ hơn 100
    values.extend(filtered_numbers)

# Vẽ biểu đồ
plot_values(values)
