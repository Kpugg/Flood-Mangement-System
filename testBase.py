# from EmulatorGUI import GPIO
# import time
# import random
# import traceback
# import requests
# from pnhLCD1602 import LCD1602  # Import thư viện LCD

# # API Key của ThingSpeak
# THINGSPEAK_API_KEY = "EBTUOCJ48KO0KBHI"  # Thay thế bằng API Key của bạn
# THINGSPEAK_URL = "https://api.thingspeak.com/update"

# # Khởi tạo màn hình LCD
# lcd = LCD1602()

# def generate_water_level():
#     # Hàm tạo dữ liệu ngẫu nhiên cho mực nước (giả định đơn vị là cm)
#     water_level = random.uniform(0.0, 100.0)  # Mực nước trong khoảng từ 0 đến 100 cm
#     return water_level

# def display_lcd_data(water_level):
#     # Hiển thị dữ liệu mực nước lên LCD
#     if water_level <= 20.0:
#         lcd.write_string("DANGEROUS!   ")
#         lcd.set_cursor(0, 1)  # Di chuyển đến dòng thứ 2
#         lcd.write_string(f"Level: {water_level:.1f} mm")  # Hiển thị mực nước với 1 chữ số sau dấu phẩy
#     else:
#         if water_level < 100:  # Kiểm tra để không bị lấn sang dòng kế tiếp
#             lcd.write_string(f"Water Level: {water_level:.1f} mm   ")  # Hiển thị mực nước
#         else:
#             lcd.write_string("Water Level: 100mm   ")  # Giới hạn trên là 100mm
#         lcd.set_cursor(0, 1)  # Di chuyển đến dòng thứ 2


# def send_data_to_thingspeak(water_level):
#     # Tạo payload gửi dữ liệu lên ThingSpeak
#     payload = {"api_key": THINGSPEAK_API_KEY, 'field1': water_level}
#     try:
#         response = requests.get(THINGSPEAK_URL, params=payload)
#         if response.status_code == 200:
#             print(f"Sending data successfully: {water_level} mm")
#         else:
#             print(f"Sending data failed. Response code: {response.status_code}")
#     except Exception as e:
#         print(f"Error sending data to ThingSpeak: {str(e)}")

# def Main():
#     system_running = False  # Biến để theo dõi trạng thái hoạt động của hệ thống

#     try:
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setwarnings(False)

#         # Setup chân cho Flow Meter YF-S201
#         GPIO.setup(4, GPIO.IN)  # SIG của Flow Meter (chân 4)

#         # Setup chân cho cảm biến rg11 rain sensor
#         GPIO.setup(22, GPIO.IN) # NO của rg11
#         # Setup các chân GPIO cho JSN-SR04T và LCD
#         GPIO.setup(14, GPIO.IN)  # ECHO của JSN-SR04T
#         GPIO.setup(15, GPIO.OUT)  # TRIG của JSN-SR04T
#         GPIO.setup(20, GPIO.OUT)  # SDA của LCD
#         GPIO.setup(21, GPIO.OUT)  # SCL của LCD

#         # Chân cho nút nhấn start và stop
#         GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Nút nhấn bắt đầu
#         GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Nút nhấn dừng

#         while True:
#             # Kiểm tra nếu nút nhấn start được nhấn
#             if GPIO.input(17) == GPIO.LOW:
#                 system_running = True
#                 print("System started")

#             # Kiểm tra nếu nút nhấn stop được nhấn
#             if GPIO.input(18) == GPIO.LOW:
#                 system_running = False
#                 lcd.clear()  # Xóa màn hình LCD khi dừng
#                 print("System stopped")

#             # Nếu hệ thống đang chạy, sinh dữ liệu ngẫu nhiên và hiển thị
#             if system_running:
#                 water_level = generate_water_level()
#                 display_lcd_data(water_level)
#                 send_data_to_thingspeak(water_level)
#                 time.sleep(1)
#             else:
#                 time.sleep(0.1)  # Nếu hệ thống không chạy, nghỉ ngắn để tiết kiệm tài nguyên

#     except Exception as ex:
#         traceback.print_exc()
#     finally:
#         GPIO.cleanup()  # Đảm bảo giải phóng GPIO khi thoát

# # Bắt đầu chương trình chính
# Main()

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

