from EmulatorGUI import GPIO
import time
import random
import traceback
import requests
import threading
from pnhLCD1602 import LCD1602  # Import thư viện LCD

# API Key của ThingSpeak
THINGSPEAK_API_KEY = "EBTUOCJ48KO0KBHI"  # Thay thế bằng API Key của bạn
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# Khởi tạo màn hình LCD cho từng trạm
lcd_thuong_nguon = LCD1602()
lcd_trung_nguon = LCD1602()
lcd_ha_nguon = LCD1602()

# Hàm gửi dữ liệu lên ThingSpeak
def send_data_to_thingspeak(water_level, location, lcd):
    payload = {"api_key": THINGSPEAK_API_KEY, 'field1': water_level, 'field2': location}
    try:
        response = requests.get(THINGSPEAK_URL, params=payload)
        if response.status_code == 200:
            lcd.write_string(f"{location}: Sent OK", line=1)
            print(f"Sent data from {location} successfully: {water_level} cm")
        else:
            lcd.write_string(f"{location}: Send Fail", line=1)
            print(f"Sending data from {location} failed. Response code: {response.status_code}")
    except Exception as e:
        lcd.write_string(f"{location}: Error!", line=1)
        print(f"Error sending data from {location}: {str(e)}")

# Hàm tạo dữ liệu ngẫu nhiên cho mực nước
def generate_water_level():
    return random.uniform(0.0, 100.0)  # Mực nước từ 0 đến 100 cm

# Hàm hiển thị dữ liệu mực nước lên LCD
def display_lcd_data(lcd, water_level, location):
    lcd.clear()
    if water_level <= 20.0:
        lcd.write_string(f"{location}: Danger", line=0)  # Hiển thị trên dòng đầu tiên
        lcd.write_string(f"{water_level:.1f} cm", line=1)  # Hiển thị trên dòng thứ hai
    else:
        lcd.write_string(f"{location}:", line=0)
        lcd.write_string(f"Level: {water_level:.1f} cm", line=1)  # Hiển thị theo từng dòng

# Hàm xử lý dữ liệu cho từng trạm
def monitor_station(station_name, lcd):
    try:
        while True:
            # Giả lập lấy dữ liệu mực nước
            water_level = generate_water_level()
            display_lcd_data(lcd, water_level, station_name)
            send_data_to_thingspeak(water_level, station_name, lcd)
            time.sleep(15)  # Đợi 15 giây trước khi lấy dữ liệu mới
    except Exception as ex:
        traceback.print_exc()

# Khởi tạo các luồng cho từng trạm quan sát
def Main():
    try:
        # Thiết lập GPIO cho các cảm biến và đèn cảnh báo ở mỗi trạm (nếu cần)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.OUT)
        GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)

        # Tạo các luồng riêng biệt cho từng trạm
        thuong_nguon_thread = threading.Thread(target=monitor_station, args=("Thượng nguồn", lcd_thuong_nguon))
        trung_nguon_thread = threading.Thread(target=monitor_station, args=("Trung nguồn", lcd_trung_nguon))
        ha_nguon_thread = threading.Thread(target=monitor_station, args=("Hạ nguồn", lcd_ha_nguon))

        # Khởi động các luồng
        thuong_nguon_thread.start()
        trung_nguon_thread.start()
        ha_nguon_thread.start()

        # Chờ các luồng hoàn thành (chúng sẽ chạy liên tục trong khi hệ thống đang hoạt động)
        thuong_nguon_thread.join()
        trung_nguon_thread.join()
        ha_nguon_thread.join()

    except Exception as ex:
        traceback.print_exc()
    finally:
        GPIO.cleanup()

# Bắt đầu chương trình chính
if __name__ == "__main__":
    Main()
