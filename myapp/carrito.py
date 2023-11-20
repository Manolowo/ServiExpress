class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get('carrito')
        if not carrito:
            self.session['carrito'] = {}
            self.carrito = self.session['carrito']
        else:
            self.carrito = carrito

    def agregar(self, servicio):
        id = str(servicio.ser_id)
        if id not in self.carrito.keys():
            self.carrito[id]={
                "id_prod": servicio.ser_id,
                "nombre": servicio.ser_desc,
                "acumulado": servicio.ser_prec,
            }
        else:
            self.carrito[id]["acumulado"] += servicio.ser_prec
        self.guardarCarrito()

    def guardarCarrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True
    
    def eliminar(self, servicio):
        id= str(servicio.id_prod)
        if id in self.carrito:
            del self.carrito[id]
            self.guardarCarrito()

    def restar(self, servicio):
        id= str(servicio.ser_id)
        if id in self.carrito.keys():
            self.carrito[id]["acumulado"]-= servicio.ser_prec

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True

