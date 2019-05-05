$(".btn-example").change(function() {
  if ($('input:checkbox[id="face"]').is(":checked") == true) {
    var $href = $(this).attr("href");

    layer_popup($href);
  } else {
    $('input[name="rect_x"]').val(0);
    $('input[name="rect_y"]').val(0);
    $('input[name="rect_width"]').val(0);
    $('input[name="rect_height"]').val(0);
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
    if (
      $('input[name="rect_width"]').val() == 0 ||
      $('input[name="rect_height"]').val() == 0
    ) {
      alert("Drag again...");
    } else {
      isDim ? $(".dim-layer").fadeOut() : $el.fadeOut(); // 닫기 버튼을 클릭하면 레이어가 닫힌다.
      return false;
    }
  });

  $(".layer .dimBg").click(function() {
    $(".dim-layer").fadeOut();
    return false;
  });

  //Canvas
  var canvas = document.getElementById("canvas");
  var ctx = canvas.getContext("2d");
  ctx.fillStyle = "#FFF";
  ctx.strokeStyle = "red";
  //Variables
  //   var canvasx = $(canvas).offset().left;
  //   var canvasy = $(canvas).offset().top;
  var canvasx = 0;
  var canvasy = 0;
  var last_mousex = (last_mousey = 0);
  var mousex = (mousey = 0);
  var mousedown = false;
  var width_save = 0;
  var height_save = 0;

  //jsA start point
  var start_x = 0;
  var start_y = 0;

  //$(".frameResizing")
  $(canvas)
    .on("mousedown", function(e) {
      // last_mousex = parseInt(e.clientX - canvasx);
      // last_mousey = parseInt(e.clientY - canvasy);
      last_mousex = parseInt(e.offsetX - canvasx);
      last_mousey = parseInt(e.offsetY - canvasy);

      if (last_mousex < 0){
	      last_mousex = 0;
      }

      if (last_mousey < 0){
	      last_mousey = 0;
      }

      //console.log("mouse donw..");
      // x0 = last_mousex;
      // y0 = last_mousey;
      mousedown = true;
    })
    .on("mousemove", function(e) {
      mousex = parseInt(e.offsetX - canvasx);
      mousey = parseInt(e.offsetY - canvasy);

      // x0 = mousex;
      // y0 = mousey;
      if (mousedown) {
        ctx.clearRect(0, 0, canvas.width, canvas.height); //clear canvas
        ctx.beginPath();
        var width = mousex - last_mousex;
        var height = mousey - last_mousey;
        ctx.rect(last_mousex, last_mousey, width, height);
	
      	if (width < 0) {
	        if (height < 0) {
			start_x = mousex;
			start_y = mousey;
		}else{
			start_x = mousex;
			start_y = last_mousey;
	        }
        }else{
	        if (height < 0) {
	      		start_x = last_mousex;
			start_y = last_mousey;
		}else{
			start_x = last_mousex;
			start_y = mousey;
	        }
	}

        if (width < 0) {
	  width = -width;
	}
	      
        if (height < 0) {
          height = -height;
        }

        width_save = width;
        height_save = height;
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
          "|| box_start: " +
          start_x +
          ", " +
          start_y +
          "|| mousedown: " +
          mousedown +
          "|| width: " +
          width +
          ", " +
          "height: " +
          height
      );
    })
    .on("mouseup", function(e) {
      //        sessionStorage.setItem( 'x0', x0 );
      //        sessionStorage.setItem( 'y0', y0 );
      //        sessionStorage.setItem( 'x1', x1 );
      //        sessionStorage.setItem( 'y1', y1 );
      mousedown = false;
      $('input[name="rect_x"]').val(start_x);
      $('input[name="rect_y"]').val(start_y);
      $('input[name="rect_width"]').val(width_save);
      $('input[name="rect_height"]').val(height_save);
      alert("resize postion saved");
    });
}
