__author__ = 'Jorgito'

import datetime

def crear():
    response.delimiters = ('<?', '?>')
    # formPieza = SQLFORM(db.pieza)
    # gridProveedor = SQLFORM.grid(db.unidad)
    return locals()


def administrar():
    crud = dict(header='', body=lambda row: DIV(
        A(SPAN("", _class="fa fa-plus"), _title="Aumentar cantidad", _href=URL('aumentar_cantidad', args=[row.id]),
          _class="btn btn-primary btn-rounded text-light"),
        A(SPAN("", _class="fa fa-dollar"), _title="Vender",
          _href=URL('venta', 'realizar_venta', args=row.id),
          _class="btn btn-info btn-rounded mr-2"),
        A(SPAN("", _class="icon magnifier icon-zoom-in glyphicon glyphicon-zoom-in"), _title="Detalles",
          _href=URL('detalles', args=[row.id]), _class="btn btn-success btn-rounded"),
        A(SPAN("", _class="fa fa-pencil"), _title="Editar",
          _href=URL('editar', args=[row.id]), _class="btn btn-info btn-rounded"),
        A(SPAN("", _class="icon trash icon-trash glyphicon glyphicon-trash"), _title="Eliminar",
          _href="#", _onclick="confirmDelete(" + str(row.id) + ")", _class="btn btn-danger btn-rounded mr-2 delete"),
        _class="btn-inline"
    )
                )

    operaciones = [crud]

    config = dict(links=operaciones, **config_general)
    grid = SQLFORM.grid(db.pieza, **config)
    return locals()


def detalles():
    if not request.args(0):
        redirect(URL('pieza', 'administrar'))

    pieza = db.pieza(request.args(0, cast=int)) or redirect(
        URL('pieza', 'administrar'))

    session.id_pieza = pieza.id

    pieza_entrada = db((db.pieza_entrada.codigo == pieza.codigo)).select(db.pieza_entrada.id,
                                                                         db.pieza_entrada.fecha_entrada,
                                                                         db.pieza_entrada.codigo,
                                                                         db.pieza_entrada.nombre,
                                                                         db.pieza_entrada.descripcion,
                                                                         db.pieza_entrada.cantidad)

    pieza_venta = db((db.pieza_venta.codigo == pieza.codigo) & (db.venta.id_pieza_venta == db.pieza_venta.id)).select(
        db.venta.id, db.venta.fecha_salida, db.venta.precio_total, db.pieza_venta.id, db.pieza_venta.codigo,
        db.pieza_venta.nombre,
        db.pieza_venta.descripcion,
        db.pieza_venta.cantidad)

    proveedores = db((db.pieza_proveedor.id_pieza == pieza.id) & (
            db.proveedor.id == db.pieza_proveedor.id_proveedor)).select(db.proveedor.nombre,
                                                                        db.proveedor.descripcion,
                                                                        db.proveedor.direccion,
                                                                        db.proveedor.telefono)

    return locals()


def editar():
    response.delimiters = ('<?', '?>')

    # Verificar que se pase un id por la url
    if not request.args(0):
        redirect(URL('pieza', 'administrar'))

    # Obtener la pieza segun id
    pieza = db.pieza(request.args(0, cast=int)) or redirect(
        URL('pieza', 'administrar'))

    proveedores = db((db.pieza_proveedor.id_pieza == pieza.id) & (
            db.pieza_proveedor.id_proveedor == db.proveedor.id)).select(db.proveedor.ALL).as_list()

    # Formato de fecha a dd/mm/aaaa
    fecha = pieza.fecha_entrada
    fecha = str(fecha.day) + "/" + str(fecha.month) + "/" + str(fecha.year)

    return locals()


def eliminar():
    if not request.args(0):
        redirect(URL('administrar'))
    id = request.args(0)
    db(db.pieza.id == id).delete()
    redirect(URL('administrar'))
    return locals()


