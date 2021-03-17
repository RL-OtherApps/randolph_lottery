function myFunction(data) {
  document.getElementById("demo").innerHTML = "Hello World";
  var x = document.getElementsByClassName("total")[0];
  var num= x.innerHTML
  $.ajax({
    type: 'POST',
    url: '/pay_amount_via_moncash',
    dataType: 'json',
    data : {},
    }).done(function(data){
        load_year=$('#age_year').empty();
        load_year_data='<option value="" selected="selected">YEAR</option>';

        load_month=$('#age_month').empty();
        load_month_data='<option value="" selected="selected">MONTH</option>';

        load_days=$('#age_day').empty();
        load_days_data='<option value="" selected="selected">DAYS</option>';
})
}