var MIM = {};

$(document).ready(function() {
    var body = $("body");
    function run(o) {
        if (!o) {
            return;
        }
        for (var k in o) {
            if (body.hasClass(k)) {
                o[k].init();
                run(o[k].also);
            }
        }
    }
    run(MIM);
});