import EmulatorGUI as GPIO
import time

# Thiết lập chế độ và chân GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led_pin = 18  # Chân GPIO để điều khiển LED
GPIO.setup(led_pin, GPIO.OUT)

try:
    while True:
        # Bật đèn LED
        GPIO.output(led_pin, GPIO.HIGH)
        print("LED ON")
        time.sleep(1)  # Giữ đèn LED bật trong 1 giây

        # Tắt đèn LED
        GPIO.output(led_pin, GPIO.LOW)
        print("LED OFF")
        time.sleep(1)  # Giữ đèn LED tắt trong 1 giây

except KeyboardInterrupt:
    print("Ngắt chương trình")
    GPIO.cleanup()  # Xóa cài đặt GPIO
