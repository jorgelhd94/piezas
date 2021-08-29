import StringIO


def salvar():
    return locals()


def cargar():
    form = FORM(INPUT(_type='file', _name='data', requires=[IS_NOT_EMPTY(error_message="Archivo no válido")]), BR(),
                INPUT(_type='submit', _class='btn btn-primary mt-2', _value="Cargar"))
    if form.process().accepted:
        __truncate()
        db.import_from_csv_file(form.vars.data.file, unique=False)
        response.flash = "La base de datos se ha cargado correctamente."

    return locals()


def export():
    s = StringIO.StringIO()
    db.export_to_csv_file(s)
    response.headers['Content-Type'] = 'text/csv'
    return s.getvalue()


def eliminar():
    if request.args(0):
        __truncate()
        redirect(URL("default", "index"))
    return locals()


def __truncate():
    db.pieza.truncate()
    db.proveedor.truncate()
    db.pieza_proveedor.truncate()
    db.pieza_venta.truncate()
    db.proveedor_venta.truncate()
    db.venta.truncate()
    db.pieza_entrada.truncate()
    db.proveedor_entrada.truncate()
    pass
