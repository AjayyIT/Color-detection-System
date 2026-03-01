import cv2
import numpy as np
import pandas as pd
import argparse
import time
import os
from datetime import datetime

# Argument parser (optional image path)
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', help="Path to image file (optional)")
args = vars(ap.parse_args())

# Ensure captures folder exists
os.makedirs("captures", exist_ok=True)

# Reading the colors CSV file
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

# Globals
clicked = False
r = g = b = xpos = ypos = 0
current_display = None     # what is currently shown in the window
frozen = False             # whether the feed is frozen
frozen_frame = None        # the frozen frame

# Function to get closest color name
def getColorName(R, G, B):
    minimum = 10**9
    cname = ""
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d < minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# Mouse callback — works on whatever is shown (live or frozen)
def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked, current_display
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        xpos, ypos = x, y

# Determine input source
if args["image"]:
    img = cv2.imread(args["image"])
    if img is None:
        print("❌ Error: Unable to read the image. Check the path.")
        exit()
    mode = "image"
else:
    # Use CAP_DSHOW on Windows to help with camera issues; remove second arg on other OSes if needed
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    time.sleep(1)  # webcam warm-up
    if not cap.isOpened():
        print("❌ Error: Unable to access webcam.")
        exit()
    mode = "camera"

cv2.namedWindow("Color Picker")
cv2.setMouseCallback("Color Picker", draw_function)

print("Controls: [ESC] exit | [c] freeze/unfreeze webcam | [C] capture & save current shown frame")

# Main loop
while True:
    if mode == "camera":
        if not frozen:
            ret, frame = cap.read()
            if not ret or frame is None:
                time.sleep(0.05)
                continue
            # optional: resize for consistent UI
            display = cv2.resize(frame, (800, 600))
        else:
            # when frozen, show the frozen_frame (already resized)
            display = frozen_frame.copy()
    else:
        display = img.copy()

    # update the global view for mouse callback to use (and for saving)
    current_display = display.copy()

    if clicked:
        # determine shape from current_display (works for image, live, or frozen)
        h, w, _ = current_display.shape
        if 0 <= xpos < w and 0 <= ypos < h:
            b, g, r = current_display[ypos, xpos]
            b, g, r = int(b), int(g), int(r)

            cv2.rectangle(display, (20, 20), (750, 60), (b, g, r), -1)
            text = getColorName(r, g, b) + f"  R={r} G={g} B={b}"
            text_color = (0, 0, 0) if (r + g + b) >= 600 else (255, 255, 255)
            cv2.putText(display, text, (50, 50), 2, 0.8, text_color, 2, cv2.LINE_AA)

    cv2.imshow("Color Picker", display)
    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC to exit
        break

    # Toggle freeze/unfreeze with 'c' (lowercase)
    if key == ord('c'):
        if mode == "camera":
            if not frozen:
                # freeze: store the current displayed frame
                frozen_frame = current_display.copy()
                frozen = True
                print("⏸ Webcam frozen — pick color on the frozen frame (double-click). Press 'c' again to resume.")
            else:
                # unfreeze: resume live feed
                frozen = False
                frozen_frame = None
                print("▶ Webcam resumed.")
        else:
            print("❗ Not using webcam — open the script without --image to use freeze feature.")

    # Manual save of currently shown frame with 'C' (uppercase)
    if key == ord('C'):
        if current_display is not None:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"captures/captured_{ts}.jpg"
            cv2.imwrite(filename, current_display)
            print(f"📸 Saved: {filename}")

# Cleanup
if mode == "camera":
    cap.release()
cv2.destroyAllWindows()
