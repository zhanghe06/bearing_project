$(function () {
    var collapse_search_obj = $('.panel-collapse')

    collapse_search_obj.on('shown.bs.collapse', function () {
        $(this).parent().find('.panel_resize_btn').removeClass('glyphicon-chevron-down')
        $(this).parent().find('.panel_resize_btn').addClass('glyphicon-chevron-up')
    })

    collapse_search_obj.on('hidden.bs.collapse', function () {
        $(this).parent().find('.panel_resize_btn').removeClass('glyphicon-chevron-up')
        $(this).parent().find('.panel_resize_btn').addClass('glyphicon-chevron-down')
    })
})