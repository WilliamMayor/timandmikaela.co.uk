MIM.slides = {
    init: function() {
        $("#slides").slidesjs({
            width: 600,
            height: 340,
            navigation: false,
            callback: {
                loaded: function() {
                    $(".slidesjs-pagination-item a").html("<i class='fa fa-fw'></i>");
                }
            }
        });
    }
};
