(function($) {
    'use strict';
    var $window = $(window);
    $window.on('resizeEnd', function() {
        $(".full_height").height($window.height());
    });
    $window.on('resize', function() {
        if (this.resizeTO) clearTimeout(this.resizeTO);
        this.resizeTO = setTimeout(function() {
            $(this).trigger('resizeEnd');
        }, 300);
    }).trigger("resize");

    if ($.fn.owlCarousel) {
        $('.you_make_like_slider').owlCarousel({
            items: 3,
            margin: 30,
            loop: true,
            nav: false,
            dots: true,
            autoplay: true,
            autoplayTimeout: 7000,
            smartSpeed: 1000,
            responsive: {
                0: {
                    items: 1
                },
                576: {
                    items: 2
                },
                768: {
                    items: 3
                }
            }
        });
    }

    $("[data-delay]").each(function() {
        var anim_del = $(this).data('delay');
        $(this).css('animation-delay', anim_del);
    });
    $("[data-duration]").each(function() {
        var anim_dur = $(this).data('duration');
        $(this).css('animation-duration', anim_dur);
    });

    if ($.fn.imagesLoaded) {
        $('.tailored-new-arrivals').imagesLoaded(function() {
            var $grid = $('.tailored-new-arrivals').isotope({
                itemSelector: '.single_gallery_item',
                percentPosition: true,
                masonry: {
                    columnWidth: '.single_gallery_item'
                }
            });
        });
    }
    $('#sideMenuBtn').on('click', function() {
        $('#wrapper').toggleClass('tailored-side-menu-open');
    })
    $('#sideMenuClose').on('click', function() {
        $('#wrapper').removeClass('tailored-side-menu-open');
    })
    if ($.fn.magnificPopup) {
        $('.gallery_img').magnificPopup({
            type: 'image',
            gallery: {
                enabled: true
            }
        });
    }
    if ($.fn.scrollUp) {
        $.scrollUp({
            scrollSpeed: 1000,
            easingType: 'easeInOutQuart',
            scrollText: '<i class="ti-angle-up" aria-hidden="true"></i>'
        });
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
            var  items, i, priceValue, price, num;

         
          items = document.getElementsByClassName("item");
          
          // Loop through all table rows, and hide those who don't match the search query
          for (i = 0; i < items.length; i++) {
            price = items[i].getElementsByClassName("product-price")[0];

            if (price) {
             
                priceValue=price.innerText;
                num=parseInt(price.innerText, 10);
                
              if (num>ui.values[0] && num<ui.values[1]  ){
              
                items[i].style.display = "";
              } else {

                items[i].style.display = "none";
              }
            } 
          }
            }

        });
    })
    $("a[href='#']").on('click', function($) {
        $.preventDefault();
    });
    if ($window.width() > 767) {
        new WOW().init();
    }
})(jQuery);
