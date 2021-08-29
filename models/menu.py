# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

icon = {"Inicio": "fa-home", "Ventas": "fa-money", "Piezas": "fa-desktop",
        "Proveedores": "fa-user",
        "Estadísticas": "fa-signal",
        "Eliminar todo": "fa-trash",
        "Base de datos": "fa-database",
        "Usuario": "fa-user-circle"}

response.menu = [
    (T('Inicio'), False, URL('default', 'index'), [])
]

T.force('es-es')


# background: #ef5350
# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if not configuration.get('app.production'):
    _app = request.application
    response.menu += [
        # (T('My Sites'), False, URL('admin', 'default', 'site')),
        (T('Piezas'), False, 'pieza', [
            (T('Añadir pieza'), False, URL(_app, 'pieza', 'crear')),
            (T('Administrar pieza'), False, URL(_app, 'pieza', 'administrar')),
            # (T('Dar salida'), False, URL(_app, 'pieza', 'salida')),
        ]),
        (T('Proveedores'), False, 'proveedor', [
            (T('Añadir proveedor'), False, URL(_app, 'proveedor', 'crear')),
            (T('Administrar proveedor'), False, URL(
                _app, 'proveedor', 'administrar')),
        ]),
        (T('Ventas'), False, 'venta', [
            (T('Realizar venta'), False, URL(_app, 'venta', 'seleccionar_pieza')),
            (T('Administrar ventas'), False, URL(_app, 'venta', 'administrar')),
        ]),
        (T('Estadísticas'), False, 'estadisticas', [
            (T('Por Pieza'), False, URL(_app, 'estadisticas', 'piezas')),
            (T('General'), False, URL(_app, 'estadisticas', 'estadistica_general')),
            # (T('Dar salida'), False, URL(_app, 'pieza', 'salida')),
        ]),        
        (T('Base de datos'), False, 'base_datos', [
            (T('Salvar base de datos'), False, URL(_app, 'base_datos', 'salvar')),
            (T('Cargar salva'), False, URL(_app, 'base_datos', 'cargar')),
        ]),
        (T('Eliminar todo'), False, URL(_app, 'base_datos', 'eliminar')),
    ]
