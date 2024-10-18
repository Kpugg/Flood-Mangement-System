from EmulatorGUI import GPIO
import time
import random
import traceback
import requests
from pnhLCD1602 import LCD1602  # Import thư viện LCD

# API Key của ThingSpeak
THINGSPEAK_API_KEY = "EBTUOCJ48KO0KBHI"  # Thay thế bằng API Key của bạn
THINGSPEAK_URL = "https://api.thingspeak.com/update"


# Khởi tạo màn hình LCD
lcd = LCD1602()

def generate_water_level():
    # Hàm tạo dữ liệu ngẫu nhiên cho mực nước (giả định đơn vị là cm)
    water_level = random.uniform(0.0, 100.0)  # Mực nước trong khoảng từ 0 đến 100 cm
    return water_level

def display_lcd_data(water_level):
    # Hiển thị dữ liệu mực nước lên LCD
    lcd.clear()
    # Kiểm tra mực nước có đạt mức cảnh báo nguy hiểm hay không
    if water_level <= 20.0:
        lcd.write_string("DANGEROUS!")
        lcd.write_string(f"{water_level:.1f} m")  # Hiển thị mực nước với 1 chữ số sau dấu phẩy
    else:
        lcd.write_string("Water Level:")
        lcd.write_string(f"{water_level:.1f} m") # Hiển thị mực nước với 1 chữ số sau dấu phẩy

def send_data_to_thingspeak(water_level):
    # Tạo payload gửi dữ liệu lên ThingSpeak
    payload = {"api_key": THINGSPEAK_API_KEY, 'field1': water_level}
    try:
        response = requests.get(THINGSPEAK_URL, params=payload)
        if response.status_code == 200:
            print(f"Sending data successfully: {water_level} m")
        else:
            print(f"Sending data failed. Response code: {response.status_code}")
    except Exception as e:
        print(f"Error sending data to ThingSpeak: {str(e)}")

def Main():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Setup các chân GPIO
        GPIO.setup(4, GPIO.OUT)
        GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(21, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(26, GPIO.IN)

        while True:
            # Nếu có tín hiệu từ chân 23 (giả lập nút nhấn), hiển thị dữ liệu random về mực nước
            if GPIO.input(23) == False:
                GPIO.output(4, GPIO.HIGH)
                GPIO.output(17, GPIO.HIGH)
                water_level = generate_water_level()
                display_lcd_data(water_level)
                time.sleep(1)

            if GPIO.input(15) == True:
                GPIO.output(18, GPIO.HIGH)
                GPIO.output(21, GPIO.HIGH)
                water_level = generate_water_level()
                display_lcd_data(water_level)
                send_data_to_thingspeak(water_level)
                time.sleep(1)

            if GPIO.input(24) == True:
                GPIO.output(18, GPIO.LOW)
                GPIO.output(21, GPIO.LOW)
                lcd.clear()  # Xóa màn hình LCD khi không cần hiển thị dữ liệu
                time.sleep(1)

            if GPIO.input(26) == True:
                GPIO.output(4, GPIO.LOW)
                GPIO.output(17, GPIO.LOW)
                lcd.clear()  # Xóa màn hình LCD khi không cần hiển thị dữ liệu
                time.sleep(1)

    except Exception as ex:
        traceback.print_exc()
    finally:
        GPIO.cleanup()  # Đảm bảo giải phóng GPIO khi thoát

# Bắt đầu chương trình chính
Main()
