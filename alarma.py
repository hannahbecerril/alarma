import threading
import winsound
import cv2
import imutils

umbral = int(input("Escriba en decimal que tanto umbral quiere tener"))

# Función para la alarma de sonido
def beep_alarm():
    global alarm
    for _ in range(5):
        if not alarm_mode:
            break
        print("ALARMA")
        winsound.Beep(2500, 1000)
    alarm = False

# Función para detectar movimiento
def detect_motion(frame):
    frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_bw = cv2.GaussianBlur(frame_bw, (21, 21), 0)
    difference = cv2.absdiff(frame_bw, start_frame)
    threshold = cv2.threshold(difference, 50, 255, cv2.THRESH_BINARY)[1]  # Aumenta el umbral de movimiento
    # Mostrar el umbral de movimiento
    cv2.imshow("Motion Detection", threshold)
    # Verificar si hay movimiento presente
    if threshold.sum() > umbral:  # Ajusta este valor según sea necesario
        return True
    else:
        return False

# Inicialización de la cámara
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Captura y procesamiento del primer fotograma
_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

# Variables para la detección de movimiento y alarma
alarm = False
alarm_mode = False
alarm_counter = 0

# Bucle principal
while True:
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    # Modo de alarma activo: detección de movimiento
    if alarm_mode:
        if detect_motion(frame):
            alarm_counter += 1
        else:
            alarm_counter = 0
    # Modo de alarma inactivo: mostrar el fotograma de la cámara
    else:
        cv2.imshow("Camera", frame)

    # Activar la alarma si hay movimiento y se supera el umbral de tiempo
    if alarm_counter > 60:  # Aumenta este valor para requerir más fotogramas consecutivos con movimiento
        if not alarm:
            alarm = True
            threading.Thread(target=beep_alarm).start()

    # Capturar eventos de teclado
    key = cv2.waitKey(30)
    if key == ord("t"):  # Cambiar el modo de alarma
        alarm_mode = not alarm_mode
        alarm_counter = 0
    elif key == ord("q"):  # Salir del programa
        alarm_mode = False
        break

# Liberar la cámara y cerrar ventanas
cap.release()
cv2.destroyAllWindows()
