import threading
import time
import RPi.GPIO as GPIO

# --- Motor 1 Pins (BOARD numbering) ---
IN1_M1, IN2_M1, IN3_M1, IN4_M1 = 18, 22, 36, 37

# --- Motor 2 Pins (BOARD numbering) ---
IN1_M2, IN2_M2, IN3_M2, IN4_M2 = 11, 13, 15, 16

# ==========================================
# SPEED CONTROL SETTING (Edit here before running)
# 0.005 = Normal speed
# 0.002 = Fast speed (Don't go below ~0.0015 or it will stall)
# 0.015 = Slow speed
MOTOR_DELAY = 0.025
# ==========================================

# Setup GPIO mode
GPIO.setmode(GPIO.BOARD)

m1_pins = [IN1_M1, IN2_M1, IN3_M1, IN4_M1]
m2_pins = [IN1_M2, IN2_M2, IN3_M2, IN4_M2]

for pin in m1_pins + m2_pins:
  GPIO.setup(pin, GPIO.OUT)

step_sequence = [
    [1, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 0, 1],
]

# State tracking dictionary
status = {"m1_fwd": False, "m1_rev": False, "m2_fwd": False, "m2_rev": False}


def run_motor_continuous(state_key, pin_list, clockwise=True):
  GPIO.setmode(GPIO.BOARD)
  in1, in2, in3, in4 = pin_list
  sequence = step_sequence if clockwise else list(reversed(step_sequence))
  idx = 0

  try:
    while status[state_key]:
      step = sequence[idx % len(sequence)]
      GPIO.output(in1, step[0])
      GPIO.output(in2, step[1])
      GPIO.output(in3, step[2])
      GPIO.output(in4, step[3])
      idx += 1
      time.sleep(MOTOR_DELAY)  # Uses your manually set speed here
  finally:
    GPIO.output(in1, 0)
    GPIO.output(in2, 0)
    GPIO.output(in3, 0)
    GPIO.output(in4, 0)
    status[state_key] = False


def stop_all_motors():
  status["m1_fwd"] = False
  status["m1_rev"] = False
  status["m2_fwd"] = False
  status["m2_rev"] = False


try:
  print("=== Continuous Toggle Motor Control ===")
  print(f"Current Preset Speed Delay: {MOTOR_DELAY}s")
  print("1: Start/Stop Motor 1 (Forward)")
  print("2: Start/Stop Motor 2 (Forward)")
  print("3: Start/Stop Motor 1 (Reverse)")
  print("4: Start/Stop Motor 2 (Reverse)")
  print("5: Exit")

  while True:
    choice = input("\nEnter command (1-5): ").strip()

    if choice == "1":
      if status["m1_fwd"]:
        print("-> Stopping Motor 1 (Forward)...")
        status["m1_fwd"] = False
      else:
        stop_all_motors()
        time.sleep(0.2)
        print("-> Motor 1 RUNNING Forward continuously.")
        status["m1_fwd"] = True
        threading.Thread(
            target=run_motor_continuous,
            args=("m1_fwd", m1_pins, True),
            daemon=True,
        ).start()

    elif choice == "2":
      if status["m2_fwd"]:
        print("-> Stopping Motor 2 (Forward)...")
        status["m2_fwd"] = False
      else:
        stop_all_motors()
        time.sleep(0.2)
        print("-> Motor 2 RUNNING Forward continuously.")
        status["m2_fwd"] = True
        threading.Thread(
            target=run_motor_continuous,
            args=("m2_fwd", m2_pins, True),
            daemon=True,
        ).start()

    elif choice == "3":
      if status["m1_rev"]:
        print("-> Stopping Motor 1 (Reverse)...")
        status["m1_rev"] = False
      else:
        stop_all_motors()
        time.sleep(0.2)
        print("-> Motor 1 RUNNING Reverse continuously.")
        status["m1_rev"] = True
        threading.Thread(
            target=run_motor_continuous,
            args=("m1_rev", m1_pins, False),
            daemon=True,
        ).start()

    elif choice == "4":
      if status["m2_rev"]:
        print("-> Stopping Motor 2 (Reverse)...")
        status["m2_rev"] = False
      else:
        stop_all_motors()
        time.sleep(0.2)
        print("-> Motor 2 RUNNING Reverse continuously.")
        status["m2_rev"] = True
        threading.Thread(
            target=run_motor_continuous,
            args=("m2_rev", m2_pins, False),
            daemon=True,
        ).start()

    elif choice == "5":
      print("Exiting program...")
      stop_all_motors()
      time.sleep(0.2)
      break

    else:
      print("Invalid choice. Please enter a number between 1 and 5.")

except KeyboardInterrupt:
  print("\nStopping motors and cleaning up GPIO...")

finally:
  stop_all_motors()
  time.sleep(0.2)
  GPIO.cleanup()

  