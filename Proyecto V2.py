import sqlite3
import tkinter as tk
from tkinter import messagebox


# CLASE PRINCIPALEISHON

class ProductosClientesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧩 Productos y Clientes")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # Conectar a la base de datos
        self.conn = sqlite3.connect("datos.db")
        self.crear_tablas()

        # Título
        tk.Label(root, text="💻 GESTIÓN BÁSICA", font=("Arial", 16, "bold")).pack(pady=20)

        # Botones principales
        tk.Button(root, text="➕ Agregar Producto", width=25, height=2,
                  bg="#1976D2", fg="white", font=("Arial", 10, "bold"),
                  command=self.agregar_producto).pack(pady=10)

        tk.Button(root, text="👤 Agregar Cliente", width=25, height=2,
                  bg="#388E3C", fg="white", font=("Arial", 10, "bold"),
                  command=self.agregar_cliente).pack(pady=10)

   
    # BASE DE DATEISHON
    
    def crear_tablas(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS productos (
                        codigo TEXT PRIMARY KEY,
                        nombre TEXT NOT NULL,
                        precio REAL NOT NULL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS clientes (
                        id_cliente TEXT PRIMARY KEY,
                        nombre TEXT NOT NULL,
                        email TEXT NOT NULL)''')
        self.conn.commit()

    
    # FUNCIONEISHON
    
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

    def agregar_cliente(self):
        win = tk.Toplevel(self.root)
        win.title("Agregar Cliente")
        win.geometry("300x220")

        tk.Label(win, text="ID Cliente:").pack()
        id_cliente = tk.Entry(win); id_cliente.pack()

        tk.Label(win, text="Nombre:").pack()
        nombre = tk.Entry(win); nombre.pack()

        tk.Label(win, text="Email:").pack()
        email = tk.Entry(win); email.pack()

        def guardar_cliente():
            try:
                c = self.conn.cursor()
                c.execute("INSERT INTO clientes VALUES (?, ?, ?)",
                          (id_cliente.get(), nombre.get(), email.get()))
                self.conn.commit()
                messagebox.showinfo("Éxito", "✅ Cliente agregado correctamente.")
                win.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "⚠️ Ya existe un cliente con ese ID.")

        tk.Button(win, text="Guardar", bg="#43A047", fg="white",
                  command=guardar_cliente).pack(pady=10)



# EJECUCIÓN DEL PROGRAMA

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductosClientesApp(root)
    root.mainloop()