def generate_flow_rate():
    # Hàm tạo dữ liệu ngẫu nhiên cho lưu lượng (giả định đơn vị là m³/s)
    flow_rate = random.uniform(250.0, 600.0)  # Lưu lượng trong khoảng từ 250 đến 600 m³/s
    return flow_rate

def generate_rainfall():
    # Hàm tạo dữ liệu ngẫu nhiên cho lưu lượng mưa (giả định đơn vị là mm/h)
    rainfall = random.uniform(0.0, 50.0)  # Lưu lượng mưa trong khoảng từ 0 đến 50 mm/h
    return rainfall

def display_data(water_level, flow_rate, rainfall):
    # Hiển thị dữ liệu lên LCD
    lcd.clear()

    # Hiển thị mực nước
    if water_level <= 20.0:
        lcd.write_string("WATER DANGEROUS!")
    else:
        lcd.write_string(f"Water Level: {water_level:.1f} cm   ")

    lcd.set_cursor(0, 1)  # Di chuyển đến dòng thứ 2

    # Hiển thị lưu lượng và kiểm tra cảnh báo
    if water_level <= 20.0:
        if flow_rate >= 300 and flow_rate < 400:
            lcd.write_string("Flow: 300 m³/s   Warning Level 1")
        elif flow_rate >= 400 and flow_rate < 500:
            lcd.write_string("Flow: 400 m³/s   Warning Level 2")
        elif flow_rate >= 500:
            lcd.write_string("Flow: 500 m³/s   Warning Level 3")
        else:
            lcd.write_string("Flow: Normal")
    else:
        lcd.write_string(f"Flow: {flow_rate:.1f} m³/s  ")

    # Xử lý cảnh báo lũ từ lưu lượng mưa
    if rainfall >= 30.0:
        lcd.write_string("Heavy Rain Alert!")
    elif rainfall >= 20.0:
        lcd.write_string("Moderate Rain Alert!")
    elif rainfall >= 10.0:
        lcd.write_string("Light Rain Alert!")

def send_data_to_thingspeak(water_level, flow_rate, rainfall):
    # Tạo payload gửi dữ liệu lên ThingSpeak
    payload = {
        "api_key": THINGSPEAK_API_KEY,
        'field1': water_level,
        'field2': flow_rate,
        'field3': rainfall
    }
    try:
        response = requests.get(THINGSPEAK_URL, params=payload)
        if response.status_code == 200:
            print(f"Sending data successfully: {water_level} cm, {flow_rate} m³/s, {rainfall} mm/h")
        else:
            print(f"Sending data failed. Response code: {response.status_code}")
    except Exception as e:
        print(f"Error sending data to ThingSpeak: {str(e)}")

def Main():
    system_running = False  # Biến để theo dõi trạng thái hoạt động của hệ thống

    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Setup các chân GPIO cho JSN-SR04T và LCD
        GPIO.setup(14, GPIO.IN)  # ECHO của JSN-SR04T
        GPIO.setup(15, GPIO.OUT)  # TRIG của JSN-SR04T
        GPIO.setup(20, GPIO.OUT)  # SDA của LCD
        GPIO.setup(21, GPIO.OUT)  # SCL của LCD

        # Chân cho nút nhấn start và stop
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Nút nhấn bắt đầu
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Nút nhấn dừng

        while True:
            # Kiểm tra nếu nút nhấn start được nhấn
            if GPIO.input(17) == GPIO.LOW:
                system_running = True
                print("System started")

            # Kiểm tra nếu nút nhấn stop được nhấn
            if GPIO.input(18) == GPIO.LOW:
                system_running = False
                lcd.clear()  # Xóa màn hình LCD khi dừng
                print("System stopped")

            # Nếu hệ thống đang chạy, sinh dữ liệu ngẫu nhiên và hiển thị
            if system_running:
                water_level = generate_water_level()
                flow_rate = generate_flow_rate()  # Sinh dữ liệu lưu lượng ngẫu nhiên
                rainfall = generate_rainfall()  # Sinh dữ liệu lưu lượng mưa ngẫu nhiên
                display_data(water_level, flow_rate, rainfall)
                send_data_to_thingspeak(water_level, flow_rate, rainfall)
                time.sleep(1)
            else:
                time.sleep(0.1)  # Nếu hệ thống không chạy, nghỉ ngắn để tiết kiệm tài nguyên

    except Exception as ex:
        traceback.print_exc()
    finally:
        GPIO.cleanup()  # Đảm bảo giải phóng GPIO khi thoát

# Bắt đầu chương trình chính
Main()
