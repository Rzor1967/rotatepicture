import cv2
import numpy as np
from PIL import Image

# Lataa kuva harmaasävynä
img = cv2.imread("14.jpg", cv2.IMREAD_GRAYSCALE)

# Binarisoi (0=tausta, 255=suorakaide)
_, binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

# Etsi ääriviivat
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Oletetaan, että suurin ääriviiva on suorakaide
c = max(contours, key=cv2.contourArea)

# Löydä minimialueen suorakaide (voi olla vinossa)
rect = cv2.minAreaRect(c)   # (keskipiste, (leveys, korkeus), kulma)
angle = rect[2] # kulma
print(f"Detected angle: {angle} degrees")
if angle < -45:
    angle += 90


binary = binary.rotate(angle, expand=True)
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
c = max(contours, key=cv2.contourArea)
rect = cv2.minAreaRect(c)
box = cv2.boxPoints(rect)
box = np.intp(box)


img = Image.open("14.jpg")
rotated = img.rotate(angle, expand=True)
mask = np.zeros_like(rotated)
cv2.drawContours(mask, [box], 0, (255, 255, 255), -1)
out = cv2.bitwise_and(rotated, rotated, mask=mask)
x,y,w,h = cv2.boundingRect(box)
cropped = out[y:y+h, x:x+w]

cv2.imshow("Cropped", cropped)
cropped.save("cropped_image.jpg", "JPEG")
# rotated.show()