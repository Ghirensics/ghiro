$(document).ready(function() {

    $('.tool').tooltip();

    $('.pop').popover();

    $(".fancybox").fancybox({
        'type': 'image',
        helpers : {
            title : {
                type : 'float'
            }
        },
        tpl : {
            error : 'Can not dispaly preview, unsupported format.'
        },
        'autoSize': 'false'
    });
    
    var Popup = {
        init : function () {
            $('a.action_print').bind('click', Popup.printIt);
        },

        printIt : function () {
            var win = window.open("","Print");
            if (win.document) {
                win.document.writeln('<img src="'+ $(this).attr('href') +'" alt="image" />');
                win.document.close();
                win.focus();
                win.print();
            }

            return false;
            }
    };
    $(document).ready(function () {
        Popup.init();
    });

    $('#btn_submit').click(function(){
        var btn = $(this);
        btn.button('loading');
        setTimeout(function(){
            btn.button('reset')
        }, 3000);
    });

    $('.btn-close-case').click(function(){
        var id = $(this).attr("id");
        $("#id-close").attr({href: id});
    });
    
    $('.btn-delete-case').click(function(){
        var id = $(this).attr("id");
        $("#id-delete").attr({href: id});
    });

    $('.btn-delete-report').click(function(){
        var id = $(this).attr("id");
        $("#id-delete-report").attr({href: id});
    });

    $('.favorite').click(function(){
        var id = $(this).attr("id");
        var rel = $(this).attr("rel");
        $.ajax({
            type: "GET",
            url: id,
            success: function(data){
                if (data == "true"){
                    $(".star"+rel).addClass('btn-warning');
                }else{
                    $(".star"+rel).removeClass('btn-warning');
                }
            }
        });
    });

    var feed_width = $('#comment').width();
    var scr_w = screen.width;
    var btn_width = 42;
    var move_right = scr_w - btn_width;
    var slide_from_right = scr_w - (feed_width - btn_width);

    positioningForm();

    $('.right_btn').click(function(){
        slideFromRight();
    });

    $('.comment_close').click(function(){
        positioningForm();
    });

    function positioningForm(){
        $('#comment').css({"left": move_right+"px"}).show();
    }

    function slideFromRight(){
        $('#comment').animate({left: slide_from_right+"px"},{duration: 'slow',easing: 'easeOutCubic'});
    }
});

function internetStatus(){
    var connected = true;
    var img = document.createElement('img');
    img.src = 'http://www.getghiro.org/static/img/logo_1_original.png?ver=' + (new Date()).getTime();
    img.onerror = function() {
        $("#noNet").show();
        $("#map_canvas").hide();
    }
    if (connected){
        loadScript()
    }
}

function loadScript() {
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.src = "http://maps.google.com/maps/api/js?sensor=false&callback=initialize";
    document.body.appendChild(script);
    $('a[data-toggle="tab"]').on('shown', function (e) {
        google.maps.event.trigger(map, 'resize');
        map.setCenter(marker.getPosition());
    });
}
