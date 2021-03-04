$(function () {
    var collapse_search_obj = $('.panel-collapse')
    var panel_resize_btn_obj = $('.panel_resize_btn')

    collapse_search_obj.on('shown.bs.collapse', function () {
        panel_resize_btn_obj.removeClass('glyphicon-chevron-down')
        panel_resize_btn_obj.addClass('glyphicon-chevron-up')
    })

    collapse_search_obj.on('hidden.bs.collapse', function () {
        panel_resize_btn_obj.removeClass('glyphicon-chevron-up')
        panel_resize_btn_obj.addClass('glyphicon-chevron-down')
    })
})