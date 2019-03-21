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


    $("a[href='#']").on('click', function($) {
        $.preventDefault();
    });
    if ($window.width() > 767) {
        new WOW().init();
    }
})(jQuery);
