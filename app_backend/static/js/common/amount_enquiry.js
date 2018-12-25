// 汇总金额
function compute_total_amount () {
    var sum = 0
    $('tr.text-muted').each(function (i, tr) {
        var j = 1
        $(tr).find('input.quantity,input.unit_price').each(function () {
            j *= Number(this.value)
        })
        sum += j
    })

    $('input#amount_enquiry').val(sum.toFixed(2).replace(/\d(?=(\d{12})+\.)/g, '$&,'))
}

// 更新数据重新汇总金额
$('input[type=number]').on('input', function () {
    compute_total_amount()
})