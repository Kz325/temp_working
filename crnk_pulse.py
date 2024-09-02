import RPi.GPIO as GPIO
import time
import threading

# GPIOの設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)

# 初期状態をHiに設定
GPIO.output(25, GPIO.HIGH)

# 周波数を格納する変数
frequency = 1000  # 初期周波数を1kHzに設定

# 制御パターン（1の時だけLoにする）
#control_pattern = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
crnk_pattern = [0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
cam_pattern  = [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def control_gpio25():
	global frequency
	while True:
		period = 1.0 / frequency
		segment_time = period / 36
		off_time = 10e-6  # 10マイクロ秒

		for i in range(36):
			if crnk_pattern[i] == 1:
				GPIO.output(25, GPIO.LOW)
				time.sleep(off_time)
				GPIO.output(25, GPIO.HIGH)
			time.sleep(segment_time - off_time if crnk_pattern[i] == 1 else segment_time)

def change_frequency(new_frequency):
	global frequency
	frequency = new_frequency

try:
	# GPIO制御スレッドを開始
	control_thread = threading.Thread(target=control_gpio25)
	control_thread.start()

	# 周波数変更の例
	time.sleep(5)  # 5秒後に周波数を変更
	change_frequency(2000)	# 周波数を2kHzに変更
	time.sleep(5)  # さらに5秒後に周波数を変更
	change_frequency(500)  # 周波数を500Hzに変更

except KeyboardInterrupt:
	pass
finally:
	GPIO.cleanup()

