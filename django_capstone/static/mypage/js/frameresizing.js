$(".btn-example").change(function() {
  if ($('input:checkbox[id="face"]').is(":checked") == true) {
    var $href = $(this).attr("href");
    layer_popup($href);
  } else {
    sessionStorage.removeItem("x0");
    sessionStorage.removeItem("x1");
    sessionStorage.removeItem("y0");
    sessionStorage.removeItem("y1");
  }
});
function layer_popup(el) {
  var $el = $(el); //레이어의 id를 $el 변수에 저장
  var isDim = $el.prev().hasClass("dimBg"); //dimmed 레이어를 감지하기 위한 boolean 변수

  isDim ? $(".dim-layer").fadeIn() : $el.fadeIn();

  var $elWidth = ~~$el.outerWidth(),
    $elHeight = ~~$el.outerHeight(),
    docWidth = $(document).width(),
    docHeight = $(document).height();

  // 화면의 중앙에 레이어를 띄운다.
  if ($elHeight < docHeight || $elWidth < docWidth) {
    $el.css({
      marginTop: -$elHeight / 2,
      marginLeft: -$elWidth / 2
    });
  } else {
    $el.css({ top: 0, left: 0 });
  }

  $el.find("a.btn-layerClose").click(function() {
    isDim ? $(".dim-layer").fadeOut() : $el.fadeOut(); // 닫기 버튼을 클릭하면 레이어가 닫힌다.
    return false;
  });

  $(".layer .dimBg").click(function() {
    $(".dim-layer").fadeOut();
    return false;
  });
}

var x0 = 0,
  y0 = 0,
  y1 = 0,
  x1 = 0;

//Canvas
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
ctx.fillStyle = "#FFF";
ctx.strokeStyle = "red";
//Variables
var canvasx = $(canvas).offset().left;
var canvasy = $(canvas).offset().top;
var last_mousex = (last_mousey = 0);
var mousex = (mousey = 0);
var mousedown = false;

$(".frameResizing")
  .ctx.on("mousedown", function(e) {
    last_mousex = parseInt(e.clientX - canvasx);
    last_mousey = parseInt(e.clientY - canvasy);
    x0 = last_mousex;
    y0 = last_mousey;
    mousedown = true;
  })
  .ctx.on("mousemove", function(e) {
    mousex = parseInt(e.clientX - canvasx);
    mousey = parseInt(e.clientY - canvasy);
    x0 = mousex;
    y0 = mousey;
    if (mousedown) {
      ctx.clearRect(0, 0, canvas.width, canvas.height); //clear canvas
      ctx.beginPath();
      var width = mousex - last_mousex;
      var height = mousey - last_mousey;
      ctx.rect(last_mousex, last_mousey, width, height);
      ctx.strokeStyle = "red";
      ctx.lineWidth = 10;
      ctx.stroke();
    }
    //Output
    $("#output").html(
      "current: " +
        mousex +
        ", " +
        mousey +
        "|| last: " +
        last_mousex +
        ", " +
        last_mousey +
        "|| mousedown: " +
        mousedown
    );
  })
  .ctx.on("mouseup", function(e) {
    //        sessionStorage.setItem( 'x0', x0 );
    //        sessionStorage.setItem( 'y0', y0 );
    //        sessionStorage.setItem( 'x1', x1 );
    //        sessionStorage.setItem( 'y1', y1 );
    mousedown = false;
    $('input[name="rect_x"]').val(x0);
    $('input[name="rect_y"]').val(y0);
    $('input[name="rect_width"]').val(x1);
    $('input[name="rect_height"]').val(y1);
    alert("resize postion saved");
  });
