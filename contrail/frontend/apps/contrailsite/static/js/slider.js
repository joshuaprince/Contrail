var i;
var minp = 0;
var maxp = 200;

var pricehr_values = [0];
var memory_values = [0];
var vcpu_values = [0];

for(i = minp; i < maxp; i++) {
    // pricehr
    var pricehr_minv = Math.log(0.01);
    var pricehr_maxv = Math.log(30);
    var scale = (pricehr_maxv-pricehr_minv) / (maxp-minp);
    var value = Math.exp(pricehr_minv + scale*(i-minp));
    if(!pricehr_values.includes(value.toFixed(2))){
        pricehr_values.push(value.toFixed(2))
    }
    else maxp++;

    // memory
    var memory_minv = Math.log(1);
    var memory_maxv = Math.log(4000);
    var scale = (memory_maxv-memory_minv) / (maxp-minp);
    var value = Math.exp(memory_minv + scale*(i-minp));
    if(!memory_values.includes(value.toFixed(0))){
        memory_values.push(value.toFixed(0))
    }
    else maxp++;

    // vcpu
    var vcpu_minv = Math.log(1);
    var vcpu_maxv = Math.log(50);
    var scale = (vcpu_maxv-vcpu_minv) / (maxp-minp);
    var value = Math.exp(vcpu_minv + scale*(i-minp));
    if(!vcpu_values.includes(value.toFixed(0))){
        vcpu_values.push(value.toFixed(0))
    }
    else maxp++;
}



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
