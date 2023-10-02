import pyautogui
import webbrowser
import time
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Variable de control para detener el hilo
detener_envio = False

# Función para bloquear los controles
def bloquear_controles():
    entrada_numero.configure(state='disabled')
    entrada_mensaje.configure(state='disabled')
    entrada_repeticiones.configure(state='disabled')
    entrada_tiempo.configure(state='disabled')
    boton_enviar.configure(state='disabled')
    boton_detener.configure(state='active')
    boton_ayuda.configure(state='disabled')

# Función para desbloquear los controles
def desbloquear_controles():
    entrada_numero.configure(state='normal')
    entrada_mensaje.configure(state='normal')
    entrada_repeticiones.configure(state='normal')
    entrada_tiempo.configure(state='normal')
    boton_enviar.configure(state='normal')
    boton_detener.configure(state='disabled')
    boton_ayuda.configure(state='normal')

# Función para enviar mensajes
def enviar_mensajes():
    global detener_envio  # Accede a la variable global
    numero = entrada_numero.get()
    mensaje = entrada_mensaje.get()
    repeticiones = int(entrada_repeticiones.get())
    tiempo_inicio_sesion = int(entrada_tiempo.get())

    webbrowser.open(f'https://web.whatsapp.com/send?phone={numero}')
    time.sleep(tiempo_inicio_sesion)  # Espera el tiempo de inicio de sesión
    detener_envio = False
    bloquear_controles()  # Bloquea los controles durante el envío

    def hilo_enviar_mensaje():
        for _ in range(repeticiones):
            if detener_envio:
                print("Envío de mensajes detenido")
                desbloquear_controles()  # Desbloquea los controles al detener
                break  # Sale del bucle si detener_envio es True
            pyautogui.typewrite(mensaje)
            pyautogui.press('enter')
            time.sleep(1)  # Ajusta este tiempo para controlar la velocidad de envío
        desbloquear_controles()  # Desbloquea los controles al finalizar

    # Inicia el hilo para enviar mensajes
    hilo_envio = threading.Thread(target=hilo_enviar_mensaje)
    hilo_envio.start()

# Función para detener el envío de mensajes
def detener_envio_mensajes():
    global detener_envio  # Accede a la variable global
    detener_envio = True

# Función para mostrar la ventana de ayuda
def mostrar_ayuda():
    mensaje_ayuda = "Siga estos pasos para usar la aplicación:\n\n" \
                    "1. Asegúrese de iniciar sesión en WhatsApp Web en su navegador antes de continuar.\n" \
                    "2. Ingrese el número de teléfono en el campo 'Número de Teléfono'.\n" \
                    "3. Ingrese el mensaje que desea enviar en el campo 'Mensaje'.\n" \
                    "4. Ingrese la cantidad de repeticiones en el campo 'Cantidad de Repeticiones'.\n" \
                    "5. Ingrese el tiempo de espera de inicio de sesión en segundos en el campo 'Tiempo de Espera de Inicio de Sesión'.\n" \
                    "6. Haga clic en el botón 'Enviar Mensajes' para iniciar el envío de mensajes.\n" \
                    "7. Para detener el envío de mensajes en cualquier momento, haga clic en el botón 'Detener Envío'."
    
    messagebox.showinfo("Ayuda", mensaje_ayuda)

if __name__ == "__main__":
    app = tk.Tk()
    app.title("WhatsApp Sender")

    # Cambiar el color de fondo y el tamaño de fuente de toda la ventana
    app.configure(bg='#e4f0f6')

    # Estilo personalizado similar a WhatsApp
    estilo = ttk.Style()
    estilo.configure('My.TButton', foreground='white', background='#25d366', font=('Helvetica', 12))
    estilo.configure('My.TLabel', font=('Helvetica', 12), background='#e4f0f6')
    estilo.configure('My.TEntry', font=('Helvetica', 12))

    # Etiqueta y campo de entrada para el número de teléfono
    etiqueta_numero = ttk.Label(app, text="Número de Teléfono:")
    etiqueta_numero.grid(row=0, column=0)
    entrada_numero = ttk.Entry(app)
    entrada_numero.grid(row=0, column=1)

    # Etiqueta y campo de entrada para el mensaje
    etiqueta_mensaje = ttk.Label(app, text="Mensaje:")
    etiqueta_mensaje.grid(row=1, column=0)
    entrada_mensaje = ttk.Entry(app)
    entrada_mensaje.grid(row=1, column=1)

    # Etiqueta y campo de entrada para la cantidad de repeticiones
    etiqueta_repeticiones = ttk.Label(app, text="Cantidad de Repeticiones:")
    etiqueta_repeticiones.grid(row=2, column=0)
    entrada_repeticiones = ttk.Entry(app)
    entrada_repeticiones.grid(row=2, column=1)

    # Etiqueta y campo de entrada para el tiempo de espera de inicio de sesión
    etiqueta_tiempo = ttk.Label(app, text="Tiempo de Espera de Inicio de Sesión (segundos):")
    etiqueta_tiempo.grid(row=3, column=0)
    entrada_tiempo = ttk.Entry(app)
    entrada_tiempo.grid(row=3, column=1)

    # Botón para enviar mensajes
    boton_enviar = ttk.Button(app, text="Enviar Mensajes", command=enviar_mensajes, style='My.TButton')
    boton_enviar.grid(row=4, column=0, columnspan=2)

    # Botón para detener el envío de mensajes
    boton_detener = ttk.Button(app, text="Detener Envío", command=detener_envio_mensajes, state='disabled', style='My.TButton')
    boton_detener.grid(row=5, column=0, columnspan=2)

    # Botón de ayuda
    boton_ayuda = ttk.Button(app, text="(?)", command=mostrar_ayuda)
    boton_ayuda.grid(row=0, column=2, sticky="ne")  # Coloca el botón en la esquina superior derecha

    app.mainloop()