
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