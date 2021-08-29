__author__ = 'Jorgito'


class Existe(Exception):
    """Clase base para excepciones en el módulo."""
    pass


@request.restful()
def api():
    response.view = 'generic.json'

    def GET(*args, **vars):
        if not request.env.request_method == 'GET':
            raise HTTP(403)
        proveedores = db().select(db.proveedor.ALL).as_list()
        return dict(proveedores=proveedores)

    def POST(*args, **vars):
        # raise HTTP(403)
        proveedor = vars
        respuesta = "ok"
        idProveedor = 0

        proveedor_data = dict(nombre=proveedor["nombre"],
                              descripcion=proveedor["descripcion"],
                              direccion=proveedor["direccion"],
                              telefono=proveedor["telefono"])

        # if db(db.unidad.tipo == tipo).select():
        #     raise HTTP(403)

        try:
            if db((db.proveedor.nombre == proveedor_data["nombre"]) & (db.proveedor.descripcion == proveedor_data["descripcion"]) & (db.proveedor.direccion == proveedor_data["direccion"]) & (db.proveedor.telefono == proveedor_data["telefono"])).select():
                raise Existe

            idProveedor = db.proveedor.insert(**proveedor_data)

        except Existe:
            respuesta = "existe"
        except Exception:
            respuesta = "error"
        
        return dict(respuesta=respuesta, id=idProveedor, **proveedor_data)
        # return dict(proveedor=proveedor)

    return locals()


def administrar():
    crud = dict(header='', body=lambda row: DIV(A(SPAN("", _class="icon magnifier icon-zoom-in glyphicon glyphicon-zoom-in"),
                                                  _title="Detalles",_href=URL('detalles', args=row.id), _class="btn btn-success btn-rounded mr-2"),
                                                A(SPAN("", _class="fa fa-pencil"),
                                                  _title="Editar", _href=URL('editar', args=row.id), _class="btn btn-info btn-rounded mr-2"),
                                                A(SPAN("", _class="icon trash icon-trash glyphicon glyphicon-trash"),
                                                  _title="Eliminar", _href="#", _onclick="confirmDelete(" + str(row.id) + ")", _class="btn btn-danger btn-rounded mr-2 delete"),
                                                _class="btn-inline"
                                                )
                )

    operaciones = [crud]
    config = dict(links=operaciones, **config_general)
    grid = SQLFORM.grid(db.proveedor, **config)
    return locals()


def crear():
    form = SQLFORM.factory(db.proveedor)
    form.add_button('Atrás', URL('administrar'),_class='btn btn-danger')
    
    if form.validate():    
        if db((db.proveedor.nombre == form.vars["nombre"]) & (db.proveedor.descripcion == form.vars["descripcion"]) & (db.proveedor.direccion == form.vars["direccion"]) & (db.proveedor.telefono == form.vars["telefono"])).select():
            response.flash = "El proveedor existe"
        else:
            id = db.proveedor.insert(**db.proveedor._filter_fields(form.vars))
            form.vars.proveedor = id
            session.flash = "Proveedor agregado correctamente"
            redirect(URL("proveedor", "administrar"))

    return locals()


def editar():
    if not request.args(0):
        redirect(URL('administrar'))
    registro = db.proveedor(request.args(0, cast=int)
                            ) or redirect(URL('administrar'))
    form = SQLFORM(db.proveedor, registro)    
    form.add_button('Atrás', URL('administrar'),_class='btn btn-danger')

    if form.validate():
        if db((db.proveedor.id != registro.id) & (db.proveedor.nombre == form.vars["nombre"]) & (db.proveedor.descripcion == form.vars["descripcion"]) & (db.proveedor.direccion == form.vars["direccion"]) & (db.proveedor.telefono == form.vars["telefono"])).select():
            response.flash = "El proveedor existe"
        else:
            db.proveedor(registro.id).update(**db.proveedor._filter_fields(form.vars))
            session.flash = "Proveedor actualizado correctamente"
            redirect(URL("proveedor", "administrar"))
    return locals()


def eliminar():
    if not request.args(0):
        redirect(URL('administrar'))
    id = request.args(0)
    db(db.proveedor.id == id).delete()
    # session.flash = "Proveedor eliminado correctamente"
    redirect(URL('administrar'))
    return locals()


def detalles():
    if not request.args(0):
        redirect(URL('administrar'))
    proveedor = db.proveedor(request.args(0, cast=int)
                             ) or redirect(URL('administrar'))

    piezas = db((db.pieza_proveedor.id_proveedor == proveedor.id) & (
        db.pieza.id == db.pieza_proveedor.id_pieza)).select(db.pieza.ALL)
    
    return locals()
