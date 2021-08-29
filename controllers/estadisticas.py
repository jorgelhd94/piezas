def piezas():
    # response.delimiters = ('<?', '?>')
    crud = dict(header='', body=lambda row: DIV(A(SPAN("", _class="fa fa-search"),
                                                  _href=URL('estadistica_pieza', args=row.id),
                                                  _class="btn btn-info btn-rounded mr-2"),
                                                _class="btn-inline"
                                                )
                )

    operaciones = [crud]
    config = dict(links=operaciones, **config_general)
    grid = SQLFORM.grid(db.pieza, **config)
    existencia = db(db.pieza.id > 0).select()
    return locals()


def estadistica_pieza():
    if not request.args(0):
        redirect(URL('piezas'))
    pieza = db.pieza(request.args(0, cast=int)) or redirect(
        URL('pieza', 'administrar'))

    year = request.now.year

    form = FORM(INPUT(_name="year", _type="number", _class="form-control", _min="2000", _max="2999", _value=year),
                SPAN(INPUT(_type='submit', _class='btn btn-primary ml-2', _style="height:100%;", _value="Buscar")))

    # rows = db((db.venta.fecha_salida.month() == 11) & (db.venta.fecha_salida.year(
    # ) == year) & (db.venta.id_pieza_venta == db.pieza_venta.id) & (db.pieza_venta.codigo == pieza.codigo)).select(db.pieza_venta.cantidad)

    if form.accepts(request, session, keepvalues=True):
        response.flash = ""
        year = form.vars.year

    valores = __obtener_estadisticas(year, pieza.codigo)
    return locals()


def estadistica_general():
    year = request.now.year

    form = FORM(INPUT(_name="year", _type="number", _class="form-control", _min="2000", _max="2999", _value=year),
                SPAN(INPUT(_type='submit', _class='btn btn-primary ml-2', _style="height:100%;", _value="Buscar")))

    # rows = db((db.venta.fecha_salida.month() == 11) & (db.venta.fecha_salida.year(
    # ) == year) & (db.venta.id_pieza_venta == db.pieza_venta.id) & (db.pieza_venta.codigo == pieza.codigo)).select(db.pieza_venta.cantidad)

    if form.accepts(request, session, keepvalues=True):
        response.flash = ""
        year = form.vars.year

    valores_entradas, mesesEntradas = __obtener_estadisticas_general_entradas(year)
    valores_ventas, mesesVentas = __obtener_estadisticas_general_ventas(year)

    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
             "Noviembre", "Diciembre"]

    return locals()


def __obtener_estadisticas_general_entradas(year):
    valores = []
    meses = {}

    for i in range(1, 13):
        rows = db((db.pieza_entrada.fecha_entrada.month() == i) & (db.pieza_entrada.fecha_entrada.year(
        ) == year)).select()

        cantidad = 0

        for j in rows:
            cantidad += j.cantidad

        valores.append(cantidad)

        mes = db((db.pieza_entrada.fecha_entrada.month() == i) & (db.pieza_entrada.fecha_entrada.year(
        ) == year)).select(db.pieza_entrada.fecha_entrada, db.pieza_entrada.codigo, db.pieza_entrada.cantidad,
                           orderby=db.pieza_entrada.fecha_entrada)

        meses[i] = {}

        for m in mes:
            try:
                meses[i][m.fecha_entrada.day]
            except:
                meses[i][m.fecha_entrada.day] = 0
            meses[i][m.fecha_entrada.day] += m.cantidad

    return valores, meses


def __obtener_estadisticas_general_ventas(year):
    valores = []
    meses = {}

    for i in range(1, 13):
        rows = db((db.venta.fecha_salida.month() == i) & (db.venta.fecha_salida.year(
        ) == year) & (db.venta.id_pieza_venta == db.pieza_venta.id)).select(db.pieza_venta.cantidad)

        cantidad = 0

        for j in rows:
            cantidad += j.cantidad

        mes = db((db.venta.fecha_salida.month() == i) & (db.venta.fecha_salida.year() == year) & (
                db.venta.id_pieza_venta == db.pieza_venta.id)).select(db.venta.fecha_salida,
                                                                      db.pieza_venta.cantidad,
                                                                      orderby=db.venta.fecha_salida)

        meses[i] = {}

        for m in mes:
            try:
                meses[i][m.venta.fecha_salida.day]
            except:
                meses[i][m.venta.fecha_salida.day] = 0
            meses[i][m.venta.fecha_salida.day] += m.pieza_venta.cantidad

        valores.append(cantidad)

    return valores, meses


def __obtener_estadisticas(year, codigo, general=False):
    valores = []
    consulta = (db.pieza_venta.codigo == codigo)

    if general:
        consulta = (db.pieza_venta.codigo != "")

    for i in range(1, 13):
        rows = db((db.venta.fecha_salida.month() == i) & (db.venta.fecha_salida.year(
        ) == year) & (db.venta.id_pieza_venta == db.pieza_venta.id) & consulta).select(db.pieza_venta.cantidad)

        cantidad = 0

        for j in rows:
            cantidad += j.cantidad

        valores.append(cantidad)

    return valores
