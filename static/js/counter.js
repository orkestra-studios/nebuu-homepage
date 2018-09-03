var scount = 0
const numberWithCommas = (x) => {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}

function countUp(count)
{
  var display = document.getElementById('count'),
      value = scount,
      delay = count-value<10 ? 640/(count-value+1) : 10;
 
  var timer = setTimeout(function() {
      var value = scount;
      if (value<count) {
        var incr = Math.max(1,Math.round((count-value)/10));
        scount = value + incr;
        display.innerHTML = numberWithCommas(scount);
        countUp(count);
      } else {
        display.innerHTML = numberWithCommas(count);
      }
  }, delay);
}

function getTextWidth(text, font) {
    // re-use canvas object for better performance
    var canvas = getTextWidth.canvas || (getTextWidth.canvas = document.createElement("canvas"));
    var context = canvas.getContext("2d");
    context.font = font;
    var metrics = context.measureText(text);
    return metrics.width;
}

function submitForm() { 
  var fs = document.getElementById("mainset");
  //fs.disabled = true;
  var hourglass = document.getElementById("hourglass");
  hourglass.setAttribute("style","animation: fadein 1s;width:48px;height;48px;");
  var form = document.getElementById("statform");
  form.submit();
}
