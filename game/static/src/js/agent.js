
function yesnoCheck() {
if (document.getElementById('yesCheck').checked) {
document.getElementById('ifYes').style.display = 'block';
document.getElementById('ifno').style.display = 'none';
}
else
{
document.getElementById('ifYes').style.display = 'none';
 document.getElementById('ifno').style.display = 'block';
}
}

function yesnoWallet() {
if (document.getElementById('yesWallet').checked) {
document.getElementById('ifYes').style.display = 'block';
document.getElementById('ifno').style.display = 'none';
}
else
{
document.getElementById('ifYes').style.display = 'none';
 document.getElementById('ifno').style.display = 'block';
}
}
function walletValidation()
{
amount = document.getElementById('amount').value;
wallet = document.getElementById('amt')
wallet2 = document.getElementById('amt2')
if(wallet2){
if (amount>wallet2.value || ((document.getElementById("amount").value) < 0 || (document.getElementById("amounts").value) < 0))
{
    if ((document.getElementById("amount").value) < 0 || (document.getElementById("amounts").value) < 0)
        {
        alert("You Cannot Enter Negative Amount")
        return false
        }
    else{
    alert("Sorry!!, You don't have that much amount in your wallet")
    return false
    }

} else
{
return true;
}
}
if(wallet){
if (amount>wallet.value  || ((document.getElementById("amount").value) < 0 || (document.getElementById("amounts").value) < 0)){
    if ((document.getElementById("amount").value) < 0 || (document.getElementById("amounts").value) < 0)
        {
        alert("You Cannot Enter Negative Amount")
        return false
        }
    else{
    alert("Sorry!!, You don't have that much amount in your wallet")
    return false
    }

} else
{
return true;
}
}
}

//function errorMessage() {
//        var error = document.getElementById("error")
//        if ((document.getElementById("amount").value) < 0 || (document.getElementById("amounts").value) < 0)
//        {
//
//            // Changing content and color of content
//            error.textContent = "Please enter a valid Number"
//            error.style.color = "red"
//        } else {
//            error.textContent = ""
//        }
//    }