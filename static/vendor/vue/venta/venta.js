new Vue({
    el: '#container',
    delimiters: ["[[", "]]"],
    data: {
        informacionPieza: pieza,
        cantidad_seleccionada: 0,
        precio_nuevo: 0.00,
        id_pieza: id_js,
        cantidadError: false,
        fechaVacia: false,
        fechaError: false
    },
    computed: {
        montoTotal() {
            var cant = this.cantidad_seleccionada;
            var precio = this.informacionPieza.precio_salida;

            if (this.precio_nuevo > 0) {
                precio = this.precio_nuevo;
            }

            this.informacionPieza.total = cant * precio;
            return this.informacionPieza.total.toFixed(2);
        },

        cantidad_virtual() {
            var virtual = this.informacionPieza.cantidad - this.cantidad_seleccionada;
            return virtual;
        }
    },
    methods: {
        formatFecha() {
            var fechaAux = this.informacionPieza.fecha_entrada.split("-");
            return fechaAux[2] + "/" + fechaAux[1] + "/" + fechaAux[0]
        },
        ejecutarSalida() {
            if (document.getElementById('fecha').value === "") {
                swal("Error", "Existen errores en el formulario.", "error");
                this.fechaVacia = true;
            } else {
                let data = {
                    id: this.informacionPieza.id,
                    // codigo: this.informacionPieza.codigo,
                    // nombre: this.informacionPieza.nombre,
                    // descripcion: this.informacionPieza.descripcion,
                    cantidad: this.informacionPieza.cantidad,
                    cantidad_seleccionada: this.cantidad_seleccionada,
                    // unidad: this.informacionPieza.unidad,
                    // precio_entrada: this.informacionPieza.precio_entrada,
                    precio_salida: this.informacionPieza.precio_salida,
                    fecha_entrada: this.informacionPieza.fecha_entrada,
                    fecha_salida: document.getElementById('fecha').value,
                    total: this.montoTotal,
                };

                if (this.precio_nuevo > 0) {
                    data.precio_salida = this.precio_nuevo;
                }

                axios.post(urlService, data).then(respuesta => {
                    if (respuesta.data.errorFecha === "True") {
                        this.fechaError = true;
                        swal("Error", "Existen errores en el formulario.", "error");
                    } else {
                        swal({
                            title: "Correcto",
                            text: "La operación ha sido realizada correctamente.",
                            type: "success",
                            allowEscapeKey: false
                        }, function (isConfirm) {
                            // alert("Hola")
                            location.href = urlRedirigir;
                        });
                    }

                }).catch(error => {
                    console.log(error);
                });
            }

        }
    }
});
  