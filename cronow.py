import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import time
from openpyxl import Workbook
import threading

# Variables globales
puerto_serial = None
cronometro_corriendo = False
start_time = None
time_cap = 0


# Función para simular la conexión (puedes adaptar esto según la lógica de conexión)
def listar_puertos():
    ports = serial.tools.list_ports.comports()
    puerto_menu['menu'].delete(0, 'end')  # Limpiar el menú
    
    # Si no hay puertos disponibles
    if not ports:
        puerto_menu['menu'].add_command(label="No hay puertos disponibles", command=tk._setit(puerto_var, ""))
        puerto_var.set("No hay puertos disponibles")
        return
    
    # Añadir los puertos disponibles al menú
    for port in ports:
        puerto_menu['menu'].add_command(label=port.device, command=tk._setit(puerto_var, port.device))
    
    # Seleccionar el primer puerto como predeterminado
    if ports:
        puerto_var.set(ports[0].device)

# Función para conectar al puerto seleccionado
def conectar_puerto():
    global puerto_serial
    selected_port = puerto_var.get()
    
    if not selected_port or selected_port == "No hay puertos disponibles":
        messagebox.showwarning("Advertencia", "Selecciona un puerto primero")
        return

    try:
        puerto_serial = serial.Serial(selected_port, baudrate=115200, timeout=1)
        estado_boton.config(bg="green", text="Conectado")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar al puerto: {e}")

def desconectar_puerto():
    global puerto_serial
    if puerto_serial:
        puerto_serial.close()
        puerto_serial = None
        estado_boton.config(bg="red", text="Desconectado")

# Interfaz Tkinter
root = tk.Tk()
root.title("Cronow created by SMARTLUM")
root.state("zoomed")

# Configuración de estilos
style = ttk.Style()
style.configure("big.TButton", font=("Helvetica", 18))
style.configure("crono.TLabel",foreground="red", font=("Helvetica", 52))

# Función para iniciar el cronómetro general

def iniciar_cronometro_general():
    global start_time, cronometro_corriendo, time_cap

    for i in range(10, 0, -1):
        cronometro_general_label.config(text=f"{i}", font=("Helvetica", 52))
        root.update()  
        time.sleep(1)  
    start_time = time.time()
    cronometro_corriendo = True
    try:
        time_cap = int(entry_time_cap.get())
    except ValueError:
        time_cap = 0
    actualizar_cronometro()

# Función para parar el cronómetro general
def parar_cronometro():
    global cronometro_corriendo
    cronometro_corriendo = False
#funcion de iniciar el cronometro con cuenta regresiva de 10 seg
def reset_cronometro():
    global cronometro_corriendo, tiempos

    cronometro_corriendo = False
    minutos = int(00)
    segundos = int(00)
    decimas = int(00)
    cronometro_general_label.config(text=f"{minutos:02d}:{segundos:02d}.{decimas}")
    tiempos=["00:00.0","00:00.0","00:00.0","00:00.0","00:00.0","00:00.0","00:00.0","00:00.0"]
    for i in range(8):
        label_time = tk.Label(frame_lane,bg="lightblue", text=str(tiempos[i]),font=("Helvetica", 30))
        label_time.grid(row=i, column=2)

    
