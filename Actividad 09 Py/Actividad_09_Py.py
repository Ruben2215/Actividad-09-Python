import tkinter as tk
from tkinter import messagebox
import serial
import time
import threading

arduino_port = "COM6"
arduino_baud = 9600
arduino = None

def Conectar():
    global arduino
    try:
        arduino = serial.Serial(arduino_port, arduino_baud, timeout=1)
        time.sleep(2)
        lbConection.config(text="Conectado", fg="green")
        messagebox.showinfo("Conexion", "Conexion establecida")
        start_reading()
    except serial.SerialException:
        messagebox.showerror("Error", "No se pudo conectar al Arduino\nPor favor, verificar la conexion")

def desconectar():
    global arduino
    if arduino and arduino.is_open:
        arduino.close()
        lbConection.config(text="Estado: Desconectado", fg="red")
        messagebox.showinfo("Conexion", "Conexion terminada")
    else:
        messagebox.showwarning("Advertencia", "No hay conexion activa")

# Funcion para enviar el limite de temperatura al Arduino
def enviar_limite():
    global arduino
    if arduino and arduino.is_open:
        try:
            limite = tbLimitTemp.get()
            if limite.isdigit(): 
                arduino.write(f"{limite}\n".encode())  
                messagebox.showinfo("Enviado", f"Limite de temperatura ({limite} C) enviado.")
            else:
                messagebox.showerror("Error", "Ingrese un valor numerico para el limite.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el limite: {e}")
    else:
        messagebox.showwarning("Advertencia", "Conectese al Arduino antes de enviar el limite.")

# Funcion para leer datos desde el Arduino
def read_from_arduino():
    global arduino
    while arduino and arduino.is_open:
        try:
            data = arduino.readline().decode().strip()  # Lee los datos de temperatura
            if data:  
                
                try:
                   
                    temp_value = float(data)
                    lbTemp.config(text=f"{temp_value} C")
                except ValueError:
                    print("Dato recibido no es un numero de temperatura")
            time.sleep(1)
        except Exception as e:
            print(f"Error leyendo datos: {e}")
            break

def start_reading():
    thread = threading.Thread(target=read_from_arduino)
    thread.daemon = True
    thread.start()

root = tk.Tk()
root.title("Interfaz de Monitoreo de Temperatura")
root.geometry("300x350")

lbTitleTemp = tk.Label(root, text="Temperatura Actual", font=("Arial", 12))
lbTitleTemp.pack(pady=10)

lbTemp = tk.Label(root, text="-- C", font=("Arial", 24))
lbTemp.pack(pady=10)

lbConection = tk.Label(root, text="Estado: Desconectado", fg="red", font=("Arial", 10))
lbConection.pack(pady=5)

lbLimitTemp = tk.Label(root, text="Limite de Temperatura:")
lbLimitTemp.pack(pady=5)
tbLimitTemp = tk.Entry(root, width=10)
tbLimitTemp.pack(pady=5)

btnEnviar = tk.Button(root, text="Enviar Limite", command=enviar_limite, font=("Arial", 10))
btnEnviar.pack(pady=5)

btnConectar = tk.Button(root, text="Conectar", command=Conectar, font=("Arial", 10))
btnConectar.pack(pady=5)

btnDesconectar = tk.Button(root, text="Desconectar", command=desconectar, font=("Arial", 10))
btnDesconectar.pack(pady=5)

root.mainloop()
