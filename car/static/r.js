document.getElementById("scope").onmousemove = getMouseXY; 
function getMouseXY(e) {
    var tempX,tempx1;
    tempX = event.clientX - document.getElementById("scope").offsetLeft-document.getElementById("scope").clientWidth/2; 
    tempx1= (tempX*30)/(document.getElementById("scope").clientWidth/2)
    
    if (Math.round(tempx1)<0){
        document.getElementById("degree").innerHTML ='向左 ' + Math.abs(Math.round(tempx1)) + "度" ;
        
    }
    else{
        document.getElementById("degree").innerHTML ='向右 ' + Math.round(tempx1) + "度";
    }
    

}                  