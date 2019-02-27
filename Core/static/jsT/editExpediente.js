var path = "http://127.0.0.1:8000";


$.ajax({
    method: "GET",
    url: path + "/api/Document_identity/",
    success: function (items) {
        $.each(items, function (i, item) {
            $('#id_doc').append($('<option>', {
                value: item.id,
                text: item.doc_des
            }));
        });
    }

});

$.ajax({
    method: "GET",
    url: path + "/api/Type_document/",
    success: function (items) {
        $.each(items, function (i, item) {
            $('#id_type_document').append($('<option>', {
                value: item.id,
                text: item.doc_des
            }));
        });
    }

});

function get_data_document(id_document) {
    //console.log(id_document);


    $.ajax({
        method: "GET",
        url: path + "/api/Document/" + id_document + ".json",
        success: function (items) {
            console.log(items);
            if (items.doc_status == 0) {
                $('#id_document').val(id_document);
                var $select = $('#id_type_document');
                $select.val(items.id_type_document);
                $('#doc_number').val(items.doc_number);
                $('#doc_pages').val(items.doc_pages);
                $('#id_tupa').val(items.id_tupa)
                $('#doc_type').val(3);
                $('#id_person').val(items.id_person);
                get_person_id(items.id_person);
                get_tupa_id(items.id_tupa);
                update_destino(items.id_tupa);
                $('#id_file_expediente').next('.custom-file-label').html(id_document+".pdf");



            }
            else {
                alert("El documento nose puede Editar, por que ya fue recepcionado ");
                $('#exampleModal').modal('hide');

                window.location.reload();
            }


        }

    });
}

function get_tupa_id(id){

      $.ajax({
        method: "GET",
        url: path + "/api/Tupa/" + id+ ".json",
        success: function (items) {
            $('#id_tupa_description').val(items.tup_des);
            $('#doc_tupa').val(items.tup_des);
        }

    });

}
function get_person_id(id) {

    $.ajax({
        method: "GET",
        url: path + "/api/Person/" + id+ ".json",
        success: function (items) {

            $('#per_dni').val(items.per_doc);
            $('#id_nombre').val(items.per_name+" "+items.per_lastname);
            $('#id_person').val(items.id);
        }

    });
}

function update_input_name(id) {

    var dni_aux = $('#per_dni').val();
    $.ajax({
        method: "GET",
        url: path + "/get_person_dni/" + dni_aux + "/",
        success: function (items) {
            $('#id_nombre').val(items.datos.nombres);
            $('#id_person').val(items.datos.id);
        }

    });

}

$("#per_dni").autocomplete({

    source: function (request, response) {
        var dni_aux = $('#per_dni').val();

        $.ajax({
            url: path + "/get_dni_autocomplete/" + dni_aux + "/",
            type: "GET",
            data: request,
            success: function (data) {

                response($.map(data.datos, function (na) {
                    return {
                        label: na.per_doc,
                        value: na.per_doc
                    };
                }))
            }
        })
    },

    minLength: 1,

    select: function (event, ui) {
        // Prevent value from being put in the input:
        this.value = ui.item.label;
        // Set the next input's value to the "value" of the item.
        console.log(ui.item.label);
        update_input_name(ui.item.label);
        $(this).next("input").val(ui.item.value);

        event.preventDefault();
    }

}).autocomplete("option", "appendTo", "#form_registro_expediente");


var aux_t;
var offices;

function update_destino(id_destino) {


    $.ajax({
        url: path + "/api/Tupa/" + id_destino + "/",
        type: "GET",
        success: function (data) {
            offices = data.id_ofi_end;
            update_destino_office(offices);
        }
    });

}

function update_destino_office(offices) {

    $.ajax({
        url: path + "/api/Office/" + offices + "/",
        type: "GET",
        success: function (data) {

            $('#id_nombre_destino').val(data.ofi_des);
        }
    });
}


