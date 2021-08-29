import datetime


def seleccionar_pieza():
    response.delimiters = ('<?', '?>')
    crud = dict(header='', body=lambda row: DIV(A(SPAN("", _class="fa fa-dollar"),
                                                  _title="Vender", _href=URL('realizar_venta', args=row.id),
                                                  _class="btn btn-info btn-rounded mr-2"),
                                                _class="btn-inline"
                                                )
                )

    operaciones = [crud]
    config = dict(links=operaciones, **config_general)
    grid = SQLFORM.grid(db.pieza.cantidad > 0, **config)
    existencia = db(db.pieza.cantidad > 0).select()
    return locals()


def realizar_venta():
    id_seleccionada = request.args(0)
    pieza = db(db.pieza.id == id_seleccionada).select().first()
    # fecha_entrada = str(pieza.fecha_entrada.day) + "/" + str(pieza.fecha_entrada.month) + "/" + str(pieza.fecha_entrada.year)
    return locals()


def administrar():
    # Formulario buscar
    year = None

    form = FORM(INPUT(_name="year", _type="number", _class="form-control", _min="2000", _max="2999", _value=year),
                SPAN(INPUT(_type='submit', _class='btn btn-primary ml-2', _style="height:100%;", _value="Buscar")))

    if form.accepts(request, session, keepvalues=True):
        response.flash = ""
        year = form.vars.year

    # Tabla
    crud = dict(header='',
                body=lambda row: DIV(A(SPAN("", _class="icon magnifier icon-zoom-in glyphicon glyphicon-zoom-in"),
                                       _title="Detalles", _href=URL('detalles', args=[row.venta.id]),
                                       _class="btn btn-success btn-rounded"),
                                     A(SPAN("", _class="fa fa-pencil"),
                                       _title="Editar", _href=URL('editar', args=[row.venta.id]),
                                       _class="btn btn-info btn-rounded"),
                                     A(SPAN("", _class="icon trash icon-trash glyphicon glyphicon-trash"),
                                       _title="Eliminar", _href="#",
                                       _onclick="confirmDelete(" + str(row.venta.id) + ")",
                                       _class="btn btn-danger btn-rounded mr-2 delete"),
                                     _class="btn-inline"
                                     )
                )

    operaciones = [crud]
    fields = [db.venta.id, db.venta.fecha_salida, db.pieza_venta.codigo,
              db.pieza_venta.nombre, db.pieza_venta.cantidad, db.venta.precio_total]

    config = dict(fields=fields, links=operaciones, **config_general)

    db.venta.id.readable = False
    db.venta.id_pieza_venta.readable = False
    db.pieza_venta.id.readable = False

    consulta = (db.pieza_venta.id == db.venta.id_pieza_venta)

    if year == "" or year == None:
        consulta = (db.pieza_venta.id == db.venta.id_pieza_venta)
    else:
        consulta = (db.pieza_venta.id == db.venta.id_pieza_venta) & (
                db.venta.fecha_salida.year() == year)

    grid = SQLFORM.grid(consulta, **config)

    return locals()


def detalles():
    if not request.args(0):
        redirect(URL('administrar'))

    pieza = db.pieza_venta(request.args(0, cast=int)) or redirect(
        URL('administrar'))

    venta = db.venta(db.venta.id_pieza_venta == pieza.id)

    db.proveedor_venta.id.readable = False
    db.proveedor_venta.id_pieza_venta.readable = False

    proveedores = SQLFORM.grid(db.proveedor_venta.id_pieza_venta == pieza.id, **config_general)
    return locals()


def editar():
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

    form_venta.add_button('Volver', URL('administrar'),
                          _class="btn btn-danger mt-4")

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
        redirect(URL('administrar'))

    return locals()


def eliminar():
    if not request.args(0):
        redirect(URL('administrar'))
    id = request.args(0)
    db(db.pieza_venta.id == id).delete()
    session.flash = "Venta eliminada correctamente"
    redirect(URL('administrar'))
    return locals()


@request.restful()
def apiVenta():
    response.view = 'generic.json'

    def POST(*args, **vars):
        errorFecha = "False"

        fechaIn = vars["fecha_entrada"].split('-')
        fechaOut = vars["fecha_salida"].split('/')

        # Para insertar fecha de salida
        fechaString = fechaOut[2] + '-' + fechaOut[1] + '-' + fechaOut[0]

        auxFechaIn = datetime.datetime(int(fechaIn[0]), int(fechaIn[1]), int(fechaIn[2]))
        auxFechaOut = datetime.datetime(int(fechaOut[2]), int(fechaOut[1]), int(fechaOut[0]))

        # Si fecha de entrada es menor o igual que la de salida. Inserto
        if (auxFechaIn <= auxFechaOut):

            # Obtengo la cantidad de piezas que habia en la base de datos
            cantidad = vars["cantidad"]
            # Obtengo la cantidad seleccionada por el usuario
            cantidad_seleccionada = vars["cantidad_seleccionada"]

            total = int(cantidad) - int(cantidad_seleccionada)

            # Inicio la insercion en el registro historico con los datos que me llegan del otro lado
            pieza = db(db.pieza.id == vars["id"]).select().first()

            id_pieza_venta = db.pieza_venta.insert(codigo=pieza.codigo, nombre=pieza.nombre,
                                                   descripcion=pieza.descripcion, cantidad=cantidad_seleccionada,
                                                   unidad=pieza.unidad, precio_entrada=pieza.precio_entrada,
                                                   precio_salida=vars["precio_salida"],
                                                   fecha_entrada=pieza.fecha_entrada)

            id_venta = db.venta.insert(fecha_salida=fechaString, precio_total=vars["total"],
                                       id_pieza_venta=id_pieza_venta)

            # Proveedores Pieza venta
            proveedores = db((db.pieza_proveedor.id_pieza == pieza.id) & (
                    db.proveedor.id == db.pieza_proveedor.id_proveedor)).select(db.proveedor.nombre,
                                                                                db.proveedor.descripcion,
                                                                                db.proveedor.direccion,
                                                                                db.proveedor.telefono)

            for p in proveedores:
                db.proveedor_venta.insert(nombre=p.nombre, descripcion=p.descripcion, direccion=p.direccion,
                                          telefono=p.telefono,
                                          id_pieza_venta=id_pieza_venta)

            db(db.pieza.id == pieza.id).update(cantidad=total)
        else:
            errorFecha = "True"
        return locals()

    return locals()
