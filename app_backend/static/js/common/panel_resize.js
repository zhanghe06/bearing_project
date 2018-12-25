$(function () {
    var collapse_search_obj = $('.panel-collapse')

    collapse_search_obj.on('shown.bs.collapse', function () {
        $(this).parent().find('.panel_resize_btn').removeClass('glyphicon-resize-full')
        $(this).parent().find('.panel_resize_btn').addClass('glyphicon-resize-small')
    })

    collapse_search_obj.on('hidden.bs.collapse', function () {
        $(this).parent().find('.panel_resize_btn').removeClass('glyphicon-resize-small')
        $(this).parent().find('.panel_resize_btn').addClass('glyphicon-resize-full')
    })
})