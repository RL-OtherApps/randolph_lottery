document.addEventListener("DOMContentLoaded", function(e){
    var body = document.querySelector("body");
    var section = document.querySelector("sections");
    var articleLotto = document.querySelector(".lotto");
    var articleBalls = document.querySelector(".balls");
    var numbers = [];
    var balls = document.getElementsByClassName("ball");
    var drawnNums = [];
    var chosenByMachine = [];
    function createNumberBoard(number){
    	console.log("I work");
        var board = document.createElement("div");
        board.classList.add("board");
        articleLotto.appendChild(board);
        for( var i = 0; i<number; i ++){
            var boardEl = document.createElement("button");
            boardEl.classList.add("boardEl");
            board.appendChild(boardEl);
        }
        var boardEls = document.getElementsByClassName("boardEl");
        for( var i =0; i<boardEls.length; i++){
            boardEls[i].setAttribute("data-number", i+1);
            var dataNumber = boardEls[i].getAttribute("data-number");
            var number = parseInt(dataNumber, 10);
            numbers.push(number);
            boardEls[i].textContent = number;
        }
    }
    createNumberBoard(49);

    var board = document.querySelector(".board");
    var boardEls = document.querySelectorAll(".boardEl");
    var counter=0
    function drawNumbers(){
        //boardEls.forEach(boardEl => boardEl.addEventListener("click", selectNums));
        for (var i = 0; i<boardEls.length; i++){
        	boardEls[i].addEventListener("click", selectNums);
        }
        function selectNums(){
            var number = parseInt(this.dataset.number, 10);
            if(this.hasAttribute("data-number")){
                drawnNums.push(number);
                counter=counter+1
                this.removeAttribute("data-number");
                this.classList.add("crossedOut");
            }
            if(counter==1){
             document.getElementById("l1").innerHTML = number;
            }
            if(counter==2){
             document.getElementById("l2").innerHTML = number;
            }
            if(counter==3){
             document.getElementById("l3").innerHTML = number;
            }
            if(counter==4){
             document.getElementById("l4").innerHTML = number;
            }
            if(counter==5){
             document.getElementById("l5").innerHTML = number;
            }
            if(counter==6){
             document.getElementById("l6").innerHTML = number;
            }

            if(drawnNums.length=== 6){
                //boardEls.forEach( boardEl => boardEl.removeAttribute("data-number"));

                //boardEls.forEach(boardEl => boardEl.addEventListener("click", makeAlert));
                for ( var i = 0; i<boardEls.length; i++){
                	boardEls[i].removeAttribute("data-number");
                	boardEls[i].addEventListener("click", makeAlert);
                }
                var startDraw = document.querySelector(".startDraw");
                if(startDraw === null){ // you have to prevent creating the button if it is already there!
                    createButtonForMachineDraw();
                } else {
                    return;
                }


            }

        }

        return drawnNums;

    }
    drawNumbers();

//    function submitNumbers(random_numbers){
//        var first = document.getElementById("l1").innerHTML
//        $.ajax({
//        type: 'POST',
//        url: '/save_numbers',
//        dataType: 'json',
//        data : {'l1': random_numbers},
//        });
//    }

    function makeAlert() {
    	var alertBox = document.createElement("div");
    	board.appendChild(alertBox);
    	alertBox.classList.add("alertBox");
    	alertBox.textContent = "you already chose 6!";

    	setTimeout(function() {
    		alertBox.parentNode.removeChild(alertBox);
    	}, 1500);

    }

    function machineDraw(){
        for( var i =0; i<6; i++){
            var idx = Math.floor(Math.random() * numbers.length)
            chosenByMachine.push(numbers[idx]);
            /*a very important line of code which prevents machine from drawing the same number again
             */
            numbers.splice(idx,1);
            console.log(numbers)
            /*this line of code allows to check if numbers are taken out*/
        }
        var btnToRemove = document.querySelector(".startDraw");

        btnToRemove.classList.add("invisible");
        /* why not remove it entirely? because it might then be accidentally created if for some reason you happen to try to click on board!!! and you may do that*/
        return chosenByMachine;

    }
    //machineDraw();

    function createButtonForMachineDraw(){
    	var startDraw = document.createElement("button");
    	startDraw.classList.add("startDraw");
    	section.appendChild(startDraw);
    	startDraw.textContent ="release the balls";
    	startDraw.addEventListener("click", machineDraw);
    	startDraw.addEventListener("click", compareArrays);

    }

    function compareArrays(){
        for( var i =0; i<balls.length; i++) {
            balls[i].textContent = chosenByMachine[i];
            (function() {
            	var j = i;
            	var f = function(){
            		balls[j].classList.remove("invisible");
            	}
            	setTimeout(f, 1000*(j+1));
            })();
        }
        var common =[];
        var arr1 = chosenByMachine;
        var arr2 = drawnNums;
            for(var i = 0; i<arr1.length; i++){
                for(var j= 0; j<arr2.length; j++){
                    if(arr1[i]===arr2[j]){
                        common.push(arr1[i]);
                    }
                }
            }
            console.log(arr1, arr2, common); /* you can monitor your arrays in console*/
            function generateResult(){
                var first = document.getElementById("l1").innerHTML
                var second = document.getElementById("l2").innerHTML
                var third = document.getElementById("l3").innerHTML
                var fourth = document.getElementById("l4").innerHTML
                var fifth = document.getElementById("l5").innerHTML
                var sixth = document.getElementById("l6").innerHTML
                     $.ajax({
                        type: 'POST',
                        url: '/save_numbers',
                        dataType: 'json',
                        data : {'l1': first,'l2': second,'l3': third,'l4': fourth,'l5': fifth,'l6': sixth,},
                        });
                var resultsBoard = document.createElement("article");
                section.appendChild(resultsBoard);
                var paragraph = document.createElement("p");
                resultsBoard.appendChild(paragraph);
                resultsBoard.classList.add("resultsBoard");
                resultsBoard.classList.add("invisible");
                if( common.length===0){
                    paragraph.textContent ="Oh, dear!  " + common.length + " balls and zero cash ";
                } else if( common.length >0 && common.length< 3){
                    paragraph.textContent ="Outta luck, only " + common.length + " , still no cash ";
                } else if(common.length ===3) {
                    paragraph.textContent ="Not bad, " + common.length + " , here's your twenty ";
                } else if(common.length ===4){
                    paragraph.textContent ="Not bad, " + common.length + " , here's your hundred ";
                } else if( common.length ===5){
                    paragraph.textContent ="Not bad, " + common.length + " , here's your thousand ";
                }
                else if(common.length===6){
                    paragraph.textContent ="A true winner " + common.length + " here's your million";
                }
            }
        setTimeout(function() {
        	makeComebackBtn();
        	document.querySelector(".resultsBoard").classList.remove("invisible"); //well, you cannot acces this outside the code
        }, 8000);
        generateResult();
    }

    function makeComebackBtn(){
        var comebackBtn = document.createElement("a");
        comebackBtn.classList.add("comebackBtn");
        section.appendChild(comebackBtn);
        comebackBtn.textContent ="again"
        comebackBtn.setAttribute("href", "https://ewagrela.github.io/lottoIE/");
    }


})

