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


$.ajax({
    method: "GET",
    url: path + "/get_departamentos/",
    success: function (items) {
        $.each(items.datos, function (i, item) {
            $('#id_departamento').append($('<option>', {
                value: item.id,
                text: item.departamento
            }));
        });
    }

});

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
});


$("#registro_persona").on("submit", function (event) {
    event.preventDefault();

    var data = $(this).serialize();
    console.log(data);
    $.ajax({
        method: "POST",
        url: path + "/api/Person/",
        data: data,
        dataType: "json",
        success: function (request) {
            $.ajax({
                method: "GET",
                url: path + "/get_last_person/",
                success: function (items) {
                    $('#person_id').val(items.datos.id);
                    $('#per_dni').val(items.datos.dni);
                    $('#id_nombre').val(items.datos.nombres);
                }

            });
            $('#exampleModal').modal('toggle');

        },
        error: function (request) {
            console.log(request);
        }

    });

});

$('#id_departamento').change(function () {

    var id_dep = $('#id_departamento option:selected').val();
    $.ajax({
        method: "GET",
        url: path + "/get_provincias/" + id_dep + "/",
        success: function (items) {

            if (items.datos.length != 0) {
                //$('#id_provincia').remove().end();
                $('#id_provincia').find('option')
                    .remove()
                    .end()
                    .append('<option value="whatever">Seleccionar</option>')
                    .val('whatever');

                $.each(items.datos, function (i, item) {
                    $('#id_provincia').append($('<option>', {
                        value: item.id,
                        text: item.provincia
                    }));
                });
            }
            else {
                $('#id_provincia').find('option')
                    .remove()
                    .end()
                    .append('<option value="whatever">Seleccionar</option>')
                    .val('whatever');
                $('#id_distrito').find('option')
                    .remove()
                    .end()
                    .append('<option value="whatever">Seleccionar</option>')
                    .val('whatever');
            }
        }
    });
});


$('#id_provincia').change(function () {

    var id_prov = $('#id_provincia option:selected').val();
    $.ajax({
        method: "GET",
        url: path + "/get_distritos/" + id_prov + "/",
        success: function (items) {

            if (items.datos.length != 0) {
                //$('#id_provincia').remove().end();
                $('#id_distrito').find('option')
                    .remove()
                    .end()
                    .append('<option value="whatever">Seleccionar</option>')
                    .val('whatever');


                $.each(items.datos, function (i, item) {
                    $('#id_distrito').append($('<option>', {
                        value: item.id,
                        text: item.distrito
                    }));
                });
            }
            else {
                $('#id_distrito').find('option')
                    .remove()
                    .end()
                    .append('<option value="whatever">Seleccionar</option>')
                    .val('whatever');
            }
        }
    });
});

var aux_t;

function update_destino(id_destino) {

    $.ajax({
        url: path + "/api/Office/" + id_destino + "/",
        type: "GET",
        success: function (data) {

            $('#id_nombre_destino').val(data.ofi_des);
        }
    });
    //console.log(aux_id_office);

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
        // Set the next input's value to the "value" of the item.
        //update_destino(ui.item.value);
        update_input_name(ui.item.label);
        $(this).next("input").val(ui.item.value);
        $('#id_tupa').val(ui.item.value);
        $('#id_tupa_description').val(ui.item.label);
        $('#doc_tupa').val(ui.item.label);
        update_destino(aux_t[0].id_ofi_end);

        event.preventDefault();
    }
});
var id_document;

function last_insert_document() {

    $.ajax({
        url: path + "/get_last_document/",
        type: "GET",
        success: function (data) {
            //console.log(data);
            //console.log(data.datos)
            id_document = data.datos.id;
            registrar_attachment_movements(id_document);
            //console.log(id_document);
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
        doc_type: doc_type

    };


    $.ajax({
        url: path + "/api/Document/",
        type: "POST",
        data: datos,
        success: function (data) {
            //id_document=last_insert_document();
            last_insert_document();
            //registrar_attachment_movements(id_document);
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
})