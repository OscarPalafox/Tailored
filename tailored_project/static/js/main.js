(function($) {
    "use strict";
    var input = $('.validate-input .input100');
    $('.validate-form').on('submit', function() {
        var check = true;
        for (var i = 0; i < input.length; i++) {
            if (validate(input[i]) == false) {
                showValidate(input[i]);
                check = false;
            }
        }
        return check;
    });
    $('.validate-form .input100').each(function() {
        $(this).focus(function() {
            hideValidate(this);
        });
    });

    function validate(input) {
        if ($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if ($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        } else {
            if ($(input).val().trim() == '') {
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).removeClass('alert-validate');
    }
    $("#S").click(function(){
        filterBySize("S");
    });
    $("#L").click(function(){
        filterBySize("L");
    });
    $("#XL").click(function(){
        filterBySize("XL");
    });
    $("#XS").click(function(){
        filterBySize("XS");
    });
    $("#XXL").click(function(){
        filterBySize("XXL");
    });
    $("#M").click(function(){
        filterBySize("M");
    });

    function filterBySize(selected) {
          // Declare variables 
          
          var  items, td, i, sizeValue, size;


          items = document.getElementsByClassName("item");
          // Loop through all table rows, and hide those who don't match the search query
          for (i = 0; i < items.length; i++) {
            size = items[i].getElementsByClassName("size")[0];
            if (size) {
             
                sizeValue=size.innerText;
              if (sizeValue.localeCompare(selected)==0 ){
              
                items[i].style.display = "";
              } else {

                items[i].style.display = "none";
              }
            } 
          }
          
}

    $('.slider-range-price').each(function(){
        $("#slider").click(function(){
         var min = jQuery(this).data('min');
         var max = jQuery(this).data('max');
         slide: function(event, ui) {
         filterByPrice(ui.values[0], ui.values[1]);
                 }
         });
    });
    function filterByCategories(event) {
          // Declare variables 
          window.print("Hello There!");
          var div, item, td, i, txtValue;

          div = document.getElementById("results");
          items = div.getElementsByTagName("item");

          // Loop through all table rows, and hide those who don't match the search query
          for (i = 0; i < items.length; i++) {
            size = items[i].getElementById("category");
            if (td) {
              txtValue = size.textContent || size.innerText;
              if (txtValue==event.data.category) {
                item[i].style.display = "";
              } else {
                item[i].style.display = "none";
              }
            } 
          }
}
    function filterByPrice(min, max) {
          // Declare variables 
         var  items, i, priceValue, price, num;

         alert(max)
          items = document.getElementsByClassName("item");
          
          // Loop through all table rows, and hide those who don't match the search query
          for (i = 0; i < items.length; i++) {
            price = items[i].getElementsByClassName("product-price")[0];

            if (price) {
             
                priceValue=price.innerText;
                num=parseInt(price.innerText, 10);
                
              if (num>min && num<max  ){
              
                items[i].style.display = "";
              } else {

                items[i].style.display = "none";
              }
            } 
          }
}
})(jQuery);
