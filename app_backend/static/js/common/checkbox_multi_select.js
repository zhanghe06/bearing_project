// 全选点击事件
$('.select_all').on('click', function () {
    var select_all_checked = $(this).prop('checked')
    $('.select_item').each(function () {
        if (select_all_checked) {
            $(this).prop('checked', true)
            $(this).parents('tr').addClass('bg-success')

        }else{
            $(this).prop('checked', false)
            $(this).parents('tr').removeClass('bg-success')
        }
    })
})

// 反选点击事件
$('.select_invert').on('click', function () {
    $('.select_item').trigger('change')
})

// 单行点击事件
$('tr.item').on('click', function () {
    $(this).find(':checkbox').trigger('change')
})

// 选框变化事件
$('.select_item').on('change', function () {
    if ($(this).prop('checked')) {
        $(this).prop('checked', false)
        $(this).parents('tr').removeClass('bg-success')
        $('.select_all').prop('checked', false)  // 取消全选
    } else {
        $(this).prop('checked', true)
        $(this).parents('tr').addClass('bg-success')
    }
})