MIM.rsvp = {
    init: function() {
        $(".response input:radio").on("change", MIM.rsvp.show_starter);
        $(".time input:radio").on("change", MIM.rsvp.show_starter);
        MIM.rsvp.show_starter();
    }, show_starter: function() {
        var response = $(".response input:radio:checked").val();
        var time = $(".time input:radio:checked").val();
        console.log(response, time);
        if (time === 'day' && response === 'accept') {
            $('.starter span').show();
        } else {
            $('.starter span').hide();
        }
    }
};
