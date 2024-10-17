from pnhLCD1602 import LCD1602
import pygame

if __name__ == "__main__":

    lcd = LCD1602()

    try:

        lcd.clear()
        # Hiển thị cả hai dòng cùng lúc
        lcd.write_string("TIEU DE VAN BAN")
        lcd.set_cursor(1, 0)  # Đặt con trỏ ở dòng thứ 2
        lcd.write_string("9999999999999989")
        pygame.time.delay(3000)  # Hiển thị trong 3 giây
        lcd.backlight_off()
        pygame.time.delay(1000)
        lcd.backlight_on()
        pygame.time.delay(1000)
        lcd.home()
        pygame.time.delay(2000)
    finally:
        lcd.close()