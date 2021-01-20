document.addEventListener("DOMContentLoaded", function(e){
    var body = document.querySelector("body");
    var section = document.querySelector("sec");
    var articleLotto = document.querySelector(".lotto");
    var articleBalls = document.querySelector(".balls");
    var numbers = [];
    var balls = document.getElementsByClassName("ball");
    var drawnNums = [];
    var chosenByMachine = [];
    function createNumberBoard(number){
    	console.log("I work");
        var board = document.createElement("div");
        board.classList.add("boards");
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
    createNumberBoard(100);

    var board = document.querySelector(".boards");
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
            var first = document.getElementById("l1").innerHTML
            $('#l11').val(first);
            if(drawnNums.length=== 1){
                //boardEls.forEach( boardEl => boardEl.removeAttribute("data-number"));

                //boardEls.forEach(boardEl => boardEl.addEventListener("click", makeAlert));
                for ( var i = 0; i<boardEls.length; i++){
                	boardEls[i].removeAttribute("data-number");
                	boardEls[i].addEventListener("click", makeAlert);
                }
                var startDraw = document.querySelector(".startDraw");
                if(startDraw === null){ // you have to prevent creating the button if it is already there!
//                    createButtonForMachineDraw();
                } else {
                    return;
                }


            }

        }

        return drawnNums;

    }
    drawNumbers();

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
                var resultsBoard = document.createElement("article");
                section.appendChild(resultsBoard);
                var paragraph = document.createElement("p");
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
//        	makeComebackBtn();
//        	document.querySelector(".resultsBoard").classList.remove("invisible"); //well, you cannot acces this outside the code
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
