import sensor
import time
import pyb

# === Camera Setup ===
sensor.reset()
sensor.set_pixformat(sensor.RGB565) # or GRAYSCALE
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)

clock = time.clock()
img_counter = 0

while(True):
    clock.tick()
    img = sensor.snapshot()

    # Save full image
    filename = "/frame_%d.jpg" % img_counter
    img.save(filename)
    print("Saved full frame:", filename)

    img_counter += 1

    pyb.delay(5000)  # Capture every 5 seconds, adjust as needed