# Función para actualizar el cronómetro general en la interfaz
def actualizar_cronometro():

    if cronometro_corriendo and start_time:
        elapsed_time = time.time() - start_time
        minutos = int(elapsed_time // 60)
        segundos = int(elapsed_time % 60)
        decimas = int((elapsed_time % 1)*10)
        cronometro_general_label.config(text=f"{minutos:02d}:{segundos:02d}.{decimas}" , style="crono.TLabel")
        
        # Parar el cronómetro si llega al time cap
        if time_cap > 0 and elapsed_time >= time_cap * 60:
            parar_cronometro()
            messagebox.showinfo("Time Cap Alcanzado", "El cronómetro ha llegado al tiempo máximo.")
            return
        
        root.after(100, actualizar_cronometro)

# Frame para el cronómetro general
frame_cronometro = tk.LabelFrame(root, text="Cronómetro General")
frame_cronometro.pack(padx=10, pady=5, fill="x")

cronometro_general_label = ttk.Label(frame_cronometro, text="00:00.0", style="crono.TLabel")  
cronometro_general_label.pack(pady=10)

# Casilla para el time cap
label_time_cap = ttk.Label(frame_cronometro, text="Time Cap (min):", font=("Helvetica", 18))
label_time_cap.pack(pady=5)
entry_time_cap = ttk.Entry(frame_cronometro, font=("Helvetica", 18))
entry_time_cap.pack(pady=5)

# Botones para iniciar y parar el cronómetro
boton_inicio = ttk.Button(frame_cronometro, text="Iniciar Cronómetro", command=iniciar_cronometro_general, style="big.TButton")
boton_inicio.pack(side=tk.LEFT, padx=20, pady=5)

# Botones para iniciar y parar el cronómetro
boton_reinicio = ttk.Button(frame_cronometro, text="Reset", command=reset_cronometro, style="big.TButton")
boton_reinicio.pack(side=tk.LEFT, padx=345, pady=5)

boton_parar = ttk.Button(frame_cronometro, text="Parar Cronómetro", command=parar_cronometro, style="big.TButton")
boton_parar.pack(side=tk.RIGHT, padx=20, pady=5)


# Frame para la conexión serial
frame_conexion = tk.LabelFrame(root,bg="lightblue", text="Conexión Serial")
frame_conexion.pack(side=tk.LEFT,padx=10, pady=10, fill="y")

# Variable para el menú desplegable de puertos
puerto_var = tk.StringVar()
puerto_menu = tk.OptionMenu(frame_conexion, puerto_var, "")
puerto_menu.config(width=30)
puerto_menu.pack(pady=10)

# Botón para listar los puertos
listar_puertos_btn = tk.Button(frame_conexion, text="Listar Puertos", command=listar_puertos)
listar_puertos_btn.pack(pady=5)

# Botón para conectar
conectar_btn = tk.Button(frame_conexion, text="Conectar", command=conectar_puerto)
conectar_btn.pack(pady=5)

# Botón para desconectar
desconectar_btn = tk.Button(frame_conexion, text="Desconectar", command=desconectar_puerto)
desconectar_btn.pack(pady=5)

# Botón de estado
estado_boton = tk.Label(frame_conexion, text="Desconectado", bg="red", width=15)
estado_boton.pack(pady=10)

wod_var = tk.StringVar(value="WOD 1")
categoria_var = tk.StringVar(value="Intermedio")
heat_var = tk.StringVar(value="Heat 1")
# Frame para la información del evento
frame_info = tk.LabelFrame(root,bg="lightblue", text="Información del Evento")
frame_info.pack(side=tk.LEFT,padx=10, pady=5, fill="y")

ttk.Label(frame_info, text="WOD:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
tk.Entry(frame_info,textvariable=wod_var, font=("Helvetica", 20), width=20).grid(row=0, column=1, padx=10, pady=5)


ttk.Label(frame_info, text="CATEGORÍA:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
tk.Entry(frame_info,textvariable=categoria_var, font=("Helvetica", 20), width=20).grid(row=1, column=1, padx=10, pady=5)

ttk.Label(frame_info, text="HEAT:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
tk.Entry(frame_info,textvariable=heat_var, font=("Helvetica", 20), width=20).grid(row=2, column=1, padx=10, pady=5)


# Frame para los carriles
frame_carriles = tk.LabelFrame(root,bg="lightblue", text="Carriles")
frame_carriles.pack(side=tk.RIGHT,padx=20, pady=5, fill="y", expand=True)



competidores = [] 
tiempos=["00:00.0","00:00.0","00:00.0","00:00.0","00:00.0","00:00.0","00:00.0","00:00.0"]

var_t_c1 = tk.StringVar(value="00:00.0")
var_t_c2 = tk.StringVar(value="00:00.0")
var_t_c3 = tk.StringVar(value="00:00.0")
var_t_c4 = tk.StringVar(value="00:00.0")
var_t_c5 = tk.StringVar(value="00:00.0")
var_t_c6 = tk.StringVar(value="00:00.0")
var_t_c7 = tk.StringVar(value="00:00.0")
var_t_c8 = tk.StringVar(value="00:00.0")

frame_lane = tk.Frame(frame_carriles,bg="lightblue")
frame_lane.pack(fill="x", padx=10, pady=5)
for i in range(8):

    label_lane = tk.Label(frame_lane,bg="lightblue", text=f"CARRIL {i+1}:",font=("Helvetica", 20), width=10)
    label_lane.grid(row=i, column=0)
        # Campo para el nombre del competidor
    nombre_competidor = tk.Entry(frame_lane, font=("Helvetica", 25), width=15)
    nombre_competidor.grid(row=i, column=1)
    competidores.append(nombre_competidor)

    label_time = tk.Label(frame_lane,bg="lightblue", text=str(tiempos[i]),font=("Helvetica", 30))
    label_time.grid(row=i, column=2)
    





workbook = Workbook()
sheet = workbook.active
sheet.title = "Resultados"
# Agregar encabezados a la hoja de Excel
sheet.append(["WOD", "Categoría", "Heat", "Carril", "Nombre", "Tiempo"])
# Función para guardar los resultados en el archivo Excel
def guardar_datos():
    # Accede a los valores de las variables
    wod = wod_var.get()
    categoria = categoria_var.get()
    heat = heat_var.get()

    # Asegúrate de que las variables tengan valor
    if not wod or not categoria or not heat:
        messagebox.showerror("Error", "Faltan datos del WOD, Categoría o Heat")
        return

    # Crear un nuevo archivo Excel
    try:
        # Añade los datos de los competidores y sus tiempos
        for i in range(8):
            name = competidores[i].get()
            time = tiempos[i]
            sheet.append([wod, categoria, heat, f"Carril {i+1}", name, time])
        
        # Guardar el archivo Excel con los valores de las variables
        filename = f"{wod}_{categoria}_{heat}.xlsx"
        workbook.save(filename)
        
        # Muestra un mensaje de éxito
        messagebox.showinfo("Éxito", f"Resultados guardados en {filename}")
    except Exception as e:
        # Muestra un mensaje de error si algo falla
        messagebox.showerror("Error", f"No se pudieron guardar los datos: {e}")

boton_guardar = ttk.Button(frame_info, text="Guardar en Excel", command=guardar_datos)
boton_guardar.grid(row=3,column=1,padx=10,pady=5)

def recibir_datos_serial():
    global tiempos
    while True:
        if puerto_serial and puerto_serial.is_open:
            try:
                data = puerto_serial.readline().decode().strip()  # Leer datos del puerto serial
                if data:
                    print(f"Datos recibidos: {data}")  # Depuración

                    # Asegurarse de que el formato es correcto "id,accion"
                    if "," in data:
                        id_carril, accion = data.split(",")
                        id_carril = int(id_carril)
                        

                        # Verificar si la acción es 'p' (parar)
                        if accion == 'p':
                            # Calcular el tiempo transcurrido para ese carril
                            tiempo_carril = time.time() - start_time
                            minutos = int(tiempo_carril // 60)
                            segundos = int(tiempo_carril % 60)
                            decimas = int((tiempo_carril % 1) * 10)

                            # Actualizar el tiempo en la interfaz de Tkinter
                            tiempos[id_carril - 1]= f"{minutos:02d}:{segundos:02d}.{decimas}"
                            
                            label_time = tk.Label(frame_lane,bg="green" ,text=str(tiempos[id_carril - 1]),font=("Helvetica", 30))
                            label_time.grid(row=id_carril - 1, column=2)
                    
                            #print(tiempos)

                            # Mostrar mensaje en la consola para depurar
                            print(f"Carril {id_carril} terminó con tiempo: {minutos:02d}:{segundos:02d}.{decimas}")
            except Exception as e:
                print(f"Error al leer datos: {e}")


# Hilo para recibir datos del ESP32
thread = threading.Thread(target=recibir_datos_serial, daemon=True)
thread.start()



# Ejecutar la interfaz
root.mainloop()
