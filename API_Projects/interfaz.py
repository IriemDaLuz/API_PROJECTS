import tkinter as tk
from tkinter import messagebox as alert, ttk

import requests
from PIL import ImageTk
from PIL import Image
from weasyprint import HTML
import io


class ProductoApp:
    def __init__(self, listaDeProductos):
        self.productos = listaDeProductos.products
        self.index = 0

        self.root = tk.Tk()
        self.root.title("Product List")
        self.root.configure(bg="#f0f0f0")

        # Frame principal
        self.frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20, width=650, height=900)
        self.frame.pack()

        # Entrada de búsqueda
        self.productoBuscado = tk.Entry(self.frame, font=("Arial", 14), width=30)
        self.productoBuscado.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.botonBusqueda = tk.Button(self.frame, text="Buscar", font=("Arial", 10), command=self.buscar_producto)
        self.botonBusqueda.grid(row=0, column=2, padx=10, pady=10)

        # Título del producto
        self.tituloProducto = tk.Label(self.frame, font=("Arial", 20, "bold"), bg="#f0f0f0")
        self.tituloProducto.grid(row=1, column=0, columnspan=2, sticky="w")

        # Placeholder para imagen
        self.img_label = ttk.Label(self.frame, background="#f0f0f0")
        self.img_label.grid(row=2, column=0, columnspan=2)

        # Información del producto
        self.categoriaProducto = tk.Label(self.frame, font=("Arial", 10), fg="orange", bg="#f0f0f0")
        self.categoriaProducto.grid(row=2, column=2, sticky="w")

        self.descripcionProducto = tk.Label(self.frame, font=("Arial", 10), wraplength=400, justify="left",
                                            bg="#f0f0f0")
        self.descripcionProducto.grid(row=3, column=2, sticky="w")

        self.stockProducto = tk.Label(self.frame, font=("Arial", 10), bg="#f0f0f0")
        self.stockProducto.grid(row=4, column=2, sticky="w")

        self.ratingProducto = tk.Label(self.frame, font=("Arial", 10), bg="#f0f0f0")
        self.ratingProducto.grid(row=5, column=2, sticky="w")

        self.precioProducto = tk.Label(self.frame, font=("Arial", 18, "bold"), fg="red", bg="#f0f0f0")
        self.precioProducto.grid(row=6, column=2, sticky="w")

        self.reviewProducto = tk.Label(self.frame, font=("Arial", 10), bg="#f0f0f0")
        self.reviewProducto.grid(row=7, column=2, sticky="w")

        # Botones de navegación
        self.btnAnterior = tk.Button(self.frame, text="Anterior", font=("Arial", 10), bg="#f0f0f0",
                                     command=self.anterior_producto)
        self.btnAnterior.grid(row=8, column=0, sticky="n")

        self.indiceActual = tk.Label(self.frame, font=("Arial", 10), bg="#f0f0f0")
        self.indiceActual.grid(row=8, column=1, sticky="n")

        self.btnSiguiente = tk.Button(self.frame, text="Siguiente", font=("Arial", 10), bg="#f0f0f0",
                                      command=self.siguiente_producto)
        self.btnSiguiente.grid(row=8, column=2, sticky="n")

        self.mostrar_producto()

    def mostrar_producto(self, img_tk=None):
        product = self.productos[self.index]
        self.tituloProducto.config(text=product.title)
        self.categoriaProducto.config(text=f"Categoría: {product.category}")
        self.descripcionProducto.config(text=product.description)
        self.stockProducto.config(text=f"Stock: {product.stock}")
        self.precioProducto.config(text=f"${product.price}")
        self.indiceActual.config(text=f"{self.index + 1}/{len(self.productos)}")
        self.ratingProducto.config(text=f"Calificación: {product.rating}")

        r = requests.get(product.thumbnail, stream=True)
        img_data = r.content
        img = Image.open(io.BytesIO(img_data))
        img.thumbnail((150, 150))

        img_tk = ImageTk.PhotoImage(img)
        self.img_label.config(image=img_tk)
        self.img_label.image = img_tk

    def siguiente_producto(self):
        if self.index < len(self.productos) - 1:
            self.index += 1
            self.mostrar_producto()

    def anterior_producto(self):
        if self.index > 0:
            self.index -= 1
            self.mostrar_producto()

    def buscar_producto(self):
        busqueda = self.productoBuscado.get().lower()
        resultados = [producto for producto in self.productos if
                      busqueda in producto.title.lower() or
                      busqueda in producto.description.lower() or
                      busqueda in producto.category.lower()]

        if resultados:
            self.mostrar_busqueda(resultados)
        else:
            alert.showerror(title="Error en la búsqueda",
                            message="No se ha encontrado ningún producto que coincida con la búsqueda. Por favor, intenta con otro término.")

    def mostrar_busqueda(self, productos_encontrados):
        ventana_busqueda = tk.Toplevel(self.root)
        ventana_busqueda.title("Resultados de Búsqueda")
        ventana_busqueda.configure(bg="#f0f0f0")

        frame_busqueda = tk.Frame(ventana_busqueda, bg="#f0f0f0", padx=20, pady=20)
        frame_busqueda.pack()

        for idx, producto in enumerate(productos_encontrados):
            ttk.Separator(
                frame_busqueda, orient=tk.HORIZONTAL
            ).grid(row=idx, column=0, columnspan=3, sticky="EW")

            tk.Label(frame_busqueda, text=producto.title, font=("Arial", 12), bg="#f0f0f0").grid(row=idx, column=0,
                                                                                                 sticky="w")
            tk.Label(frame_busqueda, text=f"Categoría: {producto.category}", font=("Arial", 10), fg="orange",
                     bg="#f0f0f0").grid(row=idx, column=2, sticky="w")
            tk.Label(frame_busqueda, text=f"${producto.price}", font=("Arial", 10, "bold"), fg="red",
                     bg="#f0f0f0").grid(row=idx, column=3, sticky="w")

        boton_pdf = tk.Button(ventana_busqueda, text="Generar PDF",
                              command=lambda: self.generar_pdf(productos_encontrados))
        boton_pdf.pack(pady=10)

    def generar_pdf(self, productos_encontrados):
        html_content = """
        <html>
        <head>
            <meta charset='UTF-8'>
            <title>Lista de Productos</title>
            <style>
                body { font-family: Arial, sans-serif; color: #333; }
                header { text-align: center; padding: 20px; background: #eee; }
                footer { text-align: center; padding: 10px; font-size: 0.8em; background: #eee; }
                h1 { color: #00000; }
                title { color: #00000; }
                .product { border: 1px solid #ddd; margin: 10px; padding: 10px; }
                .product img { max-width: 150px; height: auto; display: block; margin: 5px auto; }
                .category { color: #e67e22; font-weight: bold; }
                .price { color: #d9534f; font-size: 1.2em; }
                .description { margin-top: 10px; }
            </style>
        </head>
        <body>
            <header>
                <h1>Lista de Productos Encontrados</h1>
            </header>
            <main>
        """

        for producto in productos_encontrados:
            html_content += f"""
            <div class="product">
                <h2>{producto.title}</h2>
                <{producto.title}">
                <p class="category">Categoría: {producto.category}</p>
                <p class="price">Precio: ${producto.price}</p>
                <p class="description">{producto.description}</p>
            </div>
            """


        html_content += """
            </main>
            <footer>
                <p>Catálogo de Productos - Iriem Da Luz Galindo 2ºCFGS</p>
            </footer>
        </body>
        </html>
        """

        output_path = "CatálogoBuscado.pdf"
        HTML(string=html_content).write_pdf(output_path)
        alert.showinfo(title="PDF generado", message=f"PDF guardado en: {output_path}")


def cargarProducto(listaDeProductos):
    app = ProductoApp(listaDeProductos)
    app.root.mainloop()
