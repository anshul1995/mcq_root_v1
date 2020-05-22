$(function () {

    $("#G3-answer, #G3-create").on("click", function (e) {
        e.preventDefault();
        $(".G3-choice").hide();
        console.log("submitting G3 choice!!!!!");  // sanity check
        var btn = $('#' + this.id).attr('value');
        console.log(btn);
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            type: "POST",
            url: window.location.pathname+"G3-choice/",
            data: { choice: btn },
            success: function (result) {
                $('#questions-list').append(result.append_question_list);
                $('#questions-list').append(result.create_mcq_form);
                $('.tooltipped').tooltip();
                $('select').formSelect();
                $('#submit-quiz').append(result.submit);
                $(".G3-choice").remove()
            },
            error: function (result) {
                alert('error');
                $(".G3-choice").show()
            }
        });
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            type: "POST",
            url: window.location.pathname + "quiz-log/",
            data: {
                type: 'group 3 choice',
                action: btn,
                element_id: btn
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

});