def aumentar_cantidad():
    if not request.args(0):
        redirect(URL('administrar'))
    id = request.args(0)
    pieza = db(db.pieza.id == id).select().first()
    cantidad_real = pieza.cantidad

    # form = SQLFORM.factory(
    #     Field('cantidad', 'integer', requires=IS_NOT_EMPTY())
    # )
    # form.add_button('Volver', URL('administrar'), _class="btn btn-danger")

    form = FORM(LABEL("Aumentar cantidad:"),
                INPUT(_type="number", _min="1", _value="1", _class="form-control", _name="cantidad",
                      requires=IS_NOT_EMPTY(error_message="No es válido")), BR(),
                INPUT(_type="submit", _value="Confirmar", _class="btn btn-primary mr-2"))
    form.add_button('Volver', URL('administrar'), _class="btn btn-danger")

    if form.process().accepted:
        cant = form.vars["cantidad"]
        total = int(cantidad_real) + int(cant)
        db(db.pieza.id == id).update(cantidad=total)

        id_pieza_entrada = db.pieza_entrada.insert(codigo=pieza.codigo, nombre=pieza.nombre,
                                                   descripcion=pieza.descripcion, cantidad=cant,
                                                   unidad=pieza.unidad, precio_entrada=pieza.precio_entrada,
                                                   precio_salida=pieza.precio_salida, fecha_entrada=datetime.datetime.now().date())

        for prov in db((db.pieza_proveedor.id_pieza == pieza.id) & (
                db.pieza_proveedor.id_proveedor == db.proveedor.id)).select(db.proveedor.ALL):
            db.proveedor_entrada.insert(
                id_pieza_entrada=id_pieza_entrada, nombre=prov.nombre, descripcion=prov.descripcion,
                direccion=prov.direccion, telefono=prov.telefono)

        session.flash = "La cantidad ha aumentado"
        redirect(URL('administrar'))

    elif form.errors:
        response.flash = 'El formulario tiene errores'

    return dict(cantidad_real=cantidad_real, form=form)


"""
**********************************************
A continuacion se exponen los crud de las entradas
**********************************************
"""


def detalles_entrada():
    if not request.args(0) and not session.id_pieza:
        redirect(URL('administrar'))

    pieza_entrada = db.pieza_entrada(request.args(0, cast=int)) or redirect(URL('pieza', 'administrar'))

    db.proveedor_entrada.id.readable = False
    db.proveedor_entrada.id_pieza_entrada.readable = False

    proveedores = SQLFORM.grid(db.proveedor_entrada.id_pieza_entrada == pieza_entrada.id, **config_general)
    return locals()


def editar_entrada():
    if not request.args(0) and not session.id_pieza:
        redirect(URL('administrar'))

    id_pieza_entrada = request.args(0, cast=int) or redirect(
        URL('administrar'))

    pieza_entrada = db.pieza_entrada(id_pieza_entrada)
    fecha_entrada = pieza_entrada.fecha_entrada

    fecha_entrada_aux = str(fecha_entrada.day) + "/" + \
                        str(fecha_entrada.month) + "/" + str(fecha_entrada.year)

    requires = IS_NOT_EMPTY(error_message="Valor no válido")
    require_fecha = IS_DATE_IN_RANGE(
        format=T('%d/%m/%Y'))

    form_entrada = FORM(SPAN("Fecha de entrada"), INPUT(_type="text", _id="fecha", _class="form-control",
                                                        _name="fecha_entrada", _value=fecha_entrada_aux,
                                                        requires=[requires, require_fecha]),
                        BR(), SPAN("Nueva Cantidad"), INPUT(_type="number", _min="1", _class="form-control",
                                                            _name="cantidad", _value=pieza_entrada.cantidad,
                                                            requires=requires),
                        BR(), INPUT(_type="submit", _value="Editar", _class="btn btn-primary mr-2"),
                        _class="form-group mb-5")

    form_entrada.add_button('Volver', URL('detalles', args=[session.id_pieza]),
                            _class="btn btn-danger")

    if form_entrada.process().accepted:
        fecha_entrada_input = form_entrada.vars["fecha_entrada"]

        cantidad = form_entrada.vars["cantidad"]

        db(db.pieza_entrada.id == pieza_entrada.id).update(
            fecha_entrada=fecha_entrada_input, cantidad=cantidad)

        # db(db.pieza.id == id).update(cantidad=total)
        session.flash = "La entrada ha sido actualizada"
        redirect(URL('detalles', args=[session.id_pieza]))

    return locals()


def eliminar_entrada():
    if not request.args(0):
        redirect(URL('administrar'))

    id = request.args(0)
    db(db.pieza_entrada.id == id).delete()
    session.flash = "Entrada eliminada correctamente"
    redirect(URL('detalles', args=[session.id_pieza]))
    return locals()


"""
**********************************************
A continuacion se exponen los crud de las ventas
**********************************************
"""


