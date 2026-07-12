document.addEventListener("DOMContentLoaded",function(){

console.log("Credit Card Prediction System Loaded");

});

function validatePrediction(){

let income=document.getElementsByName("income")[0].value;

if(income<=0){

alert("Income must be greater than zero.");

return false;

}

return true;

}

function confirmLogout(){

return confirm("Do you really want to logout?");

}

function loading(){

document.getElementById("loader").style.display="block";

}

function welcome(){

console.log("Welcome to Credit Card Approval Prediction");

}