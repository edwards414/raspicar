function changeimg1(){
    document.getElementById("pca1").innerHTML="<img src='{{url_for('/static', filename='img/botton-red.png')}}'>";
    document.getElementById("pca2").innerHTML="<img src='{{url_for('/static', filename='img/botton.png')}}'>";
    document.getElementById("pca3").innerHTML="<img src='{{url_for('/static', filename='img/botton.png')}}'>";
    window.location.href='run'
}   
function changeimg2(){
    document.getElementById("pca1").innerHTML="<img src='{{url_for('/static', filename='img/botton.png')}}'>";
    document.getElementById("pca2").innerHTML="<img src='{{url_for('/static', filename='img/botton-red.png')}}'>";
    document.getElementById("pca3").innerHTML="<img src='{{url_for('/static', filename='img/botton.png')}}'>";
    window.location.href='back'
}   
function changeimg3(){
    document.getElementById("pca1").innerHTML="<img src='{{url_for('/static', filename='img/botton.png')}}'>";
    document.getElementById("pca2").innerHTML="<img src='{{url_for('/static', filename='img/botton.png')}}'>";
    document.getElementById("pca3").innerHTML="<img src='{{url_for('/static', filename='img/botton-red.png')}}'>";
    window.location.href='stop'
}   
