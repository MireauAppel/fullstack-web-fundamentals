"use strict";

document.addEventListener('DOMContentLoaded', bet_for_toffees);


function bet_for_toffees() {

  /* 
    red, blue, gains, p and below are declared
    in the same scope as the functions
    gain_toffee, lose_toffee and initiate_new_bet, 
    As a consequence, these const will be available
    as global variables within these function
    definitions and modification of the variable
    content in one function will be visible in
    the others. Also changes to n in initiate
    bet will change it's value in the 
    event listeners appropriately.
  */ 
  const red = document.querySelector('#red');
  const blue = document.querySelector('#blue');
  const gains = document.querySelector('#gains');
  const p = Math.random();
  console.log(p);

  let n;

  initiate_new_bet();

  red.addEventListener('click', (event) => {
    if (n <= p) gain_toffee(gains);
    else lose_toffee(gains);
  });
  blue.addEventListener('click', (event) => {
    if (n > p) gain_toffee(gains);
    else lose_toffee(gains);
  });


  function initiate_new_bet() { 
    n = Math.random();
    console.log(n);
  }

  function gain_toffee() {
    let gain, _;
    [gain, _] = gains.innerText.split(" ")
    gains.innerText = (parseInt(gain)+1) + " caramels";
    initiate_bet();
  }

  function lose_toffee() {
    let gain, _;
    [gain, _] = gains.innerText.split(" ")
    gains.innerText = (parseInt(gain)-1) + " caramels";
    initiate_bet();
  }
}
