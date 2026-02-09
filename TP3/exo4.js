
const p = Math.random(); 
let caramels = 0;
function get_pill_color_from_user() {
    return new Promise((resolve) => {
        const redBtn = document.querySelector("#red");
        const blueBtn = document.querySelector("#blue");

        const handleChoice = (color) => {
            redBtn.onclick = null; 
            blueBtn.onclick = null;
            resolve(color);
        };

        redBtn.onclick = () => handleChoice('red');
        blueBtn.onclick = () => handleChoice('blue');
    });
}

function resolve_gains(userChoice, n) {
    const display = document.querySelector("#gains");
    
    const winningColor = (n < p) ? 'red' : 'blue';

    if (userChoice === winningColor) {
        caramels++; 
        alert("Gagné ! Un caramel de plus.");
    } else {
        caramels--;
        alert("Perdu ! Vous perdez un caramel.");
    }

    display.innerText = "Caramels gagnés : " + caramels;
}

async function start_betting_game() {
    while (true) {
        
        let n = Math.random();

        
        let userChoice = await get_pill_color_from_user();

        
        resolve_gains(userChoice, n);
    }
}

start_betting_game();