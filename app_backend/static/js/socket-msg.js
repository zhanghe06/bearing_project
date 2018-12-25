$(function () {

    //下拉框查询组件点击查询栏时不关闭下拉框
    var body_obj = $('body')
    body_obj.on('click', '[data-stopPropagation]', function (e) {
        e.stopPropagation()
    })

    // 初始化消息数量
    $('#total-msg-count').html($('#socket-messages').find('.message').length)

    var socket = io.connect('https://' + document.domain + ':' + location.port + '/msg')
    socket.on('s_res', function (msg) {
        //console.log(msg)
        var msg_menu_obj = $('.messages-menu')
        if (!msg_menu_obj.hasClass('open')) {
            msg_menu_obj.toggleClass('open')
        }
        var socket_msg_obj = $('#socket-messages')
        //socket_msg_obj.prepend(tmpl("template-message", msg))
        socket_msg_obj.prepend(msg)
        flask_moment_render_all()
        $('#total-msg-count').html(socket_msg_obj.find('.message').length)
    })

    body_obj.on('click', '.message-close', function () {
        $(this).parent().parent().fadeTo('slow', 0.01, function () {//fade
            $(this).slideUp('slow', function () {//slide up
                $(this).remove()//then remove from the DOM
                $('#total-msg-count').html($('#socket-messages').find('.message').length)
            })
        })
    })

    body_obj.on('click', '.message-close-all', function () {
        $('.message-close').each(function () {
            $(this).click()
        })
    })
})
