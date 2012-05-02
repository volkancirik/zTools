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

                    con="<thead><tr><th>User</th><th>Date</th><th>Action</th></tr></thead><tbody>";
                    for(i=0; i < kList.length ;i+=3){
                        con+="<tr><td>"+kList[i]+"</td><td>"+kList[i+1]+"</td><td>"+kList[i+2]+"</td></tr>";
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
