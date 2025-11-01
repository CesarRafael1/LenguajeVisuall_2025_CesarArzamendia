import sqlite3
import tkinter as tk
from tkinter import messagebox

# CLASE PRINCIPAL

class ProductosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧩 Gestión de Productos")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # Conectar a la base de datos
        self.conn = sqlite3.connect("datos.db")
        self.crear_tabla_productos()

        # Título
        tk.Label(root, text="💻 GESTIÓN BASICA", font=("Arial", 16, "bold")).pack(pady=20)

        # Botones principales
        tk.Button(root, text="➕ Agregar Producto", width=25, height=2,
                  bg="#1976D2", fg="white", font=("Arial", 10, "bold"),
                  command=self.agregar_producto).pack(pady=10)

   
    # BASE DE DATOS
    
    def crear_tabla_productos(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS productos (
                        codigo TEXT PRIMARY KEY,
                        nombre TEXT NOT NULL,
                        precio REAL NOT NULL)''')
        self.conn.commit()

    
    # FUNCIONES
    
    def agregar_producto(self):
        win = tk.Toplevel(self.root)
        win.title("Agregar Producto")
        win.geometry("300x220")

        tk.Label(win, text="Código:").pack()
        codigo = tk.Entry(win); codigo.pack()

        tk.Label(win, text="Nombre:").pack()
        nombre = tk.Entry(win); nombre.pack()

        tk.Label(win, text="Precio:").pack()
        precio = tk.Entry(win); precio.pack()

        def guardar_producto():
            try:
                c = self.conn.cursor()
                c.execute("INSERT INTO productos VALUES (?, ?, ?)",
                          (codigo.get(), nombre.get(), float(precio.get())))
                self.conn.commit()
                messagebox.showinfo("Éxito", "✅ Producto agregado correctamente.")
                win.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "⚠️ Ya existe un producto con ese código.")
            except ValueError:
                messagebox.showerror("Error", "⚠️ Precio inválido.")

        tk.Button(win, text="Guardar", bg="#43A047", fg="white",
                  command=guardar_producto).pack(pady=10)


# EJECUCIÓN DEL PROGRAMA

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductosApp(root)
    root.mainloop()
