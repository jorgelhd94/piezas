/**
 * Created by Jorgito on 25/09/2019.
 */

//Rules
VeeValidate.extend('required', VeeValidateRules.required);
VeeValidate.extend('min_value', VeeValidateRules.min_value);
VeeValidate.extend('numeric', VeeValidateRules.numeric);
VeeValidate.extend('regex', VeeValidateRules.regex);



VeeValidate.localize({
    es: {
        messages: {
            "alpha": "El campo {_field_} solo debe contener letras",
            "alpha_dash": "El campo {_field_} solo debe contener letras, n�meros y guiones",
            "alpha_num": "El campo {_field_} solo debe contener letras y n�meros",
            "alpha_spaces": "El campo {_field_} solo debe contener letras y espacios",
            "between": "El campo {_field_} debe estar entre {min} y {max}",
            "confirmed": "El campo {_field_} no coincide",
            "digits": "El campo {_field_} debe ser num�rico y contener exactamente {length} d�gitos",
            "dimensions": "El campo {_field_} debe ser de {width} p�xeles por {height} p�xeles",
            "email": "El campo {_field_} debe ser un correo electr�nico v�lido",
            "excluded": "El campo {_field_} debe ser un valor v�lido",
            "ext": "El campo {_field_} debe ser un archivo v�lido",
            "image": "El campo {_field_} debe ser una imagen",
            "oneOf": "El campo {_field_} debe ser un valor v�lido",
            "integer": "El campo {_field_} debe ser un entero",
            "length": "El largo del campo {_field_} debe ser {length}",
            "max": "El campo {_field_} no debe ser mayor a {length} caracteres",
            "max_value": "El campo {_field_} debe de ser {max} o menor",
            "mimes": "El campo ${field} debe ser un tipo de archivo v�lido",
            "min": "El campo {_field_} debe tener al menos {length} caracteres",
            "min_value": "El campo {_field_} debe ser {min} o superior",
            "numeric": "El campo {_field_} debe contener solo caracteres numéricos",
            "regex": "El formato del campo {_field_} no es válido",
            "required": "El campo {_field_} es obligatorio",
            "required_if": "El campo {_field_} es obligatorio",
            "size": "El campo {_field_} debe ser menor a {size}KB"
        }
    }

});

VeeValidate.localize('es');

//Error
// VeeValidate.configure({
//     classes:{
//         invalid: 'has-error'
//     }
// });

// Add a rule.
// VeeValidate.extend('date', {
//     validate(value) {
//         try {
//             let fecha = value.split("/");
//             let dateObject = new Date(fecha[2], fecha[1] - 1, fecha[0]); 
//         } catch (error) {
//             console.log("Errorsazo!!!")
//         }
//     },
//     message: 'La Fecha no es válida. Debe ser dd/mm/aaaa.'
// });

// Register the component globally.
Vue.component('validation-provider', VeeValidate.ValidationProvider);
Vue.component('validation-observer', VeeValidate.ValidationObserver);


