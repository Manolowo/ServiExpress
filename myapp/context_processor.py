def totalCarrito(request):
    total = 0
    if "carrito" in request.session.keys():
        for key, value in request.session["carrito"].items():
            total += (value["acumulado"])
    return {"totalCarrito": total}