///*jslint devel: true*/
///*eslint-env browser*/
//
//function playGame() {
//    "use strict";
//
//    // Create the random numbers for the powerball
//    var num1 = Math.floor(Math.random() * 101);
//    var num2 = Math.floor(Math.random() * 101);
//    var num3 = Math.floor(Math.random() * 101);
//    var num4 = Math.floor(Math.random() * 101);
//    var num5 = Math.floor(Math.random() * 101);
//    var num6 = Math.floor(Math.random() * 101);
//    var num7 = Math.floor(Math.random() * 101);
//
//    // Users guess
//    var userNum1 = parseInt(document.getElementById("guess1").value);
//    var userNum2 = parseInt(document.getElementById("guess2").value);
//    var userNum3 = parseInt(document.getElementById("guess3").value);
//    var userNum4 = parseInt(document.getElementById("guess4").value);
//    var userNum5 = parseInt(document.getElementById("guess5").value);
//    var userNum6 = parseInt(document.getElementById("guess6").value);
//    var userNum7 = parseInt(document.getElementById("guess7").value);
//
//    // Output each random number
//    document.getElementById("test1").innerHTML = num1;
//    document.getElementById("test2").innerHTML = num2;
//    document.getElementById("test3").innerHTML = num3;
//    document.getElementById("test4").innerHTML = num4;
//    document.getElementById("test5").innerHTML = num5;
//    document.getElementById("test6").innerHTML = num6;
//    document.getElementById("test7").innerHTML = num7;
//
//    // Set up several conditions to see if any numbers match
//    if (num1 === userNum1 || num2 === userNum1) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num3 === userNum1 || num4 === userNum1) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num5 === userNum1 || num6 === userNum1) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num7 === userNum1) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num1 === userNum2 || num2 === userNum2) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num3 === userNum2 || num4 === userNum2) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num5 === userNum2 || num6 === userNum2) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num7 === userNum2) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num1 === userNum3 || num2 === userNum3) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num3 === userNum3 || num4 === userNum3) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num5 === userNum3 || num6 === userNum3) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num7 === userNum3) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num1 === userNum4 || num2 === userNum4) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num3 === userNum4 || num4 === userNum4) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num5 === userNum4 || num6 === userNum4) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num7 === userNum4) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num1 === userNum5 || num2 === userNum5) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num3 === userNum5 || num4 === userNum5) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num5 === userNum5 || num6 === userNum5) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num7 === userNum5) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num1 === userNum6 || num2 === userNum6) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num3 === userNum6 || num4 === userNum6) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num5 === userNum6 || num6 === userNum6) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num7 === userNum6) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num1 === userNum7 || num2 === userNum7) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num3 === userNum7 || num4 === userNum7) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num5 === userNum7 || num6 === userNum7) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (num7 === userNum7) {
//        document.getElementById("winner").innerHTML = "You got one!!";
//    } else if (userNum1 === num1 && userNum2 === num2 && userNum3 === num3 && userNum4 === num4 && userNum5 === num5 && userNum6 === num6 && userNum7 === num7) {
//        document.getElementById("winner").innerHTML = "YOU WIN!!";
//    } else {
//        document.getElementById("winner").innerHTML = "You Lose!!";
//    }
//
//}
//
//playGame();