


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

var $mem_slider = $(".memory-range-slider"),
    $mem_inputFrom = $(".memory-input-from"),
    $mem_inputTo = $(".memory-input-to");

var $vcpu_slider = $(".vcpu-range-slider"),
    $vcpu_inputFrom = $(".vcpu-input-from"),
    $vcpu_inputTo = $(".vcpu-input-to");

var $price_slider = $(".pricehr-range-slider"),
    $price_inputFrom = $(".pricehr-input-from"),
    $price_inputTo = $(".pricehr-input-to");

var pricehr_values = logvalues(0.01, 30);
var memory_values = logvalues(1, 4000);
var vcpu_values = logvalues(1, 50);


$mem_slider.ionRangeSlider({
     type: "double",
     from: memory_values.indexOf(memory_values[0]),
     to: memory_values.indexOf(memory_values[300]),
     onStart: mem_updateInputs,
     onChange: mem_updateInputs,
     values: memory_values
});

$vcpu_slider.ionRangeSlider({
     type: "double",
     from: vcpu_values.indexOf(vcpu_values[0]),
     to: vcpu_values.indexOf(vcpu_values[200]),
     onStart: vcpu_updateInputs,
     onChange: vcpu_updateInputs,
     values: vcpu_values
});

$price_slider.ionRangeSlider({
     type: "double",
     prefix: "$ ",
     from: pricehr_values.indexOf(pricehr_values[0]),
     to: pricehr_values.indexOf(pricehr_values[100]),
     onStart: price_updateInputs,
     onChange: price_updateInputs,
     values: pricehr_values
});


// prettify_enabled: true,
// prettify_separator: ".",
// values_separator: " - ",
// force_edges: true
















function mem_updateInputs (data) {
  console.log(data)
    from = data.from_value;
    to = data.to_value;

    $mem_inputFrom.prop("value", from);
    $mem_inputTo.prop("value", to);
}

$mem_inputFrom.on("input", function () {
    var val = $(this).prop("value");

    // validate
    if (val < min) {
        val = min;
    } else if (val > to) {
        val = to;
    }

    $mem_slider.data("ionRangeSlider").update({
        from: val
    });
});

$mem_inputTo.on("input", function () {
    var val = $(this).prop("value");

    // validate
    if (val < from) {
        val = from;
    } else if (val > max) {
        val = max;
    }

    $mem_slider.data("ionRangeSlider").update({
        to: val
    });
});














function vcpu_updateInputs (data) {
    from = data.from_value;
    to = data.to_value;

    $vcpu_inputFrom.prop("value", from);
    $vcpu_inputTo.prop("value", to);
}

$vcpu_inputFrom.on("input", function () {
    var val = $(this).prop("value");

    // validate
    if (val < min) {
        val = min;
    } else if (val > to) {
        val = to;
    }

    $vcpu_slider.data("ionRangeSlider").update({
        from: val
    });
});

$vcpu_inputTo.on("input", function () {
    var val = $(this).prop("value");

    // validate
    if (val < from) {
        val = from;
    } else if (val > max) {
        val = max;
    }

    $vcpu_slider.data("ionRangeSlider").update({
        to: val
    });
});












function price_updateInputs (data) {
    from = data.from_value;
    to = data.to_value;

    $price_inputFrom.prop("value", from);
    $price_inputTo.prop("value", to);
}

$price_inputFrom.on("input", function () {
    var val = $(this).prop("value");

    // validate
    if (val < min) {
        val = min;
    } else if (val > to) {
        val = to;
    }

    $price_slider.data("ionRangeSlider").update({
        from: val
    });
});

$price_inputTo.on("input", function () {
    var val = $(this).prop("value");

    // validate
    if (val < from) {
        val = from;
    } else if (val > max) {
        val = max;
    }

    $price_slider.data("ionRangeSlider").update({
        to: val
    });
});
