var path = "http://127.0.0.1:8000";

var id_type_document;
var id_person;
var id_tupa;
var doc_number;
var doc_exp_number;
var doc_des;
var doc_pages;
var doc_type;





function get_id_document(id) {

    $.ajax({
        url: path + "/api/Document/" + id + ".json",
        type: "GET",
        success: function (data) {

            id_type_document = data.id_type_document;
            id_person = data.id_person;
            id_tupa = data.id_tupa;
            doc_number = data.doc_number;
            doc_exp_number = data.doc_exp_number;
            doc_des = data.doc_des;
            doc_pages = data.doc_pages;
            doc_type = data.doc_type;

            $('#id_folios_hoja_tramite').html(doc_pages);
            $('#id_documento_exp_number').html(doc_number);

            $('.id_folios_hoja_tramite').html(doc_pages);
            //$('table .id_folios_hoja_tramite').html(doc_pages);
            //$('#id_folios_hoja_tramite').html(doc_pages);
            set_type_document(id_type_document);
            set_id_person(id_person);
            set_id_tupa(id_tupa);
            //$("#id_hoja_tramite").show();
            $('#id_hoja_tramite').printThis();




        },
        error: function () {
            alert("error en el registro ");
        }
    });
}

function set_type_document(id_type_document){
      $.ajax({
        url: path + "/api/Type_document/"+id_type_document+".json",
        type: "GET",
        success: function (data) {

            $('.id_documento_hoja_tramite').html(data.doc_des);
            $('#id_documento_hoja_tramite').html(data.doc_des);
        },
        error: function () {
            alert("error en el registro ");
        }
    });
}
function set_id_person(id_person){
      $.ajax({
        url: path + "/api/Person/"+id_person+".json",
        type: "GET",
        success: function (data) {

            $('.id_administrado_hoja_tramite').html(data.per_name+" "+data.per_lastname);
            $('#id_administrado_hoja_tramite').html(data.per_name+" "+data.per_lastname);


        },
        error: function () {
            alert("error en el registro ");
        }
    });
}
function set_id_tupa(id_tupa){
      $.ajax({
        url: path + "/api/Tupa/"+id_tupa+".json",
        type: "GET",
        success: function (data) {

        $('.id_doc_des_hoja_tramite').html(data.tup_des);
        $('#id_doc_des_hoja_tramite').html(data.tup_des);
        },
        error: function () {
            alert("error en el registro ");
        }
    });
}