$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

function closePopupBox(){
    $('.popupBox').hide();
    return false;
}

function closeCommentBox(){
    $('.commentBox').hide();
    return false;
}
function closeReturnBox(){
    $('#id_reasonList>option:eq(0)').attr('selected', true);
    $('#id_actionList>option:eq(0)').attr('selected', true);
    $('#id_returnedComment').val('');
    $('.returnBox').hide();
    return false;
}
function closeRefundBox(){
    $('#id_refundReferenceNumber').val('');
    $('#id_customerContactedList>option:eq(0)').attr('selected', true);
    $('#id_refundedIsCouponNeeded').attr("checked", "");
    $('#id_newCoupon').val('');
    $('.refundBox').hide();
    return false;
}
function closeColumnBox(){
    $('.columnBox').hide();
    return false;
}

function viewCommentBox(){
    $('.commentBox').show();
    return false;
}
function viewReturnBox(suborderNumber,orderNumber,sku,returnedOrderID,action,reason,comment,isWithInvoice){
    $('#id_returnedSuborder').text(suborderNumber);
    $('#id_returnedOrder').text(orderNumber);
    $('#id_returnedSku').text(sku);
    $('#id_returnedItemID').val(returnedOrderID);
    $('#id_actionList').val(action);
    $('#id_reasonList').val(reason);
    $('#id_returnedComment').val(comment);
    if(isWithInvoice == "True")
        $('#id_isWithInvoice').attr('checked','checked');
    $('.returnBox').show();
    return false;
}
function viewRefundBox(orderNumber,idSalesOrder,sku,returnedOrderID,refundReferenceNumber,customerContactedList,refundedIsCouponNeeded,newCoupon,payment_method,comment){
    $('#id_refundedOrderNumber').text(orderNumber);
    $('#id_refundedIdSalesOrderItem').text(idSalesOrder);
    $('#id_refundedSku').text(sku);
    $('#id_returnedItemID').val(returnedOrderID);
    $('#id_refundReferenceNumber').val(refundReferenceNumber);
    $('#id_customerContactedList').val(customerContactedList);
    $('#id_comment').val(comment);

    if(refundedIsCouponNeeded == "True")
        $('#id_refundedIsCouponNeeded').attr('checked','checked');
    $('#id_newCoupon').val(newCoupon);

    if(payment_method == "CodPayment"){
        $('.refundRefNumberWrapper').hide();
        $('#id_paymentType').html(payment_method);
        $('.paymentTypeWrapper').show();
    }else{
        $('.refundRefNumberWrapper').show();
        $('.paymentTypeWrapper').hide();
    }

    $('.refundBox').show();
    return false;
}
function viewInvoiceBox(invoiceID,transactionCode,supplierName,transactionID,invoiceNumber,invoiceAmount,quantityInvoice,returnInvoice){
    $('#id_invoiceID').val(invoiceID);

    $('#id_transactionCode').text(transactionCode);
    $('#id_transactionSupplierName').text(supplierName);
    $('#id_transactionID').val(transactionID);

    $('#id_transactionInvoiceNumber').val(invoiceNumber);
    $('#id_transactionInvoiceAmount').val(invoiceAmount);
    $('#id_transactionInvoiceQuantity').val(quantityInvoice);
    $('#id_transactionReturnInvoiceNumber').val(returnInvoice);

    $('.invoiceBox').show();
    return false;
}

function closeInvoiceBox(){
    $('#id_invoiceID').val('');

    $('#id_transactionCode').val('');
    $('#id_transactionSupplierName').val('');


    $('#id_transactionInvoiceNumber').val('');
    $('#id_transactionInvoiceAmount').val('');
    $('#id_transactionInvoiceQuantity').val('');
    $('#id_transactionReturnInvoiceNumber').val('');

    $('.invoiceBox').hide();
    return false;
}


function viewColumnBox(){
    $('.columnBox').show();
    return false;
}
function submitComment(){
                 //$('#comment').val($('#userComment').val());
                $('#id_buttonSource').val("comment");
                $('#orderUpdateForm').submit();
}
function submitReturnForm(){
    if( $('#id_actionList').val() == "" || $('#id_actionList').val() == "0")
    {
        $('#id_actionList').css("border-color","red");
    }
    else if($('#id_reasonList').val() == "" || $('#id_reasonList').val() == "0"){
        $('#id_reasonList').css("border-color","red");
    }
    else
    {
        $('#returnedOrderForm').submit();
        closeReturnBox();
    }

}
function submitRefundedForm(){
    $('#refundedOrderForm').submit();
    closeRefundBox();
}
function submitInvoiceForm(){
    $('#id_invoiceForm').submit();
    closeInvoiceBox();
}
function fnShowHide( iCol, status )
{
	/* Get the DataTables object again - this is not a recreation, just a get of the object */
	var oTable = $('#orderList').dataTable();

	var bVis = oTable.fnSettings().aoColumns[iCol].bVisible;
	oTable.fnSetColumnVis( iCol, status );
}

function submitColumn(){
     closeColumnBox();
     $('input:checkbox[name=columnChecked]').each(function() {
       fnShowHide($(this).val(),$(this).attr("checked"));
     });

}

function viewOrderHistory(pk){
        url1 = "/cross_order/order_history/?pk="+pk;
        jQuery.ajax(
			{
				'type': 'GET',
                async:false,
        		'url': url1,
        		'data': '',
        		'success' : function(data){
                    kList = data.split(',');

                    con="<thead><tr><th>Date</th><th>User</th><th>Action</th></tr></thead><tbody>";
                    for(i=0; i < kList.length ;i+=3){
                        con+="<tr><td>"+kList[i+1]+"</td><td>"+kList[i]+"</td><td>"+kList[i+2]+"</td></tr>";
                    }
                    con +="</tbody>";

                    $('#history').html(con);
                     $('#history').dataTable({
                        "bJQueryUI": true,
                        "bDestroy":true
                    });
/*
                    var mv = JSON.parse(data);

                    $('#history').dataTable( {
		                "aaData": "",
                        "aoColumns":[
                            { "sTitle": "Order" },
                            { "sTitle": "User" },
                            { "sTitle": "Date" },
                            { "sTitle": "Changed To"}
                        ],
                        "bJQueryUI": true,
                        "bDestroy":true
                    });
*/
                    $('.popupBox').show();
			    }
            });
}

function displayModuleMenus(menuClass,menuItem){
    $('.dynamicMenuItem').hide();
    $('.dynamicMenuItem').removeClass("activeItem");
    $('.'+menuClass).show();

    if(menuItem.length > 0)
        $('#'+menuItem).addClass("activeItem");
}

function redirectTo(url){
    window.location = url;
}

function setMenuName(moduleName){
    $('#moduleName').html(" - "+moduleName);
}