$("#id_tupa_description").autocomplete({

    source: function (request, response) {
        var tupa = $('#id_tupa_description').val();
        $.ajax({
            url: path + "/get_tupa_autocomplete/" + tupa + "/",
            type: "GET",
            data: request,
            success: function (data) {
                aux_t = data.datos;
                //console.log(data.datos);
                response($.map(data.datos, function (na) {
                    return {

                        label: na.tup_des,
                        value: na.id


                    };
                }))
            }
        })
    },

    minLength: 1,

    select: function (event, ui) {


        this.value = ui.item.label;
        console.log(ui);
        // Set the next input's value to the "value" of the item.
        //update_destino(ui.item.value);
        update_input_name(ui.item.label);
        $(this).next("input").val(ui.item.value);
        $('#id_tupa').val(ui.item.value);
        $('#id_tupa_description').val(ui.item.label);
        $('#doc_tupa').val(ui.item.label);
        console.log(ui.item.value);
        update_destino(ui.item.value);

        event.preventDefault();
    }
}).autocomplete("option", "appendTo", "#form_registro_expediente");
var id_document;

function last_insert_document() {

    $.ajax({
        url: path + "/get_last_document/",
        type: "GET",
        success: function (data) {

            id_document = data.datos.id;
            registrar_attachment_movements(id_document);

        },
        error: function () {
            alert("error en el registro ");

        }
    });
    return id_document;
}

function registrar_attachment_movements(id_document) {


    var form = $('#form_registro_expediente')[0];
    var fd = new FormData(form);
    var file_data = $('input[type="file"]')[0].files[0];
    var csrf = $('#form_registro_expediente input[name=csrfmiddlewaretoken]').val();

    fd.append("file", file_data);
    fd.append("path", id_document);
    fd.append("csrfmiddlewaretoken", csrf);


    $.ajax({
        type: 'POST',
        url: path + '/register_attachment/',
        data: fd,
        cache: false,
        contentType: false,
        processData: false,
        success: function (data) {
            console.log("Success");
            $("#btn_registrar_expediente").prop("disabled", false);
            alert("se Regitro con exito");

            window.open(path + "/imprimirHojaTramite/");
            window.location.reload();


        },
        error: function (data) {
            console.log("ERRORRR");
        }
    });

    $.ajax({
        url: path + "/get_last_document_movement/",
        type: "GET",
        success: function (data) {

        },
        error: function () {
            alert("error en el registro ");
        }
    });

}

$('#btn_registrar_expediente').click(function () {
    $("#btn_registrar_expediente").prop("disabled", true);
    var csrf = $('#form_registro_expediente input[name=csrfmiddlewaretoken]').val();
    var id_type_document = $('#id_type_document').val();
    var id_person = $('#id_person').val();
    var id_tupa = $('#id_tupa').val();
    var doc_number = $('#doc_number').val();
    var doc_des = $('#id_nombre_destino').val();
    var doc_pages = $('#doc_pages').val();
    var doc_type = $('#doc_type').val();

    var datos;
    datos = {

        csrfmiddlewaretoken: csrf,
        id_type_document: id_type_document,
        id_person: id_person,
        id_tupa: id_tupa,
        doc_number: doc_number,
        doc_des: doc_des,
        doc_pages: doc_pages,
        doc_type: doc_type,
        doc_status: 0

    };


    var id_doc=$('#id_document').val();
    $.ajax({
        url: path + "/api/Document/"+id_doc+"/",
        type: "PATCH",
        data: datos,
        success: function (data) {

            var namePdf=$('.custom-file-label').html();
            console.log(namePdf)
            if(namePdf==id_doc+".pdf"){
                alert("Actualizado con éxito!!");
                window.location.reload();
            }
            else{
                last_insert_document();
            }


        },
        error: function () {
            alert("error en el registro ");
        }
    });

});

$('#id_file_expediente').on('change', function () {
    //get the file name
    var fileName = $(this).val();
    //replace the "Choose a file" label
    $(this).next('.custom-file-label').html(fileName);
});


