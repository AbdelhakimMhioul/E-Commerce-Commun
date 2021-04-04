{/* <script>
    $(document).on('submit', '#addWishlist', function (e) {
        e.preventDefault();
        $.ajax({
        type: 'POST',
            url: "{% url 'addWishlist' product.id %}",
            data:
            {
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function () {
        alert('Message Sent Successfully');
            }
        })
    }); $(document).on('submit', '#addCart', function (e) {
        e.preventDefault();
        $.ajax({
        type: 'POST',
            url: "{% url 'addCart' product.id %}",
            data:
            {
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function () {
        alert('Message Sent Successfully');
            }
        })
    });
</script> */}