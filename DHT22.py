#Phạm Ngọc Hưng
#Thư viện mô phỏng cảm biến DHT22
#Nhiệt độ trong khoảng: 20 đến 30 độ C
#Độ ẩm trong khoảnh: 40% đến 60%
#Trễ 0.5 giây mỗi lần đọc (có thể điều chỉnh thờ gian này)

import random
import time

class DHT22:
    def __init__(self, pin):
        self.pin = pin

    def read(self):
        # Giả lập giá trị nhiệt độ và độ ẩm
        temperature = random.uniform(20.0, 30.0)  # Nhiệt độ từ 20 đến 30 độ C
        humidity = random.uniform(40.0, 60.0)      # Độ ẩm từ 40% đến 60%
        
        # Thời gian giả lập để đọc dữ liệu (0.5 giây)
        time.sleep(0.5)
        
        return temperature, humidity

# Hàm đọc nhiệt độ, độ ẩm
def readSensor(pin):
    sensor = DHT22(pin)
    return sensor.read()