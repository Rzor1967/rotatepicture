import cv2
import numpy as np
import os

def straighten_and_crop(image_path, save_path="output.png"):
    # Lataa kuva
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (31, 31), 0)

    # cv2.imshow("gray", gray)
    # cv2.waitKey(0)
    # Kynnysarvo mustaa taustaa vastaan
    _, binary = cv2.threshold(gray, 32, 255, cv2.THRESH_BINARY)
    # cv2.imshow("Binaari", binary)
    # cv2.waitKey(0)
    
    # Etsi ääriviivat
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Valitse suurin ääriviiva (oletetaan että se on suorakaide)
    c = max(contours, key=cv2.contourArea)

    # Löydä minimi-kiertävä suorakulmio
    rect = cv2.minAreaRect(c)

    box = cv2.boxPoints(rect)
    box = np.intp(box)

    # Suorakulmion kulma
    angle = rect[2]
    print(f"Detected angle: {angle} degrees")
    if angle < -45:
        angle = 90 + angle
    if angle > 45:
        angle = angle - 90
    print(f"Corrected angle for rotation: {angle} degrees")
    # Luo kiertomatriisi ja käännä
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # cv2.imshow("Rotated", rotated)
    # cv2.waitKey(0)

    # Päivitä ääriviiva uudesta kuvasta
    gray_rot = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (31, 31), 0)
    _, thresh_rot = cv2.threshold(gray_rot, 32, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh_rot, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)

    # Rajaa lopputulos
    cropped = rotated[y:y+h, x:x+w]

    img_with_border = cv2.copyMakeBorder(cropped, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=[0,0,0])
    # Tallenna
    cv2.imwrite(save_path, img_with_border)
    print(f"Tallennettu: {save_path}")

# Käyttö
folder_path = "C:/Users/OMISTAJA/Pictures/Scan/1"
image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg'))]
for f in image_files:
    _, num = f.split('_')
    straighten_and_crop(os.path.join(folder_path, f), os.path.join(folder_path, f"pic_{num}"))

# straighten_and_crop(pic_file, "rajattu1.png")