function Ball() {
    this.id = "ball";
    this.x = 50;
    this.y = 50;
    this.vx = 1;
    this.vy = 1;
    this.width = 64;
    this.height= 64;
}

function Racket(id, x, y){
    this.id = id;
    this.x = x;
    this.y = y;
    this.width = 55;
    this.height = 196;
    this.speed = 10;
}

let buttons = {
    p1_up: false,
    p1_down: false,
    p2_up: false,
    p2_down: false
}

let scores = {p1: 0, p2: 0}
let scoreElement;
let ball, racketL, racketR;

function track_player_input(event) {
    let state = (event.type == "keydown");
        switch(event.key) {
            case "a": buttons.p1_up = state; break;
            case "q": buttons.p1_down = state; break;
            case "p": buttons.p2_up = state; break;
            case "m": buttons.p2_down = state; break;
        }
    
}

document.addEventListener("keydown", track_player_input);
document.addEventListener("keyup", track_player_input);

function place_objects(objects) {
    for(let object of objects) {
        let element = document.getElementById(object.id);
        element.style.left = object.x + "px";
        element.style.top = object.y + "px";
    }
}

function resetBall(){
    let rect = document.body.getBoundingClientRect();
    ball.x = rect.width / 2 - ball.width / 2;
    ball.y = rect.height / 2 - ball.height / 2;
    ball.vx = (Math.random() > 0.5 ? 1 : -1) * 10;
    ball.vy = (Math.random() > 0.5 ? 1 : -1) * 10;
}

function update() {
    let rect = document.body.getBoundingClientRect();
    let ballCenterY = ball.y + (ball.height / 2);

    ball.x += ball.vx;
    ball.y += ball.vy;

    if (ball.x <= racketL.x + racketL.width && ballCenterY >= racketL.y && ballCenterY <= racketL.y + racketL.height){
        ball.vx=Math.abs(ball.vx);
    }
    if (ball.x + ball.width >= racketR.x && ballCenterY >= racketR.y && ballCenterY <= racketR.y + racketR.height){
        ball.vx = -Math.abs(ball.vx);
    }

    if (ball.x < 0) {
        scores.p2++;
        resetBall();
    } else if (ball.x > rect.width - ball.width) {
        scores.p1++;
        resetBall();
    }
    
    if (ball.y < 0 || ball.y > rect.height - ball.height){
        ball.vy = -ball.vy;
    }

    if (scoreElement) scoreElement.innerHTML = scores.p1 + " - " + scores.p2;
    //p1
    if (buttons.p1_up && racketL.y > 0) {
        racketL.y -= racketL.speed;
    }
    if (buttons.p1_down && racketL.y < rect.height - racketL.height) {
        racketL.y += racketL.speed;
    }

    //pé2
    if (buttons.p2_up && racketR.y > 0) {
        racketR.y -= racketR.speed;
    }
    if (buttons.p2_down && racketR.y < rect.height - racketR.height) {
        racketR.y += racketR.speed;
    }

    place_objects([ball, racketL, racketR]);
}


function init() {
    let rect = document.body.getBoundingClientRect();
    scoreElement = document.getElementById("scores");
    ball = new Ball();
    racketL = new Racket("left", 20, (rect.height / 2) - 98);
    racketR = new Racket("right", rect.width - 75, (rect.height / 2) - 98);
    setInterval(update, 16); //changé pour mouvement plus fluide
    resetBall();
}