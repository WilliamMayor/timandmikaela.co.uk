MIM.home = {
    init: function() {
        MIM.home.countdown();
        window.setInterval(MIM.home.countdown, 1000);
    },
    countdown: function() {
        var tick = Date.now();
        var tock = new Date(2015, 7, 1, 14, 1, 0);
        var delta = tock - tick; // milliseconds
        var days = Math.floor(delta / (1000*60*60*24));
        var hours = Math.floor(delta / (1000*60*60)) - days*24;
        var minutes = Math.floor(delta / (1000*60)) - days*24*60 - hours*60;
        $(".countdown .days span.number").text(days);
        $(".countdown .hours span.number").text(hours);
        $(".countdown .minutes span.number").text(minutes);
        $(".countdown .days span.plural").text((days === 1) ? '' : 's');
        $(".countdown .hours span.plural").text((hours === 1) ? '' : 's');
        $(".countdown .minutes span.plural").text((minutes === 1) ? '' : 's');
    }
};
