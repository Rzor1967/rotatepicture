import cv2
import numpy as np
import os
import time

counter = 0

def straighten_and_crop(img):
    # Muutetaan binaarikuvaksi
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (31, 31), 0)
    _, binary = cv2.threshold(gray, 32, 255, cv2.THRESH_BINARY)
    
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

    # Päivitä ääriviiva uudesta kuvasta
    gray_rot = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (31, 31), 0)
    _, thresh_rot = cv2.threshold(gray_rot, 32, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh_rot, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)

    # Rajaa lopputulos ja lisää reunus
    cropped = rotated[y:y+h, x:x+w]
    img_with_border = cv2.copyMakeBorder(cropped, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=[0,0,0])
    
    return img_with_border

def erota_alueet(kuva_polku, tulos_kansio="alueet"):
    # 1. Lataa alkuperäinen värikuva
    img = cv2.imread(kuva_polku)
    if img is None:
        print("Virhe: kuvaa ei voitu ladata.")
        return

    # 2. Harmaasävyksi
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. Gaussian blur
    blur = cv2.GaussianBlur(gray, (31, 31), 0)

    # 4. Binaarisointi (Otsu)
    _, thresh = cv2.threshold(blur, 32, 255, cv2.THRESH_BINARY)

    # 5. Etsi ääriviivat
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 6. Luo kansio tuloksille
    os.makedirs(tulos_kansio, exist_ok=True)

    # 7. Käy läpi kaikki löydetyt alueet
    for i, cnt in enumerate(contours):
        # Jätä pois liian pienet kohdat
        if cv2.contourArea(cnt) < 40000: # 200 x 200 px
            continue

        # Luo maski
        mask = np.zeros(gray.shape, dtype=np.uint8)
        cv2.drawContours(mask, [cnt], -1, 255, thickness=cv2.FILLED)

        # Käytä maskia alkuperäiseen
        erottu = cv2.bitwise_and(img, img, mask=mask)

        # Rajaa bounding boxin avulla
        x, y, w, h = cv2.boundingRect(cnt)
        roi = erottu[y:y+h, x:x+w]
        img_with_border = cv2.copyMakeBorder(roi, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=[0,0,0])
        
        # Suorista ja rajaa alue
        final_pic = straighten_and_crop(img_with_border)
        
        # Tallenna oma tiedosto
        global counter
        counter += 1
        cv2.imwrite(f"{tulos_kansio}/alue_{counter}.jpg", final_pic)

def main(source_path, dest_path):
    while True:
        image_files = [f for f in os.listdir(source_path) if f.lower().endswith(('.jpg'))]
        for f in image_files:
            full_path = os.path.join(source_path, f)
            erota_alueet(full_path, dest_path)
            millisekunnit = int(time.time() * 1000)
            os.rename(full_path, os.path.join(source_path+"/done", str(millisekunnit) + "_" + f))
        print("Odota uusia kuvia...")
        time.sleep(5)  # Odota 5 sekuntia ennen seuraavaa tarkistusta

if __name__ == "__main__":
    source_path = "C:/Users/OMISTAJA/Pictures/Crop"
    dest_path = "C:/Users/OMISTAJA/Pictures/Scan/1"
    main(source_path, dest_path)
    




















































