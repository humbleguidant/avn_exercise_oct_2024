/** Function for executing AJAX calls to the server to perform POST actions
 * based off of action parameter.
 * Used for adding and removing cards from shopping cart or entire application */
function perform_action(action)
{
    $.ajax({
        type: 'POST',
        url: action,
        contentType: false,
        cache: false,
        processData: true,
        success: function (data) {
            if (data)
                //if (data.delete_success === true && data.upload_success === true)
                location.reload();
            else
                alert('An error occurred. Please contact IT services.');
        },
    });
}

/** AJAX call to upload card */
$(document).ready(function () {
    $('#upload-card-btn').click(function () {
        /** Get user input from upload form and send to server */
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
    /** AJAX call to add item to cart */
    $('.add-to-cart-button').click(function () {
        perform_action('/add_to_cart/' + $(this).data('email') + '/' + $(this).data('id'));
    });

    /** AJAX call to remove item from cart */
    $('.remove-from-cart-button').click(function () {
        perform_action('/remove_item_from_cart/' + $(this).data('email') + '/' + $(this).data('id'));
    });

    /** AJAX call to remove card from system */
    $('.delete-card-from-shop-button').click(function () {
        perform_action('/remove_card_from_shop/' + $(this).data('email') + '/' + $(this).data('id') + '/' +
            $(this).data('name').valueOf().replace('images/', ''))
    });
});