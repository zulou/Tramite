var path = "http://127.0.0.1:8000";

var dataset = [];

{%
    if documentos %}
{%
    for document in documentos %}
//dataset.push({id:"{{vou.id}}",voucher:"{{vou.vouch.id}}",dni:"{{vou.vouch.consession.clients.dni}}",name:"{{vou.vouch.consession.clients.firstname}} {{vou.vouch.consession.clients.lastname}}",market:"{{vou.vouch.consession.points.sections.markets.name}}",section:"{{vou.vouch.consession.points.sections.name}}",point:"{{vou.vouch.consession.points.point_code}}",date:"{{vou.vouch.date_pay}}",price_point:"{{vou.price_point}}"});
dataset.push({
    id: "{{document.id}}",
    doc_number: "{{document.doc_number}}",
    doc_exp_number: "{{document.doc_exp_number}}",
    id_type_document: "{{document.id_type_document.doc_des}}",
    doc_pages: "{{document.doc_pages}}",
    id_tupa: "{{document.id_tupa.tup_des}}",
    id_person: "{{document.id_person.per_name}}",
    doc_des: "{{document.id_tupa.id_ofi_end.ofi_des}}",
    id_type_origin: "{{document.doc_des.doc_type}}"
});
//console.log("{{vou}}");

{%
    endfor %
}

{% else %
}

{%
    endif %
}


$(document).ready(function () {


    var table = $('#list-persona').DataTable({

        "language": {
            "sProcessing": "Procesando...",
            "sLengthMenu": "Mostrar _MENU_ registros",
            "sZeroRecords": "No se encontraron resultados",
            "sEmptyTable": "Ningún dato disponible en esta tabla",
            "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
            "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
            "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
            "sInfoPostFix": "",
            "sSearch": "Buscar:",
            "sUrl": "",
            "sInfoThousands": ",",
            "sLoadingRecords": "Cargando...",
            "oPaginate": {
                "sFirst": "Primero",
                "sLast": "Último",
                "sNext": "Siguiente",
                "sPrevious": "Anterior"
            },
            "oAria": {
                "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                "sSortDescending": ": Activar para ordenar la columna de manera descendente"
            }
        },
    {
        #dom
    :
        "Bfrtip", #
    }
    "data"
:
    dataset,
        "aoColumns"
:
    [
        {"data": "id"},
        {"data": "doc_exp_number"},
        {"data": "doc_number"},
        {"data": "id_type_document"},
        {"data": "doc_pages"},
        {"data": "id_tupa"},
        {"data": "id_person"},
        {"data": "doc_des"},
        {"data": "id_type_origin"},


        {
            "targets": -1,
            "data": null,
            "defaultContent": '<button class="btn btn-outline-warning btn-sm"><i class="fa fa-edit"></i> Editar</button>'
        },
        {
            "targets": -1,
            "data": null,
            "defaultContent": '<button class="btn btn-outline-primary btn-sm"><i class="fa fa-eye"></i> Ver</button>'
        }
    ],
        "order"
:
    [[0, "desc"]],
        "pageLength"
:
    10,
        {
    #"lengthMenu"
:
    false, #
}
    "bLengthChange"
:
    false,

        {
    #select
:
    true, #
}
} )
    ;

    $('.dataTables_filter label').addClass('col-sm-12 control-label');
    $('.dataTables_filter input').addClass('form-control');
    {
        #$('.dataTables_length label').addClass('col-sm-12 control-label');
        #
    }
    {
        #$('.dataTables_length select').addClass('form-control');
        #
    }

    $('#list-persona tbody').on('click', 'button.btn-outline-warning', function () {
        var data = table.row($(this).parents('tr')).data();

        console.log(data);
        $("#id_pay").val(data.id);
        $("#voucher").val(data.voucher);
        $("#dni_pay").val(data.dni);
        $("#full_name").val(data.name);
        $("#concession").val(data.market + "  /  " + data.section + " / " + data.point);
        $("#price").val(data.price_point);
        $('#edit_vouchers').modal('show');


    });

    $('#list-persona tbody').on('click', 'button.btn-outline-primary', function () {
        var data = table.row($(this).parents('tr')).data();
        console.log(data.id);
    });

    $('#button-pay').click(function (e) {
        e.preventDefault();
        var id = parseInt($("#id_pay").val());
        var voucher = parseInt($("#voucher").val());
        var csrf_pay = $('#pay_concession input[name=csrfmiddlewaretoken]').val();
        var price_point = parseInt($("#price").val());
        console.log(csrf_pay);
        var datos;
        datos = {
            csrfmiddlewaretoken: csrf_pay,
            id: id,
            vouch: voucher,
            price_point: price_point,
            price_water: 0,
            price_energy: 0

        };
        $.ajax({
            url: path + "/api/VoucherDetail/" + voucher + "/",
            type: "PUT",
            dataType: "json",
            data: datos,
            success: function (data) {

                alert("éxito!!1");
            }
        });
    });


});