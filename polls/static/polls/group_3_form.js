$(function () {

    $("#G3-answer, #G3-create").on("click", function (e) {
        e.preventDefault();
        $(".G3-choice").hide()
        console.log("submitting G3 choice!")  // sanity check
        $.ajax({
            type: "POST",
            url: window.location.pathname+"G3-choice/",
            data: { choice: $('#' + this.id).attr('value') },
            success: function (result) {
                $('#questions-list').append(result.append_question_list);
                $('#create-quiz-form').append(result.create_mcq_form);
                $('#submit-quiz').append(result.submit);
                $(".G3-choice").remove()
            },
            error: function (result) {
                alert('error');
                $(".G3-choice").show()
            }
        });
    });

    // This function gets cookie with a given name
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

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});