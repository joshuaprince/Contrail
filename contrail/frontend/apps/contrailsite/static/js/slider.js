


function logvalues(min, max){
  var i;
  var minp = 0;
  var maxp = 500;
  var values = [0]

  for(i = minp; i < maxp; i++) {
      var minv = Math.log(min);
      var maxv = Math.log(max);
      var scale = (maxv-minv) / (maxp-minp);
      var value = Math.exp(minv + scale*(i-minp));
      if(!values.includes(value.toFixed(2))){
          values.push(value.toFixed(2))
      }
  }

  values.push(Math.ceil(value))

  return values;
}

var pricehr_values = logvalues(0.01, 30);
var memory_values = logvalues(1, 4000);
var vcpu_values = logvalues(1, 50);

$(".pricehr-range-slider").ionRangeSlider({
     type: "double",
     // from: custom_values.indexOf(0),
     // to: custom_values.indexOf(1.6),
     values: pricehr_values
});

$(".memory-range-slider").ionRangeSlider({
     type: "double",
     // from: custom_values.indexOf(0),
     // to: custom_values.indexOf(1.6),
     values: memory_values
});

$(".vcpu-range-slider").ionRangeSlider({
     type: "double",
     // from: custom_values.indexOf(0),
     // to: custom_values.indexOf(1.6),
     values: vcpu_values
});
