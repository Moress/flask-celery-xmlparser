$(function () {
    $('.js-row-active').each(function (i, elem) {
        var row_item = $(elem)
        var task_id = row_item.data('id');
        updateTask(task_id, row_item);
    });

    function updateTask(task_id, row_item) {
        var url = '/task_status/' + task_id;
        $.getJSON(url, function (result) {
                row_item.find('.js-row-state').html(result.STATE)
                row_item.find('.js-row-count').html(result.COUNT)
                row_item.find('.js-row-weight').html(result.WEIGHT)

                if (result.STATE != 'SUCCESS' && result.STATE != 'FAILURE') {
                    setTimeout(function () {
                        updateTask(task_id, row_item)
                    }, 1000);
                }
                else
                {
                    row_item.removeClass('js-row-active');
                }
            })
    }
})
