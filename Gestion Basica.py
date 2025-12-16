import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog   


# CLASE PRINCIPALEISHON

class ProductosClientesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧩 Productos y Clientes")
        self.root.geometry("400x400")
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

        # 🔍 Ver registros
        tk.Button(root, text="📋 Ver Registros", width=25, height=2,
                  bg="#F57C00", fg="white", font=("Arial", 10, "bold"),
                  command=self.ver_registros).pack(pady=10)

        # 💾 Guardar registros
        tk.Button(root, text="💾 Guardar Registros", width=25, height=2,
                  bg="#5E35B1", fg="white", font=("Arial", 10, "bold"),
                  command=self.guardar_registros).pack(pady=10)

        # ❌ Salir
        tk.Button(root, text="❌ Salir del Programa", width=25, height=2,
                  bg="#D32F2F", fg="white", font=("Arial", 10, "bold"),
                  command=self.cerrar_programa).pack(pady=10)

   
    # BASE DE DATEISHON
    
    def crear_tablas(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS productos (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    precio REAL NOT NULL)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
                c.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)",
                          (nombre.get(), float(precio.get())))
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
                c.execute("INSERT INTO clientes (nombre, email) VALUES (?, ?)",
                         (nombre.get(), email.get()))
                self.conn.commit()
                messagebox.showinfo("Éxito", "✅ Cliente agregado correctamente.")
                win.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "⚠️ Ya existe un cliente con ese ID.")

        tk.Button(win, text="Guardar", bg="#43A047", fg="white",
                  command=guardar_cliente).pack(pady=10)

    #  Ver registros
    def ver_registros(self):
        win = tk.Toplevel(self.root)
        win.title("📋 Registros")
        win.geometry("500x400")

        c = self.conn.cursor()

        # Productos
        tk.Label(win, text="🛒 PRODUCTOS", font=("Arial", 12, "bold")).pack(pady=5)
        productos_box = tk.Text(win, width=60, height=10)
        productos_box.pack()
        productos_box.insert(tk.END, "ID\tNombre\tPrecio\n")
        productos_box.insert(tk.END, "-"*50 + "\n")
        for p in c.execute("SELECT * FROM productos"):
            productos_box.insert(tk.END, f"{p[0]}\t{p[1]}\t${p[2]:.2f}\n")

        # Clientes
        tk.Label(win, text="👥 CLIENTES", font=("Arial", 12, "bold")).pack(pady=5)
        clientes_box = tk.Text(win, width=60, height=10)
        clientes_box.pack()
        clientes_box.insert(tk.END, "ID\tNombre\tEmail\n")
        clientes_box.insert(tk.END, "-"*50 + "\n")
        for cte in c.execute("SELECT * FROM clientes"):
            clientes_box.insert(tk.END, f"{cte[0]}\t{cte[1]}\t{cte[2]}\n")

        productos_box.config(state="disabled")
        clientes_box.config(state="disabled")

    # 💾 Guardar registros (con explorador)
    def guardar_registros(self):
        try:
            ruta = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Archivo de texto", "*.txt")],
                title="Guardar registros"
            )

            if not ruta:
                return

            c = self.conn.cursor()
            with open(ruta, "w", encoding="utf-8") as f:
                f.write("🛒 PRODUCTOS\n")
                f.write("Código\tNombre\tPrecio\n")
                f.write("-" * 40 + "\n")
                for p in c.execute("SELECT * FROM productos"):
                    f.write(f"{p[0]}\t{p[1]}\t${p[2]:.2f}\n")

                f.write("\n👥 CLIENTES\n")
                f.write("ID\tNombre\tEmail\n")
                f.write("-" * 40 + "\n")
                for cte in c.execute("SELECT * FROM clientes"):
                    f.write(f"{cte[0]}\t{cte[1]}\t{cte[2]}\n")

            messagebox.showinfo("Éxito", "✅ Archivo guardado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"⚠️ No se pudo guardar\n{e}")

    # Nueva funcion cerrar programa
    def cerrar_programa(self):
        if messagebox.askyesno("Salir", "¿Deseas cerrar el programa?"):
            self.root.destroy()



# EJECUCIÓN DEL PROGRAMA

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductosClientesApp(root)
    root.mainloop()