$('#comment-button').click(function(){

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


    $.ajax({
        url: $('#comment-button').data('data-url'),
        method: 'POST',
        data: {
            'body': $('#body').val(),
        },
        success: function(data){
            if(data.status == 'ok'){
                $('#comment-form').hide(2000);
                $('#comment-form').html(data.data);
                $('#h-comment').html('باتشکر. نظر شما به دست ما رسید.');
                $('#comment-form').show(2000);
            }
            else{
            $('#comment-form').html(data.data);
            };
        }
    });

});
