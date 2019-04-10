$('.btn-example').change(function(){
    if ($('input:checkbox[id="face"]').is(':checked') == true){
        var $href = $(this).attr('href');
        layer_popup($href);
    }else{
        sessionStorage.removeItem( 'x0' );
        sessionStorage.removeItem( 'x1' );
        sessionStorage.removeItem( 'y0' );
        sessionStorage.removeItem( 'y1' );
    }
});
function layer_popup(el){

    var $el = $(el);        //레이어의 id를 $el 변수에 저장
    var isDim = $el.prev().hasClass('dimBg');   //dimmed 레이어를 감지하기 위한 boolean 변수

    isDim ? $('.dim-layer').fadeIn() : $el.fadeIn();

    var $elWidth = ~~($el.outerWidth()),
        $elHeight = ~~($el.outerHeight()),
        docWidth = $(document).width(),
        docHeight = $(document).height();

    // 화면의 중앙에 레이어를 띄운다.
    if ($elHeight < docHeight || $elWidth < docWidth) {
        $el.css({
            marginTop: -$elHeight /2,
            marginLeft: -$elWidth/2
        })
    } else {
        $el.css({top: 0, left: 0});
    }





    $el.find('a.btn-layerClose').click(function(){
        isDim ? $('.dim-layer').fadeOut() : $el.fadeOut(); // 닫기 버튼을 클릭하면 레이어가 닫힌다.
        return false;
    });

    $('.layer .dimBg').click(function(){
        $('.dim-layer').fadeOut();
        return false;
    });

}
    var x0=0,
        y0=0,
        y1=0,
        x1=0;

    $('.frameResizing').mousedown(function(){
        x0=200;
        y0=150;
    }).mousemove(function(){
        x1=600;
        y1=450;
    }).mouseup(function(){
//        sessionStorage.setItem( 'x0', x0 );
//        sessionStorage.setItem( 'y0', y0 );
//        sessionStorage.setItem( 'x1', x1 );
//        sessionStorage.setItem( 'y1', y1 );
        $('input[name="rect_x"]').val(x0);
        $('input[name="rect_y"]').val(y0);
        $('input[name="rect_width"]').val(x1-x0);
        $('input[name="rect_height"]').val(y1-y0);
        alert("resize postion saved");
    });