
$(window).on("load", function () {
    var zoom = {
        zoomboxLeft: null, zoomboxTop: null, //zoombox
        cursorStartX: null, cursorStartY: null, //cursor
        imgStartLeft: null, imgStartTop: null, //image
        minDragLeft: null, maxDragLeft: null, minDragTop: null, maxDragTop: null
    };

    //gestore di chiavi ===========================================
    $(document).keydown(function (e) {
        if (e.which == 32) { if (!$(".zoombox img").hasClass("moving")) { $(".zoombox img").addClass("drag"); } } //SPACE
    });
    $(document).keyup(function (e) {
        if (e.which == 32) { if (!$(".zoombox img").hasClass("moving")) { $(".zoombox img").removeClass("drag"); } } //SPACE
    });

    //RESetta immagine =======================================
    $(".reset").on("click", function () {
        var zoombox = "#" + $(this).parent().attr("id") + " .zoombox";
        $(zoombox + " img").css({ "left": 0, "top": 0, "width": $(zoombox).width(), "height": $(zoombox).height() - 30 });
    }).click();

    //ZOOM&DRAG-EVENTS=======================================

    $(".zoombox img").mousedown(function (e) {
        e.preventDefault();
        $(".zoombox img").addClass("moving");
        var selector = $(this).next();
        var zoombox = $(this).parent();
        $(zoombox).addClass("active");

        //store zoombox left&top
        zoom.zoomboxLeft = $(zoombox).offset().left + parseInt($(zoombox).css("border-left-width").replace(/\D+/, ""));
        zoom.zoomboxTop = $(zoombox).offset().top + parseInt($(zoombox).css("border-top-width").replace(/\D+/, ""));

        //store starting punto del cursore (relativo zoombox)
        zoom.cursorStartX = e.pageX - zoom.zoomboxLeft;
        zoom.cursorStartY = e.pageY - zoom.zoomboxTop;

        if ($(".zoombox img").hasClass("drag")) {
            //store starting positions of image (relativo zoombox)
            zoom.imgStartLeft = $(this).position().left;
            zoom.imgStartTop = $(this).position().top;

            //imposta drag boundaries relativo a zoombox)
            zoom.minDragLeft = $(zoombox).width() - $(this).width();
            zoom.maxDragLeft = 0;
            zoom.minDragTop = $(zoombox).height() - $(this).height();
            zoom.maxDragTop = 0;
        } else {
            //imposta drag boundaries relativo a zoombox)
            zoom.minDragLeft = 0;
            zoom.maxDragLeft = $(zoombox).width();
            zoom.minDragTop = 0;
            zoom.maxDragTop = $(zoombox).height();

            //activa zoom-selector

            $(selector).css({ "display": "block", "width": 0, "height": 0, "left": zoom.cursorStartX, "top": zoom.cursorStartY });

        }
    });

    //MOUSEMOVE----------------------------------------------
    $(document).mousemove(function (e) {
        if ($(".zoombox img").hasClass("moving")) {
            if ($(".zoombox img").hasClass("drag")) {
                var img = $(".zoombox.active img")[0];

                //update image position (relative zoombox)
                $(img).css({
                    "left": zoom.imgStartLeft + (e.pageX - zoom.zoomboxLeft) - zoom.cursorStartX,
                    "top": zoom.imgStartTop + (e.pageY - zoom.zoomboxTop) - zoom.cursorStartY
                });
                //prevent dragging in prohibited areas (relative to zoombox)
                if ($(img).position().left <= zoom.minDragLeft) { $(img).css("left", zoom.minDragLeft); } else
                    if ($(img).position().left >= zoom.maxDragLeft) { $(img).css("left", zoom.maxDragLeft); }
                if ($(img).position().top <= zoom.minDragTop) { $(img).css("top", zoom.minDragTop); } else
                    if ($(img).position().top >= zoom.maxDragTop) { $(img).css("top", zoom.maxDragTop); }
            } else {
                //calculate selector width and height (relative to zoombox)
                var width = (e.pageX - zoom.zoomboxLeft) - zoom.cursorStartX;
                var height = (e.pageY - zoom.zoomboxTop) - zoom.cursorStartY;

                //prevent dragging in prohibited areas (relative to zoombox)
                if (e.pageX - zoom.zoomboxLeft <= zoom.minDragLeft) { width = zoom.minDragLeft - zoom.cursorStartX; } else
                    if (e.pageX - zoom.zoomboxLeft >= zoom.maxDragLeft) { width = zoom.maxDragLeft - zoom.cursorStartX; }
                if (e.pageY - zoom.zoomboxTop <= zoom.minDragTop) { height = zoom.minDragTop - zoom.cursorStartY; } else
                    if (e.pageY - zoom.zoomboxTop >= zoom.maxDragTop) { height = zoom.maxDragTop - zoom.cursorStartY; }

                //update zoom-selector
                var selector = $(".zoombox.active .selector")[0];
                $(selector).css({ "width": Math.abs(width), "height": Math.abs(height) });
                if (width < 0) { $(selector).css("left", zoom.cursorStartX - Math.abs(width)); }
                if (height < 0) { $(selector).css("top", zoom.cursorStartY - Math.abs(height)); }
            }
        }
    });

    //MOUSEUP------------------------------------------------
    $(document).mouseup(function () {
        if ($(".zoombox img").hasClass("moving")) {
            if (!$(".zoombox img").hasClass("drag")) {
                var img = $(".zoombox.active img")[0];
                var selector = $(".zoombox.active .selector")[0];

                if ($(selector).width() > 0 && $(selector).height() > 0) {
                    //resize zoom-selector and image
                    var magnification = ($(selector).width() < $(selector).height() ? $(selector).parent().width() / $(selector).width() : $(selector).parent().height() / $(selector).height()); //go for the highest magnification
                    var hFactor = $(img).width() / ($(selector).position().left - $(img).position().left);
                    var vFactor = $(img).height() / ($(selector).position().top - $(img).position().top);
                    $(selector).css({ "width": $(selector).width() * magnification, "height": $(selector).height() * magnification });
                    $(img).css({ "width": $(img).width() * magnification, "height": $(img).height() * magnification });
                    //correct for misalignment during magnification, caused by size-factor
                    $(img).css({
                        "left": $(selector).position().left - ($(img).width() / hFactor),
                        "top": $(selector).position().top - ($(img).height() / vFactor)
                    });

                    //reposition zoom-selector and image (relative to zoombox)
                    var selectorLeft = ($(selector).parent().width() / 2) - ($(selector).width() / 2);
                    var selectorTop = ($(selector).parent().height() / 2) - ($(selector).height() / 2);
                    var selectorDeltaLeft = selectorLeft - $(selector).position().left;
                    var selectorDeltaTop = selectorTop - $(selector).position().top;
                    $(selector).css({ "left": selectorLeft, "top": selectorTop });
                    $(img).css({ "left": "+=" + selectorDeltaLeft, "top": "+=" + selectorDeltaTop });
                }
                //deactivate zoom-selector
                $(selector).css({ "display": "none", "width": 0, "height": 0, "left": 0, "top": 0 });
            } else { $(".zoombox img").removeClass("drag"); }
            $(".zoombox img").removeClass("moving");
            $(".zoombox.active").removeClass("active");
        }
    });

    /*function drawLine(e) {
        e.preventDefault();
        $(".zoombox img").addClass("moving");
        var selector = $('.zoombox').next();
        var zoombox = $('.zoombox').parent();
        $(zoombox).addClass("active");

        //store zoombox left&top
        zoom.zoomboxLeft = $(zoombox).offset().left + parseInt($(zoombox).css("border-left-width").replace(/\D+/, ""));
        zoom.zoomboxTop = $(zoombox).offset().top + parseInt($(zoombox).css("border-top-width").replace(/\D+/, ""));

        //store starting positions of cursor (relative to zoombox)
        zoom.cursorStartX = e.pageX - zoom.zoomboxLeft;
        zoom.cursorStartY = e.pageY - zoom.zoomboxTop;
        //activate zoom-selector
        $(selector).css({ "display": "block", "width": 0, "height": 0, "left": zoom.cursorStartX, "top": zoom.cursorStartY });

    }*/
});