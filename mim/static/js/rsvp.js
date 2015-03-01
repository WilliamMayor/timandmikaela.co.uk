MIM.rsvp = {
    init: function() {
        $(".response input:radio").on("change", function() {
            var response = $(this).val();
            console.log(response);
            if (response === 'accept') {
                $('.starter span').show();
            } else {
                $('.starter span').hide();
            }
        });
    }
};
