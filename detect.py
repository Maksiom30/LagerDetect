import cv2
import numpy as np

def detect_bottles(image):
    # Bild einlesen
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Bildvorverarbeitung
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # Konturen finden
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Flaschen erkennen und markieren
    count = 0
    for contour in contours:
        # Eine einfache Annahme: Flaschen sind kreisförmig
        if len(contour) >= 5 and len(contour) <= 20:
            ellipse = cv2.fitEllipse(contour)
            cv2.ellipse(image, ellipse, (0, 255, 0), 2)
            count += 1

    # Ergebnis anzeigen
    return image, count

# Beispielaufruf der Funktion
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        img = detect_bottles(frame)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()