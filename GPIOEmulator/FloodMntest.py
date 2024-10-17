import EmulatorGUI as GPIO  # Giả lập chân GPIO
import time
import pnhLCD1602 as lcd  # Thư viện để điều khiển LCD

# Khởi tạo màn hình LCD
lcd = lcd.LCD1602()

# Thiết lập GPIO cho cảm biến HC-SR04
TRIG = 23  # Chân TRIG của cảm biến
ECHO = 24  # Chân ECHO của cảm biến
BUTTON = 25  # Chân GPIO giả lập để kiểm tra (ví dụ nút nhấn giả lập)

# Cài đặt chân TRIG là output và chân ECHO, BUTTON là input
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Giả lập nút nhấn

# Ngưỡng an toàn (khoảng cách mực nước an toàn)
safe_threshold = 30.0  # cm

# Hàm đo khoảng cách từ cảm biến HC-SR04
def measure_distance():
    # Gửi xung TRIG
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # Xung kích hoạt 10 microseconds
    GPIO.output(TRIG, False)

    # Tính thời gian phản hồi của ECHO
    pulse_start = time.time()
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    pulse_end = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Tính khoảng cách dựa trên thời gian
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Công thức tính khoảng cách
    distance = round(distance, 2)  # Làm tròn đến 2 chữ số thập phân

    return distance

# Hàm hiển thị thông báo lên màn hình LCD
def display_message(distance):
    lcd.clear()  # Xóa nội dung trên màn hình trước khi hiển thị mới
    lcd.print_lcd("Khoang cach: {:.2f} cm".format(distance))  # In thông báo lên màn hình

    # Nếu khoảng cách nhỏ hơn ngưỡng an toàn -> cảnh báo lũ lụt
    if distance < safe_threshold:
        lcd.print_lcd("\nCanh bao lu lut!")
    else:
        lcd.print_lcd("\nTinh trang an toan")

try:
    while True:
        # Kiểm tra nút nhấn (hoặc tín hiệu giả lập khác)
        if GPIO.input(BUTTON) == GPIO.HIGH:
            # Đo khoảng cách từ cảm biến khi có tín hiệu từ nút nhấn
            distance = measure_distance()
            print(f"Khoang cach hien tai: {distance} cm")

            # Hiển thị thông điệp dựa trên khoảng cách
            display_message(distance)

        # Chờ một giây trước khi thực hiện lại
        time.sleep(1)

except KeyboardInterrupt:
    print("Ngat chuong trinh!")
    GPIO.cleanup()  # Đảm bảo các chân GPIO được tắt đúng cách
