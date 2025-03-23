import cv2 
import mysql.connector
import datetime
import tkinter as tk
from tkinter import messagebox

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="registro"
    )

def registrar_entrada_salida(empleado_id, tipo):
    conn = connect_db()
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO registros (empleado_id, timestamp, tipo) VALUES (%s, %s, %s)", (empleado_id, timestamp, tipo))
    conn.commit()
    conn.close()
    messagebox.showinfo("Registro Exitoso", f"{tipo} registrada para el empleado {empleado_id} a las {timestamp}")

def escanear_qr_camara():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        
        data, bbox, _ = detector.detectAndDecode(frame)
        if data:
            cap.release()
            cv2.destroyAllWindows()
            tipo = "Entrada" if not verificar_ultimo_registro(data) else "Salida"
            registrar_entrada_salida(data, tipo)
            return
        
        cv2.imshow("Escanear QR", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def verificar_ultimo_registro(empleado_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT tipo FROM registros WHERE empleado_id = %s ORDER BY timestamp DESC LIMIT 1", (empleado_id,))
    ultimo = cursor.fetchone()
    conn.close()
    return ultimo and ultimo[0] == "Entrada"

def iniciar_interfaz():
    root = tk.Tk()
    root.title("Registro de Empleados HNSC")
    root.geometry("400x300")
    
    
    label = tk.Label(root, text="Escanea tu QR", font=("Arial", 14))
    label.pack(pady=20)
    
    
    btn_escanear_camara = tk.Button(root, text="Escanear QR ", command=escanear_qr_camara, height=2, width=25)
    btn_escanear_camara.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()
