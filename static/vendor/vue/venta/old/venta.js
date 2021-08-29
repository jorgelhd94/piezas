new Vue({
    el: '#container',
    data: {
        informacionPieza:{
            id:'',
            codigo:'',
            nombre:'',
            descripcion:'',
            cantidad:'',
            cantidad_seleccionada:0,
            unidad:'',
            precio_entrada:'',
            precio_salida:0.00,
            fecha_entrada:'',
            fecha_salida:'',
            total:'',
        },        
        precio_nuevo: 0.00,
        id_pieza:id_js,
        cantidadError: false,
        fechaVacia: false,
        fechaError: false
    },
    computed: {
        montoTotal(){
            var cant=this.informacionPieza.cantidad_seleccionada;
            var precio=this.informacionPieza.precio_salida;

            if(this.precio_nuevo > 0){
                precio = this.precio_nuevo;
            }

            this.informacionPieza.total=cant*precio;
            return this.informacionPieza.total;
        },
        cantidad_virtual(){
            var virtual=this.informacionPieza.cantidad-this.informacionPieza.cantidad_seleccionada;
            return virtual;
        }
    },
    created(){
        this.infoPieza();
    },
    methods:{
        formatFecha(){
            var fechaAux = this.informacionPieza.fecha_entrada.split("-");

            return fechaAux[2] + "/" + fechaAux[1] + "/" + fechaAux[0]
        },
        infoPieza(){
            const data={
                operacion:'info',
                id:this.id_pieza,
            };
            axios.post(urlService,data).then(respuesta=>{
                this.informacionPieza.id=respuesta.data.pieza[0].id;
                this.informacionPieza.codigo=respuesta.data.pieza[0].codigo;
                this.informacionPieza.nombre=respuesta.data.pieza[0].nombre;
                this.informacionPieza.descripcion=respuesta.data.pieza[0].descripcion;
                this.informacionPieza.cantidad=respuesta.data.pieza[0].cantidad;
                this.informacionPieza.unidad=respuesta.data.pieza[0].unidad;
                this.informacionPieza.precio_entrada=respuesta.data.pieza[0].precio_entrada;
                this.informacionPieza.precio_salida=respuesta.data.pieza[0].precio_salida;
                this.informacionPieza.fecha_entrada=respuesta.data.pieza[0].fecha_entrada;
            });
        },
        ejecutarSalida(){
            if((this.informacionPieza.cantidad_seleccionada <= 0) || 
               (this.informacionPieza.cantidad_seleccionada > parseInt(this.informacionPieza.cantidad_seleccionada))){
                swal("Error", "Existen errores en el formulario.", "error");
                this.cantidadError = true;
            }
            else if(document.getElementById('fecha').value === ""){
                swal("Error", "Existen errores en el formulario.", "error");
                this.fechaVacia = true;
            }
            else{
                let data={
                    operacion:'salida',
                    id:this.informacionPieza.id,
                    codigo:this.informacionPieza.codigo,
                    nombre:this.informacionPieza.nombre,
                    descripcion:this.informacionPieza.descripcion,
                    cantidad:this.informacionPieza.cantidad,
                    cantidad_seleccionada:this.informacionPieza.cantidad_seleccionada,
                    unidad:this.informacionPieza.unidad,
                    precio_entrada:this.informacionPieza.precio_entrada,
                    precio_salida:this.informacionPieza.precio_salida,
                    fecha_entrada:this.informacionPieza.fecha_entrada,
                    fecha_salida: document.getElementById('fecha').value,
                    total:this.informacionPieza.total,
                };

                if(this.precio_nuevo > 0){
                    data.precio_salida = this.precio_nuevo;
                }
                // console.log(data)
                axios.post(urlService,data).then(respuesta=>{
                    if(respuesta.data.errorFecha === "True"){
                        this.fechaError = true;                        
                    }
                    else{
                        swal({
                            title: "Correcto",
                            text: "La operación ha sido realizada correctamente.",
                            type: "success",
                            allowEscapeKey: false
                        }, function(isConfirm){
                            // alert("Hola")
                            location.href = urlRedirigir;
                        });
                    }
                    
                });
            }
            
        }
    }
  });
  