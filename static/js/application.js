$(document).ready(function() {
    
    $('.tool').tooltip();
    
    $('.pop').popover();
    $(".fancybox").fancybox({
        'type': 'image',
        helpers : {
            title : {
                type : 'float'
            },
        },
        tpl : {
            error : 'Can not dispaly preview, unsupported format.'
        },
        'autoSize': 'false'
    });
    
    Popup = {
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
        }
        $(document).ready(function () {
        Popup.init();
    });
    
    $('#btn_submit').click(function(){
        var btn = $(this);
        btn.button('loading');
        setTimeout(function(){
            btn.button('reset')
        }, 2000)
    });
    
    $('.btn-close-case').click(function(){
        var id = $(this).attr("id");
        $("#id-close").attr({href: id});
    });
    
    $('.btn-delete-case').click(function(){
        var id = $(this).attr("id");
        $("#id-delete").attr({href: id});
    });
});

function internetStatus(){
    var status = navigator.onLine ? 'online' : 'offline';
    if (status == 'offline'){
        alert("To use the map feature you need to be connected to internet.");
    }else{
        $('#map_canvas').fadeIn();
        loadScript();
    }
};