def detalles_venta():
    if not request.args(0):
        redirect(URL('administrar'))

    pieza = db.pieza_venta(request.args(0, cast=int)) or redirect(
        URL('administrar'))

    venta = db.venta(db.venta.id_pieza_venta == pieza.id)

    db.proveedor_venta.id.readable = False
    db.proveedor_venta.id_pieza_venta.readable = False

    proveedores = SQLFORM.grid(db.proveedor_venta.id_pieza_venta == pieza.id, **config_general)
    return locals()


def editar_venta():
    if not request.args(0):
        redirect(URL('administrar'))

    id = request.args(0, cast=int) or redirect(
        URL('administrar'))

    pieza = db.pieza_venta(id)
    venta = db.venta(db.venta.id_pieza_venta == id)
    fecha_salida = venta.fecha_salida

    fecha_salida_aux = str(fecha_salida.day) + "/" + \
                       str(fecha_salida.month) + "/" + str(fecha_salida.year)

    requires = IS_NOT_EMPTY(error_message="Valor no válido")
    require_fecha = IS_DATE_IN_RANGE(
        format=T('%d/%m/%Y'), minimum=fecha_salida)

    form_venta = FORM(SPAN("Fecha de salida"), INPUT(_type="text", _id="fecha", _class="form-control",
                                                     _name="fecha_salida", _value=fecha_salida_aux,
                                                     requires=[requires, require_fecha]),
                      BR(), SPAN("Cantidad"), INPUT(_type="number", _min="1", _class="form-control",
                                                    _name="cantidad", _value=pieza.cantidad, requires=requires),
                      BR(), SPAN("Precio de salida"),
                      INPUT(_type="number", _min="0", _step="0.01", _class="form-control",
                            _name="precio_salida", _value=pieza.precio_salida, requires=requires),
                      SPAN(I(_class="fa fa-info-circle text-info"), " Usar la coma(,) como separador"),
                      BR(), INPUT(_type="submit", _value="Editar", _class="btn btn-primary mr-2 mt-4"),
                      _class="form-group mb-5")

    form_venta.add_button('Volver', URL('detalles', args=[session.id_pieza]),
                          _class="btn btn-danger  mt-4")

    if form_venta.process().accepted:
        fecha_salida_input = form_venta.vars["fecha_salida"]

        cantidad_venta = form_venta.vars["cantidad"]
        precio_salida = form_venta.vars["precio_salida"]

        precio_total = float(precio_salida) * int(cantidad_venta)

        db(db.venta.id == venta.id).update(
            fecha_salida=fecha_salida_input, precio_total=precio_total)
        pieza.update_record(cantidad=cantidad_venta,
                            precio_salida=precio_salida)

        # db(db.pieza.id == id).update(cantidad=total)
        session.flash = "La venta ha sido actualizada"
        redirect(URL('detalles', args=[session.id_pieza]))

    return locals()


def eliminar_venta():
    if not request.args(0):
        redirect(URL('administrar'))
    id = request.args(0)
    db(db.pieza_venta.id == id).delete()
    session.flash = "Venta eliminada correctamente"
    redirect(URL('detalles', args=[session.id_pieza]))
    return locals()


"""
****************************************
A continuacion se exponen los services
****************************************
"""


@request.restful()
def api():
    response.view = 'generic.json'

    def GET(*args, **vars):
        #     if not request.env.request_method == 'GET': raise HTTP(403)
        #     proveedores = db().select(db.proveedor.ALL).as_list()
        return dict()

    def POST(*args, **vars):
        # raise HTTP(403)
        pieza = vars["pieza"]
        proveedores_list = vars["proveedores_list"]
        respuesta = "ok"
        idProveedor = 0

        fechaIn = pieza["fechaIn"].split('/')
        fechaString = fechaIn[2] + '-' + fechaIn[1] + '-' + fechaIn[0]

        pieza_data = dict(codigo=pieza["codigo"], nombre=pieza["nombre"],
                          descripcion=pieza["descripcion"], cantidad=pieza["cantidad"],
                          unidad=pieza["unidad"], precio_entrada=pieza["precioIn"],
                          precio_salida=pieza["precioOut"], fecha_entrada=fechaString)

        # if db(db.unidad.tipo == tipo).select():
        #     raise HTTP(403)

        try:
            id_pieza = db.pieza.insert(**pieza_data)

            id_pieza_entrada = db.pieza_entrada.insert(**pieza_data)

            for prov in proveedores_list:
                db.pieza_proveedor.insert(
                    id_pieza=id_pieza, id_proveedor=prov["id"])

                db.proveedor_entrada.insert(
                    id_pieza_entrada=id_pieza_entrada, nombre=prov["nombre"], descripcion=prov["descripcion"],
                    direccion=prov["direccion"], telefono=prov["telefono"])

        except Exception:
            respuesta = "error"

        return dict(respuesta=respuesta)
        # return dict(proveedor=proveedor)

    return locals()


