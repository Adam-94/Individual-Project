var i = 0;
var text = "Getting Vehicle Data...";
var speed = 120;

function loadingText() {
    if (i < text.length) {
        document.getElementById('btn-label').innerHTML += text.charAt(i);
    }
    ++i;
    setTimeout(loadingText, speed);
}

document.addEventListener('DOMContentLoaded', (ev)=>{
let form = document.getElementById('myform');
let input = document.getElementById('capture');

input.addEventListener('change', (ev)=>{
console.dir( input.files[0] );
if(input.files[0].type.indexOf("image/") > -1){
    let img = document.getElementById('capture');
    img.src = window.URL.createObjectURL(input.files[0]);
}

var data = new FormData();
data.append('image', $('#capture')[0].files[0])
console.log(data)
$.ajax({
    type: 'POST',
    url: '/take_pic',
    data: new FormData($('#myform')[0]),
    contentType: false,
    cache: false,
    processData: false,
    async: true,
    error:function(data){
        console.log("upload error");
    },
    success: function (data) {
        console.log('Success!');
        $("#btn-label").text('');
        getResults();
        loadingText();
    },
});
})
})

function getResults() {
    $.ajax({
    url: '/motdata',
    type: 'GET',
    dataType: 'json',
    async: true,
    cache: false,
    error:function(data){
        console.log("error");
    },
    success: function (data) {
        console.log(data);
        $("#numplate").text(data.plate)
        $("#carmake").text(data.car)
        $("#yearman").text(data.year)
        $("#tax").text(data.tax)
        $("#mot").text(data.mot)

        $("#btn-label").text("Take a Picture")
    },
});
}
