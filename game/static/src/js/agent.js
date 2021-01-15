
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
if (amount>wallet2.value){
alert("Sorry!!, You don't have that much amount in your wallet")
return false
} else
{
return true;
}
}
if(wallet){
if (amount>wallet.value){
alert("Sorry!!, You don't have that much amount in your wallet")
return false
} else
{
return true;
}
}
}