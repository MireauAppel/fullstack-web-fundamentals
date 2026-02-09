
let i = 0;
let timer = null;

function compteur(){
    const bouton = document.getElementById('toggle');
    const displayCount = document.getElementById('count');
    const displayFB = document.getElementById('fb');

    if(timer == null){
        bouton.innerText = "Stop";

        timer = setInterval(() => {
            i++;
            displayCount.innerHTML = i;
            
            if (i % 3 == 0 && i % 5 == 0){
                displayFB.innerHTML = "Fizz-buzz";
            } else if (i % 3 == 0){
                displayFB.innerHTML = "Fizz";
            } else if (i % 5 == 0) {
                displayFB.innerHTML = "Buzz";
            } else {
                displayFB.innerHTML = "";
            }
        }, 1000);
    } else{
        clearInterval(timer);
        timer = null;
        bouton.innerText = "Start";
    }   
}


