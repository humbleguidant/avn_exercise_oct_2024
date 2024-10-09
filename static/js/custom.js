function perform_action(action, email, card_id)
{
    $.ajax({
        type: 'POST',
        url: action + email + '/' + card_id,
        contentType: false,
        cache: false,
        processData: true,
        success: function (data) {
            if (data)
                location.reload();
            else
                alert('An error occurred. Please contact IT services.');
        },
    });
}

$(document).ready(function () {
    $('#upload-card-btn').click(function () {
        var form_data = new FormData();
        form_data.append('file', $('#upload-card-form')[0]);
        form_data.append('price', $('#price-input').valueOf())
        form_data.append('description', $('#description-input').valueOf())
        $.ajax({
            type: 'POST',
            url: '/upload',
            data: form_data,
            contentType: false,
            cache: false,
            processData: true,
            success: function (data) {
                console.log('Success!');
            },
        });
    });
    $('.add-to-cart-button').click(function () {
        perform_action('/add_to_cart/',  $(this).data('email'), $(this).data('id'));
    });

    $('.remove-from-cart-button').click(function () {
        perform_action('/remove_item_from_cart/', $(this).data('email'), $(this).data('id'));
    });

    $('.delete-card-from-shop-btn').click(function () {
        perform_action('/remove_card_from_shop/', $(this).data('email'), $(this).data('id'))
    });
});