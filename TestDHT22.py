# Thử nghiệm DHT22
from DHT22 import readSensor

pin = 4  # Số pin mà bạn sẽ sử dụng
print("Bắt đầu đọc nhiệt độ, độ ẩm...")
temperature, humidity = readSensor(pin)
print(f"Nhiệt độ: {temperature:.2f} °C")
print(f"Độ ẩm: {humidity:.2f} %")

input("Nhấn phím Enter để kết thúc")