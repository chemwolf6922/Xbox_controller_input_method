setInterval(function getData(){
    $.get('/getInfo',function(data){draw(data)})
},16);


function draw(data){
    var LSXText = document.getElementById('LSX');
    var LSYText = document.getElementById('LSY');
    var RSXText = document.getElementById('RSX');
    var RSYText = document.getElementById('RSY');
    LSXText.innerHTML = String(data.LSX);
    LSYText.innerHTML = String(data.LSY);
    RSXText.innerHTML = String(data.RSX);
    RSYText.innerHTML = String(data.RSY);
}
