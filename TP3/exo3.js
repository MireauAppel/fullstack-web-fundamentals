let x = 0;
let sum = 0;
let sum_display = "";
const div = document.querySelector("#calc")
const input = document.querySelector("#input")
function update_sum(){
    if (x>=5){
        x=0;
        sum = 0;
        sum_display = "";
        div.innerText = ""; 
    }
    let j = parseInt(input.value);
    if (isNaN(j)) return;
    if (sum_display != ""){
        sum_display+= "+";
    }
    sum_display=sum_display+j;
    sum += j;
    x++;
    if (x == 5){
        sum_display+= "=" + sum;
    }
    div.innerText=sum_display;
    input.value = "";
}

function get_next_user_number(){
    return new Promise((resolve) => {
        const btn = document.querySelector("#btn");
        
        const handler = () => {
            btn.removeEventListener('click', handler);
            resolve();
        }
        btn.addEventListener('click', handler);
    });
}

async function sum_5_numbers_async() {
    document.querySelector("#btn").removeEventListener('click', update_sum);

    while (true) {
        await get_next_user_number();
        update_sum();
    }
}

sum_5_numbers_async();
function one_second() {
    return new Promise((resolve) => {
        setTimeout(resolve, 1000);
    });
}

async function blink_text(text) {
    let d = document.createElement("div");
    d.innerText = text;
    d.style.display = 'block';
    document.querySelector('body').appendChild(d);

    let div_visible = true;
    while (true) {
        await one_second();
        if (div_visible === true) {
            div_visible = false;
            d.style.display = 'none';
        } else {
            div_visible = true;
            d.style.display = 'block';
        }
    }
}

function main() {
    blink_text('Magic!'); 
    sum_5_numbers_async();
}