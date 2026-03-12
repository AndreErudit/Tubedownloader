document.querySelector("form").addEventListener("submit", function(){

let bar = document.getElementById("bar");

let width = 0;

let interval = setInterval(function(){

if(width >= 100){

clearInterval(interval);

}

else{

width++;

bar.style.width = width + "%";

}

},50)

})