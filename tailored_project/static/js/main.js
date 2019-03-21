
	var search={};
	search.size=null;
	search.sect=null;
	search.cat=null;


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
		} else if ($(input).attr('type') == 'password'){
			if($('input').val() != $('#id_password2').val()) {
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
	

<<<<<<< HEAD
	});

	$("#page2").click(function(){
		var thisURL=(window.location.href).replace("http://127.0.0.1:8000","").replace("3/","");
		window.location.href = thisURL+'2/';
	});

	$("#page3").click(function(){
		var thisURL=(window.location.href).replace("http://127.0.0.1:8000","").replace("2/","").replace("3/","");
		window.location.href = thisURL;
	});
	
=======

>>>>>>> 16cf8abe12bdbad731ae5a0c0e3c92dff96fd332
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
		  
		  var  items, td, i, sizeValue, size, category, section;
		  if(selected.localeCompare(search.size)==0){
		  	search.size=null;
		  	if(search.cat==null || search.sect==null){
		  		showAll();
		  	}else{
		  		  filterByCategories(search.cat, search.sect);
		  	}
		
		  }else{
		  items = document.getElementsByClassName("item");
		  // Loop through all table rows, and hide those who don't match the search query
		  for (i = 0; i < items.length; i++) {
			size = items[i].getElementsByClassName("size")[0];
			if (size) {
			 
				sizeValue=size.innerText;
				if(search.cat==null || search.sect==null){
					if (sizeValue.localeCompare(selected)==0 ){
							
							items[i].style.display = "";

				  	} else {

							items[i].style.display = "none";
			  }
				}else{
					category=items[i].getElementsByClassName("category")[0].innerText;
					section=items[i].getElementsByClassName("section")[0].innerText;
					if (sizeValue.localeCompare(selected)==0 &&section.localeCompare(search.sect)==0 && category.localeCompare(search.cat)==0){
					  	
						items[i].style.display = "";
					  } else {

						items[i].style.display = "none";
					  }
				}
			} 
		  }
		  search.size=selected;
		}
}
	

 $('#menu-content2').click(function(){
	  //  var ps =document.getElementsByTagName("p");
	   var items= document.getElementsByClassName("cat");
	   for (var i = 0; i<items.length; i++) {

		   $("#"+items[i].id).click({"category":items[i],"section": items[i].parentNode.parentNode },function(event){
			

			filterByCategories(event.data['category'].innerText, event.data["section"].id);
		   });
	   }

 });
	function filterByCategories(category, section) {
		  // Declare variables
		  var sec, items,  i, catValue,secValue ,cat ,size;


		  items = document.getElementsByClassName("item");

		  // Loop through all table rows, and hide those who don't match the search query
		  for (i = 0; i < items.length; i++) {

			cat = items[i].getElementsByClassName("category")[0];
			sec = items[i].getElementsByClassName("section")[0];
			if (cat&&sec) {
			  catValue =cat.innerText;
			  secValue =sec.innerText;
			  if(search.size==null){
				if (catValue.localeCompare(category)==0 && secValue.localeCompare(section)==0 ){
					items[i].style.display = "";
			  } else {
					items[i].style.display = "none";
			  }

			  }else{
			  	size = items[i].getElementsByClassName("size")[0].innerText;
			  if (catValue.localeCompare(category)==0 && secValue.localeCompare(section)==0 && size.localeCompare(search.size)==0){
				items[i].style.display = "";
			  } else {
				items[i].style.display = "none";
			  }

			  }
			  
			} 
		  }
		  search.cat=category;
		  search.sect=section;
}
	function showAll(){
				 // Declare variables
		  var sec, items,  i, catValue,secValue ,cat ,size, category;


		  items = document.getElementsByClassName("item");

		  // Loop through all table rows, and hide those who don't match the search query
		  for (i = 0; i < items.length; i++) {
	
			
					items[i].style.display = "";

							}
						}
	function filterByPrice(min, max){
		 var  items, i, priceValue, price, num, size, category, temp;

                items = document.getElementsByClassName("item");
             	  
                for (var i=0; i<items.length; i++) {
                    if(search.cat&&search.sect &&(!search.size)){
                        category=items[i].getElementsByClassName("category")[0].innerText;
                        category=items[i].getElementsByClassName("section")[0].innerText;
                        if(category.localeCompare(search.cat)!=0 || section.localeCompare(search.sect)!=0){
                            delete items[i];
                    
                    }   
                }else
                if(search.size && !search.cat){
                        size = items[i].getElementsByClassName("size")[0].innerText;
                        if(size.localeCompare(search.size)!=0){
                            delete items[i];
                    }
                    }else
                
                if(search.cat&&search.sect &&search.size){
                        size = items[i].getElementsByClassName("size")[0].innerText;
                        category=items[i].getElementsByClassName("category")[0].innerText;
                        category=items[i].getElementsByClassName("section")[0].innerText;
                        if(category.localeCompare(search.cat)!=0 
                            || section.localeCompare(search.sect)!=0 || size.localeCompare(search.size!=0)) {
                            delete items[i];
                    
                    }   
                }
                }
        
          // Loop through all table rows, and hide those who don't match the price bracket
                for (i = 0; i < items.length; i++) {
                	if(items[i]){
                    price = items[i].getElementsByClassName("product-price")[0];
                    if (price ) {
                        num=parseInt(price.innerText, 10);          
                                if (num>min && num<max  ){
                                    items[i].style.display = "";
                                 } else {

                                    items[i].style.display = "none";
                                  }
                            }
                      }
          }
          // Loop through all table rows, and hide those who don't match the search query
          
            
	}

    $('.slider-range-price').each(function() {
        var min = jQuery(this).data('min');
        var max = jQuery(this).data('max');
        var unit = jQuery(this).data('unit');
        var value_min = jQuery(this).data('value-min');
        var value_max = jQuery(this).data('value-max');
        var label_result = jQuery(this).data('label-result');
        var t = $(this);
        $(this).slider({

            range: true,
            min: min,
            max: max,
            values: [value_min, value_max],
            slide: function(event, ui) {
                var result = label_result + " " + unit + ui.values[0] + ' - ' + unit + ui.values[1];
                console.log(t);
                t.closest('.slider-range').find('.range-price').html(result);
                filterByPrice(ui.values[0], ui.values[1])
          }     

        });
    });
			


})(jQuery);