@request.restful()
def apiEditar():
    """
    Servicio para editar una pieza
    """
    response.view = 'generic.json'

    def GET(*args, **vars):
        #     if not request.env.request_method == 'GET': raise HTTP(403)
        #     proveedores = db().select(db.proveedor.ALL).as_list()
        return dict()

    def POST(*args, **vars):
        # raise HTTP(403)
        pieza = vars["pieza"]
        proveedores_list = vars["proveedores_list"]
        respuesta = "ok"
        idProveedor = 0

        fechaIn = pieza["fechaIn"].split('/')
        fechaString = fechaIn[2] + '-' + fechaIn[1] + '-' + fechaIn[0]

        pieza_data = dict(codigo=pieza["codigo"], nombre=pieza["nombre"],
                          descripcion=pieza["descripcion"], cantidad=pieza["cantidad"],
                          unidad=pieza["unidad"], precio_entrada=pieza["precioIn"],
                          precio_salida=pieza["precioOut"], fecha_entrada=fechaString)

        # Verificar si aumento la cantidad. Para asi dar nueva entrada
        cantidad_antigua = db.pieza(pieza["id"]).cantidad
        cantidad_nueva = int(pieza["cantidad"]) - cantidad_antigua if cantidad_antigua < int(
            pieza["cantidad"]) else int(pieza["cantidad"])

        registrar_entrada = cantidad_antigua != int(pieza["cantidad"]) and cantidad_nueva != 0

        if registrar_entrada:
            id_pieza_entrada = db.pieza_entrada.insert(codigo=pieza["codigo"], nombre=pieza["nombre"],
                                                       descripcion=pieza["descripcion"], cantidad=cantidad_nueva,
                                                       unidad=pieza["unidad"], precio_entrada=pieza["precioIn"],
                                                       precio_salida=pieza["precioOut"], fecha_entrada=datetime.datetime.now().date())

            for prov in proveedores_list:
                db.proveedor_entrada.insert(
                    id_pieza_entrada=id_pieza_entrada, nombre=prov["nombre"], descripcion=prov["descripcion"],
                    direccion=prov["direccion"], telefono=prov["telefono"])

        # Actualizo la pieza
        try:
            db(db.pieza.id == pieza["id"]).update(**pieza_data)
            db(db.pieza_proveedor.id_pieza == pieza["id"]).delete()

            for prov in proveedores_list:
                db.pieza_proveedor.insert(
                    id_pieza=pieza["id"], id_proveedor=prov["id"])

        except Exception:
            respuesta = "error"

        return dict(respuesta=respuesta)
        # return dict(proveedor=proveedor)

    return locals()


@request.restful()
def verificarCodigo():
    response.view = 'generic.json'

    def GET(*args, **vars):
        #     if not request.env.request_method == 'GET': raise HTTP(403)
        #     proveedores = db().select(db.proveedor.ALL).as_list()
        return dict()

    def POST(*args, **vars):
        # raise HTTP(403)
        codigo = vars["value"]
        respuesta = "ok"

        if db(db.pieza.codigo == codigo).select():
            respuesta = "error"

        return dict(respuesta=respuesta)
        # return dict(proveedor=proveedor)

    return locals()


@request.restful()
def verificarCodigoEditar():
    response.view = 'generic.json'

    def GET(*args, **vars):
        #     if not request.env.request_method == 'GET': raise HTTP(403)
        #     proveedores = db().select(db.proveedor.ALL).as_list()
        return dict()

    def POST(*args, **vars):
        # raise HTTP(403)
        codigo = vars["value"]
        respuesta = "ok"

        if db(db.pieza.codigo == codigo).select() and codigo != vars["origin"]:
            respuesta = "error"

        return dict(respuesta=respuesta)
        # return dict(proveedor=proveedor)

    return locals()
