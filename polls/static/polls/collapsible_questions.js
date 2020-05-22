$(function () {
    $('.tooltipped').tooltip();
    $('select').formSelect();
    $('.collapsible').collapsible({
        onOpenEnd: function (e) {
            // console.log('open '+$(e).children('div.collapsible-header').attr('value'));
            $.ajax({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                type: "POST",
                url: window.location.pathname + "quiz-log/",
                data: {
                    type: 'question',
                    action: 'open',
                    element_id: $(e).children('div.collapsible-header').attr('value')
                }
            });
        },
        onCloseStart: function (e) {
            // console.log('close '+$(e).children('div.collapsible-header').attr('value'));
            $.ajax({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                type: "POST",
                url: window.location.pathname + "quiz-log/",
                data: {
                    type: 'question',
                    action: 'close',
                    element_id: $(e).children('div.collapsible-header').attr('value')
                }
            });
        }
    });

    $('#questions-list').on('click', 'input.log-mcq', function (e) {
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            type: "POST",
            url: window.location.pathname + "quiz-log/",
            data: {
                type: 'choice',
                action: 'select',
                element_id: $(this).attr('value')
            }
        });
    })

    $('#questions-list').on('focus', 'textarea.log-text', function (e) {
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            type: "POST",
            url: window.location.pathname + "quiz-log/",
            data: {
                type: 'create mcq text',
                action: 'focus',
                element_id: $(this).attr('name')
            }
        });
    })

    $('#questions-list').on('blur', 'textarea.log-text', function (e) {
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            type: "POST",
            url: window.location.pathname + "quiz-log/",
            data: {
                type: 'create mcq text',
                action: 'blue',
                element_id: $(this).attr('name')
            }
        });
    })



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