new Vue({
    el: "#container",
    data: {
        mostrar_pag_1: true,
        codigo: piezaEditar.codigo,
        codigoError: false,
        nombre: piezaEditar.nombre,
        descripcion: piezaEditar.descripcion,
        cantidad:piezaEditar.cantidad,
        unidad: piezaEditar.unidad,
        precioIn: piezaEditar.precioIn,
        precioOut: piezaEditar.precioOut,
        fechaIn:"",
        fechaError:false,
        fechaValid: false, 
        proveedor_data: {
            nombre: "",
            descripcion: "",
            direccion: "",
            telefono: ""
        },
        proveedores: [],
        proveedores_api:[{}]
    },
    created: function () {
        this.getProveedores();
        this.initProveedores();        
    },
    computed:{
       
    },
    methods: {
        initProveedores(){
            /* Verificar que existan proveedores*/

            if(this.proveedores.length == 1){
                this.proveedores = [];
                this.proveedores.push({
                    id: 0,
                    nombre: "",
                    descripcion: "",
                    direccion: "",
                    telefono: ""
                });
            }
            else{
                this.proveedores = proveedoresEditar;

                if(this.proveedores.length === 0){
                    this.proveedores.push({
                        id: 0,
                        nombre: "",
                        descripcion: "",
                        direccion: "",
                        telefono: ""
                    });
                }
            }           
            
        },
        resetProveedores(){
            if(this.proveedores[0].id === 0){
                this.proveedores = []
            }
        },
        verifyFecha(){
            if(document.getElementById('fecha').value === ""){
                this.fechaError = true;
                this.fechaValid = false;
            }
            else{
                this.fechaError = false;
                this.fechaValid = true;
            }
            
        },
        async verifyCodigo(){
            const self = this;
            this.codigoError = false;
            const data = {
                value: this.codigo,
                origin: piezaEditar.codigo
            };
            await axios.post(urlVerificarCodigo, data)
                                .then(res => {                                    
                                    if (res.data.respuesta == "error") {
                                        self.codigoError = true;
                                    }                              
                                })
                                .catch(error => {
                                    //console.log(error);
                                    // swal.showInputError("Esa unidad ya existe!!!");
                                    self.codigoError = true;
                                });            
            
            return this.codigoError;
        },       
        async save_pieza() {
            const isValid = await this.$refs.observer.validate();
            this.fechaIn = document.getElementById('fecha').value;

            if (!isValid) {
              // ABORT!!
                swal("Error!!", "Existen errores en el formulario.", "error");  
                
                if(this.fechaIn == ""){
                    this.fechaError = true;
                }
            }
            else{
                let verifyCodigoAux = await this.verifyCodigo();
                
                if(this.fechaIn == ""){
                    swal("Error!!", "Existen errores en el formulario.", "error");
                    this.fechaError = true;
                }
                else if(verifyCodigoAux){
                    swal("Error!!", "Existen errores en el formulario.", "error");
                }
                else{
                    // 🐿 ship it
                    this.mostrar_pag_1 = false;
                    // alert(this.fechaIn);
                }
            }
            
            
          },
        getProveedores(){
            axios.get(urlProveedores).then(response=> {
                this.proveedores_api = response.data.proveedores;
            });
        },
        seleccionarProveedor(item){
            var existe = false;

            for(const i in this.proveedores){                
                if(this.proveedores[i].id == item.id){
                    existe = true;
                    break;
                }
            }           

            if(!existe){
                this.resetProveedores();
                this.proveedores.push(item);                
                swal("Correcto!!", "El proveedor se ha añadido correctamente.", "success");
                
            }
            else{
                swal("Error!!", "Este proveedor se ha selecionado anteriormente.", "error");
            }
                            
        },
        async createProveedor(){
            const isValid = await this.$refs.proveedorForm.validate();

            if (!isValid) {
                // ABORT!!
                // swal("Error!!", "Existen errores en el formulario.", "error");                       
                
            }
            else{             
            // 🐿 ship it
                axios.post(urlProveedores, this.proveedor_data).then(res => {
                    // console.log(res.data);
                    if (res.data.respuesta == "ok") {
                        const proveedorAux = {id: res.data.id, nombre: res.data.nombre,
                            descripcion: res.data.descripcion,
                         direccion: res.data.direccion, telefono: res.data.telefono};
                        
                        
                        this.resetProveedores();
                        this.proveedores.push(proveedorAux);
                        this.proveedores_api.push(proveedorAux);

                        this.proveedor_data= {
                            nombre: "",
                            descripcion: "",
                            direccion: "",
                            telefono: ""
                        }
                        this.$refs.proveedorForm.reset();
                        // this.$refs.proveedorForm.invalid
                        
                        swal("Correcto!!", "El proveedor ha sido creado.", "success");
                    }
                    else if (res.data.respuesta == "existe"){
                        swal("Cuidado!!", "Existe un proveedor con esos datos.", "warning");
                    
                    }
                    else {
                        swal("Error!!", "Ha ocurrido un problema al crear el proveedor.", "error");
                    }
                })
                .catch(error => {
                    swal("Error!!", "Ha ocurrido un problema al crear el proveedor.", "error");
                    
                });
                
                $("#PrimaryModal").modal('hide');
                
            }            

        },
        quitarProveedor(index){           
            const self = this;
            swal({
                title: "Advertencia",
                text: "¿Estás seguro de quitar el proveedor?",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Confirmar",
                cancelButtonText: "Cancelar",
                closeOnConfirm: false
            },
            function(){
                // console.log(self.proveedores.length)
                if(self.proveedores.length === 1){
                    self.initProveedores();
                }
                else{
                self.proveedores.splice(index, 1);
                }
                swal("Correcto!!", "El proveedor se ha quitado correctamente.", "success");
            });
            
        },        
        create_data(){
            const self = this;
            const pieza={
                id: piezaEditar.id,
                codigo: this.codigo,
                nombre: this.nombre,
                descripcion: this.descripcion,
                fechaIn: this.fechaIn,
                cantidad: this.cantidad,
                unidad: this.unidad,
                precioIn: this.precioIn,
                precioOut: this.precioOut
            };

            const proveedores_list = this.proveedores;

            if(proveedores_list[0].id == 0){
                swal({
                    title: "Advertencia",
                    text: "No ha añadido ningún proveedor.¿Desea continuar?",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "Continuar",
                    cancelButtonText: "Cancelar",
                    closeOnConfirm: false
                },
                function(){
                    self.send_pieza(pieza, proveedores_list);                    
                });
            }
            else{                
                this.send_pieza(pieza, proveedores_list);
            }
        },
        send_pieza(pieza, proveedores_list){

            if(proveedores_list[0].id === 0){
                proveedores_list = []
            }

            const datos = {
                pieza,
                proveedores_list
            }

            console.log(datos)
            
            axios.post(urlPieza, datos).then(res => {
                if (res.data.respuesta == "ok") {
                    
                    // this.$refs.proveedorForm.invalid
                    // console.log(res.data)
                    swal({
                        title: "Correcto!!",
                        text: "La pieza se ha actualizado correctamente.",
                        type: "success",
                    }, function(value){
                        location.href=redirigirAdmin
                    });
                }
                else {
                    swal("Error!!", "Ha ocurrido un problema al actualizar la pieza."  + error, "error");
                }
            })
            .catch(error => {
                swal("Error!!", "Ha ocurrido un problema al actualizar la pieza.", "error");
                
            });

        },
        ir_admin(){
            location.href=redirigirAdmin
        }

    },

});