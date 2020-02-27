// -----------------------------

//   Custom js
/* =================== */
/*




*/
// -----------------------------


(function($) {
    "use strict";




    /*---------------------
    preloader
    --------------------- */

    $(window).on('load', function() {

        if ($('.wow').length > 0) {
            var wowSel = 'wow';
            var wow = new WOW({
                boxClass: wowSel,
                animateClass: 'animated',
                offset: 0,
                mobile: true,
                live: true,
                callback: function(box) {

                },
                scrollContainer: null
            });
            wow.init();
        }
        $('#preloader').fadeOut('slow', function() {
            $(this).remove();
        });
    });


    /*---------------------
    Wow
    --------------------- */
    // if ($('.wow').length > 0) {
    //     var wowSel = 'wow';

    //     var wow = new WOW({
    //         boxClass: wowSel,
    //         animateClass: 'animated',
    //         offset: 0,
    //         mobile: true,
    //         live: true,
    //         callback: function(box) {

    //         },
    //         scrollContainer: null
    //     });
    //     wow.init();
    // }


        /*---------------------
     ## Wordpress Friendly Menu
     --------------------- */
     $(window).on('resize', function () {
        var wWidth = $(this).width();

        var selectedMenu = $('.s-menu'); // .s-menu  nav  ul li a (this is the structur)
        if (wWidth > 991) {
            selectedMenu.addClass('menu-activated');
            $('.menu-activated >nav >ul >li ul').addClass('sub-menu');
            $('.menu-activated >nav >ul >li ul li:has(ul)').addClass('menu-item-has-children');
            $('.menu-activated >nav >ul >li:has(ul)').addClass('menu-item-has-children has-submenu');
            $('.prc-anim').addClass('prc-area');

        } else {
            $('.menu-activated >nav >ul >li ul').removeClass('sub-menu');
            $('.menu-activated >nav >ul li:has(ul)').removeClass('menu-item-has-children');
            $('.menu-activated >nav >ul >li:has(ul)').removeClass('menu-item-has-children has-submenu');
            selectedMenu.removeClass('menu-activated');
            $('.prc-anim').removeClass('prc-area');

            $('.feature-item-area .left-feature').removeClass('left-feature');
        }

    }).resize();


    // SerchNav Btn
    // $(window).on('resize', function(){
    //     if( $('body').width() < 1023 ) {
    //         alert('hello');
    //     }
    // });

    /*---------------------
    ## SlickNav menu Activation
    --------------------- */
    $('ul#mobile_menu').slicknav({
        'appendTo': '.responsive-menu-wrap',
        'label': 'MENU',
    });

    (function () {
        $(".mobile-menu").append('<div class="mobile-menu-logo"></div>');
        $(".mobile-menu ul li.mid-logo").remove();
        $(".mobile-menu-logo").append($(".logo").clone());


    })();



    /*-----------------
    sticky
    -----------------*/
    $(window).on('scroll', function() {
        if ($(window).scrollTop() > 85) {
            $('header').addClass('navbar-fixed-top');
        } else {
            $('header').removeClass('navbar-fixed-top');
        }
    });

    /*-----------------
    scroll-up
    -----------------*/
    $.scrollUp({
        scrollText: '<i class="fa fa-arrow-up" aria-hidden="true"></i>',
        easingType: 'linear',
        scrollSpeed: 1500,
        animation: 'fade'
    });

    /*------------------------------
         counter
    ------------------------------ */
    $('.counter-up').counterUp();


    /*---------------------
    smooth scroll
    --------------------- */
    $('.smoothscroll').on('click', function(e) {
        e.preventDefault();
        var target = this.hash;

        $('html, body').stop().animate({
            'scrollTop': $(target).offset().top - 80
        }, 1200);
    });


    /*---------------------
    countdown
    --------------------- */
    $('[data-countdown]').each(function() {
        var $this = $(this),
            finalDate = $(this).data('countdown');
        $this.countdown(finalDate, function(event) {
            $this.html(event.strftime('<span class="cdown days"><span class="time-count">%-D</span> <p>Days</p></span> <span class="cdown hour"><span class="time-count">%-H</span> <p>Hour</p></span> <span class="cdown minutes"><span class="time-count">%M</span> <p>Min</p></span> <span class="cdown second"> <span><span class="time-count">%S</span> <p>Sec</p></span>'));
        });
    });




    // Testimonial V1 Carousel
    $(window).on('load', function() {

        var sync1 = $("#sync1");
        var sync2 = $("#sync2");
        var slidesPerPage = 4; //globaly define number of elements per page
        var syncedSecondary = true;

        sync1.owlCarousel({
          items : 1,
          slideSpeed : 2000,
          nav: true,
          autoplay: true,
          dots: true,
          loop: true,
          responsiveRefreshRate : 200,
          navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
        }).on('changed.owl.carousel', syncPosition);

        sync2
          .on('initialized.owl.carousel', function () {
            sync2.find(".owl-item").eq(0).addClass("current");
          })
          .owlCarousel({
          items : slidesPerPage,
          dots: true,
          nav: true,
          smartSpeed: 200,
          slideSpeed : 500,
          slideBy: slidesPerPage, //alternatively you can slide by 1, this way the active slide will stick to the first item in the second carousel
          responsiveRefreshRate : 100
        }).on('changed.owl.carousel', syncPosition2);

        function syncPosition(el) {
          //if you set loop to false, you have to restore this next line
          //var current = el.item.index;

          //if you disable loop you have to comment this block
          var count = el.item.count-1;
          var current = Math.round(el.item.index - (el.item.count/2) - .5);

          if(current < 0) {
            current = count;
          }
          if(current > count) {
            current = 0;
          }

          //end block

          sync2
            .find(".owl-item")
            .removeClass("current")
            .eq(current)
            .addClass("current");
          var onscreen = sync2.find('.owl-item.active').length - 1;
          var start = sync2.find('.owl-item.active').first().index();
          var end = sync2.find('.owl-item.active').last().index();

          if (current > end) {
            sync2.data('owl.carousel').to(current, 100, true);
          }
          if (current < start) {
            sync2.data('owl.carousel').to(current - onscreen, 100, true);
          }
        }

        function syncPosition2(el) {
          if(syncedSecondary) {
            var number = el.item.index;
            sync1.data('owl.carousel').to(number, 100, true);
          }
        }

        sync2.on("click", ".owl-item", function(e){
          e.preventDefault();
          var number = $(this).index();
          sync1.data('owl.carousel').to(number, 300, true);
        });
      });




    // Testimonial V2 Carousel
    function testimonial2_carousel() {
        var owl = $(".testimonial2-carousel");
        owl.owlCarousel({
            loop: true,
            margin: 0,
            responsiveClass: true,
            navigation: true,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            nav: true,
            items: 5,
            smartSpeed: 2000,
            dots: true,
            autoplay: false,
            autoplayTimeout: 5000,
            center: false,
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                760: {
                    items: 2
                }
            }
        });
    }
    testimonial2_carousel();

    // Testimonial V3 Carousel
    function testimonial3_carousel() {
        var owl = $(".testimonial3-carousel");
        owl.owlCarousel({
            loop: true,
            margin: 0,
            responsiveClass: true,
            navigation: true,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            nav: true,
            items: 5,
            smartSpeed: 2000,
            dots: true,
            autoplay: false,
            autoplayTimeout: 5000,
            center: false,
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                760: {
                    items: 2
                }
            }
        });
    }
    testimonial3_carousel();

    // Hero 2 Carousel
    function hero2_carousel() {
        var owl = $(".hero2-carousel");
        owl.owlCarousel({
            loop: true,
            margin: 0,
            responsiveClass: true,
            navigation: true,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            nav: true,
            items: 5,
            smartSpeed: 2000,
            dots: true,
            autoplay: false,
            autoplayTimeout: 5000,
            center: true,
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                760: {
                    items: 1
                }
            }
        });
    }
    hero2_carousel();




    // Hero 5 Carousel
    function heroV5_carousel() {
        var owl = $(".heroV5-carousel");
        owl.owlCarousel({
            loop: true,
            margin: 0,
            responsiveClass: true,
            navigation: true,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            nav: true,
            items: 5,
            smartSpeed: 2000,
            dots: true,
            autoplay: false,
            autoplayTimeout: 5000,
            center: true,
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                760: {
                    items: 1
                }
            }
        });
    }
    heroV5_carousel();

    // Hero Carousel 3
    function heroV9_carousel() {
        var owl = $(".hero-fph3-carousel");
        owl.owlCarousel({
            loop: true,
            margin: 0,
            responsiveClass: true,
            navigation: true,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            nav: true,
            items: 5,
            smartSpeed: 2000,
            dots: true,
            autoplay: true,
            autoplayTimeout: 5000,
            center: true,
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                760: {
                    items: 1
                }
            }
        });
        owl.on('mousewheel', '.owl-stage', function (e) {
            if (e.deltaY>0) {
                owl.trigger('prev.owl');
            } else {
                owl.trigger('next.owl');
            }
            e.preventDefault();
        });
        $(window).on('keyup', function (event) {
            // handle cursor keys
            if (event.keyCode == 37) {
                // go left
                owl.trigger('prev.owl');

            } else if (event.keyCode == 39) {
               // go right
               owl.trigger('next.owl');
            }

        });


    //here we need hide because method show() doesn't work with css visible


    //all other is the same
    // owl.on('translated.owl.carousel', function( event ) {
    //     $( ".active .item .sfph-text" ).hide();
    //     $( ".active .item .sfph-text" ).addClass( "animated fadeInRight" );
    //     $(".active .item .sfph-text").show();
    // });



    }
    heroV9_carousel();

    // Service 2 Carousel
    function service2_carousel() {
        var owl = $(".service2-carousel");
        owl.owlCarousel({
            loop: true,
            margin: 0,
            responsiveClass: true,
            navigation: true,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            nav: true,
            items: 5,
            smartSpeed: 2000,
            dots: true,
            autoplay: false,
            autoplayTimeout: 5000,
            center: true,
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                760: {
                    items: 3
                }
            }
        });
    }
    service2_carousel();

    // Instagran Carousel
    function instagram_carousel() {
        var owl = $(".insta-carousel");
        owl.owlCarousel({
            loop: true,
            margin: 0,
            responsiveClass: true,
            navigation: true,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            nav: true,
            items: 5,
            smartSpeed: 2000,
            dots: true,
            autoplay: false,
            autoplayTimeout: 5000,
            center: false,
            responsive: {
                0: {
                    items: 2
                },
                480: {
                    items: 4
                },
                760: {
                    items: 8
                }
            }
        });
    }
    instagram_carousel();

    // Instagran Carousel
    function gallery_carousel() {
        var owl = $(".gallery-carousel");
        owl.owlCarousel({
            loop: true,
            margin: 0,
            responsiveClass: true,
            navigation: true,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            nav: true,
            items: 5,
            smartSpeed: 2000,
            dots: true,
            autoplay: false,
            autoplayTimeout: 5000,
            center: true,
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 2
                },
                760: {
                    items: 3
                }
            }
        });
    }
    gallery_carousel();


    // Hero 6 Carousel
    function hero6_carousel() {
        var owl = $(".hero6-carousel");
        owl.owlCarousel({
            loop: true,
            margin: 0,
            responsiveClass: true,
            navigation: true,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            nav: true,
            items: 5,
            smartSpeed: 2000,
            dots: false,
            autoplay: false,
            autoplayTimeout: 5000,
            center: false,
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 2
                },
                760: {
                    items: 4
                }
            }
        });
        owl.on('mousewheel', '.owl-stage', function (e) {
            if (e.deltaY>0) {
                owl.trigger('prev.owl');
            } else {
                owl.trigger('next.owl');
            }
            e.preventDefault();
        });
        $(window).on('keyup', function (event) {
            // handle cursor keys
            if (event.keyCode == 37) {
                // go left
                owl.trigger('prev.owl');

            } else if (event.keyCode == 39) {
               // go right
               owl.trigger('next.owl');
            }

        });

    }
    hero6_carousel();



    // Hero 13 Slider
    if ($(".hero_V13").length > 0) {
        $(window).on("load",function() {
            var bigimage = $(".hss-V13");
            var thumbs = $(".hss-V13thumbs");
            //var totalslides = 10;
            var syncedSecondary = true;

            bigimage
              .owlCarousel({
              items: 1,
              slideSpeed: 2000,
              nav: true,
              autoplay: true,
              dots: false,
              loop: true,
              responsiveRefreshRate: 200,
              navText: [
                '<i class="fa fa-arrow-left" aria-hidden="true"></i>',
                '<i class="fa fa-arrow-right" aria-hidden="true"></i>'
              ]
            })
              .on("changed.owl.carousel", syncPosition);

            thumbs
              .on("initialized.owl.carousel", function() {
              thumbs
                .find(".owl-item")
                .eq(0)
                .addClass("current");
            })
              .owlCarousel({
              items: 4,
              dots: true,
              nav: true,
              navText: [
                '<i class="fa fa-arrow-left" aria-hidden="true"></i>',
                '<i class="fa fa-arrow-right" aria-hidden="true"></i>'
              ],
              smartSpeed: 200,
              slideSpeed: 500,
              slideBy: 4,
              responsiveRefreshRate: 100
            })
              .on("changed.owl.carousel", syncPosition2);

            function syncPosition(el) {
              //if loop is set to false, then you have to uncomment the next line
              //var current = el.item.index;

              //to disable loop, comment this block
              var count = el.item.count - 1;
              var current = Math.round(el.item.index - el.item.count / 2 - 0.5);

              if (current < 0) {
                current = count;
              }
              if (current > count) {
                current = 0;
              }
              //to this
              thumbs
                .find(".owl-item")
                .removeClass("current")
                .eq(current)
                .addClass("current");
              var onscreen = thumbs.find(".owl-item.active").length - 1;
              var start = thumbs
              .find(".owl-item.active")
              .first()
              .index();
              var end = thumbs
              .find(".owl-item.active")
              .last()
              .index();

              if (current > end) {
                thumbs.data("owl.carousel").to(current, 100, true);
              }
              if (current < start) {
                thumbs.data("owl.carousel").to(current - onscreen, 100, true);
              }
            }

            function syncPosition2(el) {
              if (syncedSecondary) {
                var number = el.item.index;
                bigimage.data("owl.carousel").to(number, 100, true);
              }
            }

            thumbs.on("click", ".owl-item", function(e) {
              e.preventDefault();
              var number = $(this).index();
              bigimage.data("owl.carousel").to(number, 300, true);
            });
          });
    }





    // Hero Ripples
    if ($(".hero2-ripples").length > 0) {
        $('.hero2-ripples').ripples({
            dropRadius: 10,
            perturbance: 0.01,

        });
    }



    // Hero 19 Carousel
    function hero19_carousel() {
        var owl = $(".hero19-carousel");
        owl.owlCarousel({
            loop: true,
            margin: 0,
            responsiveClass: true,
            navigation: true,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            nav: true,
            items: 5,
            smartSpeed: 2000,
            dots: true,
            autoplay: false,
            autoplayTimeout: 5000,
            center: true,
            // animateOut: 'slideOutUp',
            // animateIn: 'slideInUp',
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                760: {
                    items: 1
                }
            }
        });
        owl.on('mousewheel', '.owl-stage', function (e) {
            if (e.deltaY>0) {
                owl.trigger('prev.owl');
            } else {
                owl.trigger('next.owl');
            }
            e.preventDefault();
        });
        $(window).on('keyup', function (event) {
            // handle cursor keys
            if (event.keyCode == 37) {
                // go left
                owl.trigger('prev.owl');

            } else if (event.keyCode == 39) {
               // go right
               owl.trigger('next.owl');
            }

        });
    }
    hero19_carousel();


    // Hero 20 Carousel
    function hero20_carousel() {
        var owl = $(".hero20-carousel");
        owl.owlCarousel({
            loop: true,
            margin: 0,
            responsiveClass: true,
            navigation: true,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            nav: true,
            items: 5,
            smartSpeed: 2000,
            dots: true,
            autoplay: false,
            autoplayTimeout: 5000,
            center: true,
            // animateOut: 'slideOutUp',
            // animateIn: 'slideInUp',
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                760: {
                    items: 1
                }
            }
        });
        owl.on('mousewheel', '.owl-stage', function (e) {
            if (e.deltaY>0) {
                owl.trigger('prev.owl');
            } else {
                owl.trigger('next.owl');
            }
            e.preventDefault();
        });
        $(window).on('keyup', function (event) {
            // handle cursor keys
            if (event.keyCode == 37) {
                // go left
                owl.trigger('prev.owl');

            } else if (event.keyCode == 39) {
               // go right
               owl.trigger('next.owl');
            }

        });
    }
    hero20_carousel();



     /*---------------------
    ## Skill Bar
    --------------------- */

    if ($(".profoSkill").length > 0) {
        $(".bar").each(function () {

            var $bar = $(this),
                $pct = $bar.find(".pct"),
                data = $bar.data("bar");

            setTimeout(function () {

                $bar
                    .animate({
                        "width": $pct.html()
                    }, data.speed || 2000, function () {

                        $pct.css({
                            "opacity": 1
                        });

                    });

            }, data.delay || 0);

        });
    }







    if ($("#ri-grid").length > 0) {
        $(function() {

            $( '#ri-grid' ).gridrotator( {
                rows		: 10,
                columns		: 8,
                animType	: 'fadeInOut',
                animSpeed	: 1000,
                interval	: 450,
                step		: 3,
                w1024		: {
                    rows	: 5,
                    columns	: 5
                },
                w768		: {
                    rows	: 5,
                    columns	: 5
                },
                w480		: {
                    rows	: 4,
                    columns	: 2
                }
            } );

        });
    }


    if ($("#ri-grid2").length > 0) {
        $(function() {

            $( '#ri-grid2' ).gridrotator( {
                rows		: 10,
                columns		: 8,
                animType	: 'fadeInOut',
                animSpeed	: 1000,
                interval	: 450,
                step		: 3,
                w1024		: {
                    rows	: 5,
                    columns	: 5
                },
                w768		: {
                    rows	: 5,
                    columns	: 5
                },
                w480		: {
                    rows	: 4,
                    columns	: 2
                }
            } );

        });
    }


  /*---------------------
    // Ajax Contact Form
    --------------------- */


    $('.cf-msg').hide();
    $('form#cf button#submit').on('click', function() {

        var firstName = $('#firstName').val();
        var phone = $('#phone').val();
        var email = $('#email').val();
        var subjectName = $('#subjectName').val();
        var msg = $('#msg').val();
        var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;

        if (!regex.test(email)) {
            alert('Please enter valid email');
            return false;
        }

        firstName = $.trim(firstName);
        phone = $.trim(phone);
        subjectName = $.trim(subjectName);
        email = $.trim(email);
        msg = $.trim(msg);

        if (firstName != '' && email != '' && msg != '') {
            var values = "firstName=" + firstName + "&phone=" + phone + "&subjectName=" + subjectName + "&email=" + email + " &msg=" + msg;
            $.ajax({
                type: "POST",
                url: "assets/php/mail.php",
                data: values,
                success: function() {
                    $('#firstName').val('');
                    $('#phone').val('');
                    $('#subjectName').val('');
                    $('#email').val('');
                    $('#msg').val('');

                    $('.cf-msg').fadeIn().html('<div class="alert alert-success"><strong>Success!</strong> Email has been sent successfully.</div>');
                    setTimeout(function() {
                        $('.cf-msg').fadeOut('slow');
                    }, 4000);
                }
            });
        } else {
            $('.cf-msg').fadeIn().html('<div class="alert alert-danger"><strong>Warning!</strong> Please fillup the informations correctly.</div>')
        }
        return false;
    });


    // Ajax Contact Form JS END


}(jQuery));


/*---------------------
    Shuffle JS
--------------------- */
// Portfolio Style 1
if ($('.shuffle-box').length > 0) {
    var Shuffle = window.Shuffle;
    var myShuffle = new Shuffle(document.querySelector('.shuffle-box'), {
    itemSelector: '.single-shuffle',
    sizer: '.my-sizer-element',
    buffer: 1,
    });

    $('input[name="shuffle-filter"]').on('change', function (evt) {
    var input = evt.currentTarget;
    if (input.checked) {
        myShuffle.filter(input.value);
    }
    });
}



// Portfolio Style 2
if ($('.fotolia-grid-2').length > 0) {

    var Shuffle = window.Shuffle;
    var myShuffle = new Shuffle(document.querySelector('.fotolia-grid-2'), {
    itemSelector: '.grid2-item',
    sizer: '.grid2-sizer',
    buffer: 1,
    });

    $('input[name="shuffle-filter"]').on('change', function (evt) {
    var input = evt.currentTarget;
    if (input.checked) {
        myShuffle.filter(input.value);
    }
    });
}



// Portfolio Style 3
if ($('.fotolia-grid-3').length > 0) {
    var Shuffle = window.Shuffle;
    var myShuffle = new Shuffle(document.querySelector('.fotolia-grid-3'), {
    itemSelector: '.grid3-item',
    sizer: '.grid3-sizer',
    buffer: 1,
    });

    $('input[name="shuffle-filter"]').on('change', function (evt) {
    var input = evt.currentTarget;
    if (input.checked) {
        myShuffle.filter(input.value);
    }
    });

}


// Portfolio Style 4
if ($('.fotolia-grid-4').length > 0) {
    var Shuffle = window.Shuffle;
    var myShuffle = new Shuffle(document.querySelector('.fotolia-grid-4'), {
    itemSelector: '.grid4-item',
    sizer: '.grid4-sizer',
    buffer: 1,
    });

    $('input[name="shuffle-filter"]').on('change', function (evt) {
    var input = evt.currentTarget;
    if (input.checked) {
        myShuffle.filter(input.value);
    }
    });

}

/*---------------------
    Secondary Nav 1 JS
    --------------------- */
if ($('.fotoliaCircular-menu').length > 0) {
    var items = document.querySelectorAll('.circle a');

    for (var i = 0, l = items.length; i < l; i++) {
        items[i].style.left = (50 - 35 * Math.cos(-0.5 * Math.PI - 2 * (1 / l) * i * Math.PI)).toFixed(4) + "%";

        items[i].style.top = (50 + 35 * Math.sin(-0.5 * Math.PI - 2 * (1 / l) * i * Math.PI)).toFixed(4) + "%";
    }

    // document.querySelector('.menu2nd-btn').onclick = function (e) {
    //     e.preventDefault();
    //     document.querySelector('.circle').classList.toggle('open');
    //     document.querySelector('.secondMenu_V1').classList.toggle('active');
    // }
    $('.menu2nd-btn').on('click',function(){
        document.querySelector('.circle').classList.toggle('open');
        document.querySelector('.secondMenu_V1').classList.toggle('active');
    });

    $(document).on('keyup',function(evt) {
        if (evt.keyCode == 27) {
            $('.circle').removeClass('open');
            $('.secondMenu_V1').removeClass('active');
        }
    });
}




(function($){
    var search_button = $('.search-open'),
        close_button  = $('.search-close'),
        input = $('.input');
    search_button.on('click',function(){
      $('.search_V1').addClass('open');
      search_button.fadeOut(0);
      close_button.fadeIn(0);

      input.fadeIn(500);
    });

    close_button.on('click',function(){
    $('.search_V1').removeClass('open');
      close_button.fadeOut(0);
      search_button.fadeIn(0);
      input.fadeOut(500);
    });
  })(jQuery);







// Slick JS
if ($('.gallerySliderV1').length > 0) {
    $(window).on('load', function () {

        $('.gallerySliderV1').slick({
            autoplay: true,
            autoplaySpeed: 3000,
            pauseOnHover: true,
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows: false,
            fade: true,
            speed: 900,
            dots: false,
            infinite: true,
            asNavFor: '.gallerySliderV1_nav'
        });

        $('.gallerySliderV1_nav').slick({
            slidesToShow: 8,
            // slidesToScroll: 1,
            arrows: true,
            dots: false,
            infinite: true,
            focusOnSelect: true,
            responsive: [
                {
                    breakpoint: 1200,
                    settings: {
                      slidesToShow: 5
                  }
                },
                {
                    breakpoint: 800,
                    settings: {
                        slidesToShow: 4
                    }
                },
                {
                    breakpoint: 600,
                    settings: {
                        slidesToShow: 3
                    }
                },
                {
                    breakpoint: 500,
                    settings: {
                        slidesToShow: 2
                    }
                },
            ],
            asNavFor: '.gallerySliderV1',
        });

        $('.gallerySliderV1').on('wheel', (function(e) {
            e.preventDefault();

            if (e.originalEvent.deltaY < 0) {
              $(this).slick('slickPrev');
            } else {
              $(this).slick('slickNext');
            }
        }));
        $(window).on('keyup', function (event) {
            // handle cursor keys
            if (event.keyCode == 37) {
                // go left
                $('.gallerySliderV1').slick('slickNext');

            } else if (event.keyCode == 39) {
               // go right
               $('.gallerySliderV1').slick('slickPrev');
            }

        });

    });
}



// Slick JS
if ($('.gallerySliderV2').length > 0) {
    $(window).on('load', function () {

        $('.gallerySliderV2').slick({
            autoplay: false,
            autoplaySpeed: 3000,
            pauseOnHover: true,
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows: false,
            fade: true,
            speed: 900,
            dots: false,
            infinite: false,
            asNavFor: '.gallerySliderV2_nav'
        });

        // $('.gallerySliderV2').on('wheel', (function(e) {
        //     e.preventDefault();

        //     if (e.originalEvent.deltaY < 0) {
        //       $(this).slick('slickNext');
        //     } else {
        //       $(this).slick('slickPrev');
        //     }
        // }));

        $('.gallerySliderV2_nav').slick({
            slidesToShow: 3,
            // slidesToScroll: 1,
            arrows: false,
            dots: false,
            infinite: false,
            focusOnSelect: true,
            vertical: true,
            verticalSwiping: true,
            responsive: [
                {
                    breakpoint: 1200,
                    settings: {
                      slidesToShow: 3
                  }
                },
                {
                    breakpoint: 800,
                    settings: {
                        slidesToShow: 3
                    }
                },
                {
                    breakpoint: 600,
                    settings: {
                        slidesToShow: 3
                    }
                },
                {
                    breakpoint: 500,
                    settings: {
                        slidesToShow: 3
                    }
                },
            ],
            asNavFor: '.gallerySliderV2',
        });


        $('.gallerySliderV2_nav').on('wheel', (function(e) {
            e.preventDefault();

            if (e.originalEvent.deltaY < 0) {
              $(this).slick('slickPrev');
            } else {
              $(this).slick('slickNext');
            }


        }));

        $('.gallerySliderV2_nav').on('afterChange', function(event, slick, currentSlide) {
            // console.log(slick, currentSlide);
            if (slick.$slides.length-1 == currentSlide) {
                $('html, body').animate({
                    scrollTop: $("#pf16").offset().top
                }, 2000);
            }
          })


    });
}






// Overlay Nav

$('#toggleNavMenu').on('click',function() {
    $(this).toggleClass('active');
    $('#overlay').toggleClass('open');
});


if ($('.overlayNav').length > 0) {


    $(window).on('load',function(){
        $('.overlayNav ul.oLay-menu>li').has('>ul').addClass('hasSub');
        $('.overlayNav ul>li>ul.oSubmenu>li').has('ul').addClass('has3Sub');
        $('.hasSub>a').on('click', function () {
            $(this).parent('li.hasSub').toggleClass('showDropdown');
        });
        $('li.has3Sub>a').on('click', function () {
            $(this).parent('li.has3Sub').toggleClass('showDropdown');
        });
    });

    // $('.overlayNav ul>li').on('click', function () {
    //     $(this).toggleClass('showSubmenu');
    // });

    // $('.overlayNav ul>li ul.oSubmenu>li').on('click', function () {
    //     $(this).toggleClass('show3Submenu');
    // });
}





// Overlay Nav 2

if ($('.oNav').length > 0) {
    $('.sf-toggle-btn').on('click',function(){
        $('.sidemenu2-area').toggleClass('showsm2');
    });

    $('.sf-toggle-close').on('click',function(){
        $('.sidemenu2-area').removeClass('showsm2');
    });
}




// Fixed SideNav2 JS
$('.sfv2-oc').on('click', function(){
    $(this).parent().addClass('active-ocnav');
    $('.active-ocnav').parent().toggleClass('show-ocnav');
});






// Hero Area Blend Camera Mask JS
if ($('#circle').length > 0) {
$(window).on('load',function(e) {

    // set the variables
    var timer;
    var mouseX = 0, mouseY = 0;
    var xp = 0, yp =0;
    var circle = $("#circle");

    function mouseStopped(){
        // if mouse stop moving remove class moving
        // it will hide the circle with opacity transition
        circle.removeClass('moving');
    }

    $(window).on('mousemove',function(e){
        // if mouse start moving add class moving
        // it will show the circle with opacity transition
        circle.addClass('moving');
        // get the mouse position minus 160px to center the circle
        mouseX = e.pageX - 50;
        mouseY = e.pageY - 50;
        // if mouse stop moving clear timer and call mouseStopped function
        clearTimeout(timer);
        timer=setTimeout(mouseStopped,3000);
    });

    // set the momentum with setInterval function
    var loop = setInterval(function(){
    // change 12 to alter damping higher is slower
    xp += ((mouseX - xp)/6);
    yp += ((mouseY - yp)/6);
    circle.css({left: xp +'px', top: yp +'px'});  //
    }, 30);

    });

}





// Sidebar Fixed V2

$('#sfv2-toggler').on('click',function() {
    $('.sideBar-fixed.sideBar-fixedV2').toggleClass('sfv2vissible');
    $('.sfv2-open-om i.fa').toggleClass('fa-times');
});



    // Masonry Grid
    if ($('.g5grid').length > 0) {
        $('.g5grid').masonry({
            itemSelector: '.g5grid-item',
            columnWidth: 240
        });
    }

    // Slider Revolution Activation
    if ($('.revSlideHero').length > 0) {
        var revapi486;
        $(window).on('load', function () {
            if ($("#rev_slider_486_1").revolution == undefined) {
                revslider_showDoubleJqueryError("#rev_slider_486_1");
            } else {
                revapi486 = $("#rev_slider_486_1").show().revolution({
                    sliderType: "standard",
                    jsFileLocation: "assets/revolution/js/",
                    sliderLayout: "fullwidth",
                    dottedOverlay: "none",
                    delay: 9000,
                    navigation: {
                        keyboardNavigation: "on",
                        keyboard_direction: "horizontal",
                        mouseScrollNavigation: "off",
                        mouseScrollReverse: "default",
                        onHoverStop: "on",
                        touch: {
                            touchenabled: "on",
                            swipe_threshold: 75,
                            swipe_min_touches: 1,
                            swipe_direction: "horizontal",
                            drag_block_vertical: false
                        }
                        ,
                        arrows: {
                            style: "gyges",
                            enable: true,
                            hide_onmobile: false,
                            hide_over: 778,
                            hide_onleave: false,
                            tmp: '',
                            left: {
                                h_align: "right",
                                v_align: "bottom",
                                h_offset: 40,
                                v_offset: 0
                            },
                            right: {
                                h_align: "right",
                                v_align: "bottom",
                                h_offset: 0,
                                v_offset: 0
                            }
                        }
                        ,
                        tabs: {
                            style: "erinyen",
                            enable: true,
                            width: 250,
                            height: 50,
                            min_width: 250,
                            wrapper_padding: 0,
                            wrapper_color: "transparent",
                            wrapper_opacity: "0",
                            tmp: '<div class="tp-tab-title">{{title}}</div>',
                            //tmp: '<div class="tp-tab-title">{{title}}</div><div class="tp-tab-desc">{{description}}</div>',
                            visibleAmount: 3,
                            hide_onmobile: true,
                            hide_under: 778,
                            hide_onleave: false,
                            hide_delay: 200,
                            direction: "vertical",
                            span: false,
                            position: "inner",
                            space: 10,
                            h_align: "right",
                            v_align: "center",
                            h_offset: 30,
                            v_offset: 0
                        }
                    },
                    viewPort: {
                        enable: true,
                        outof: "pause",
                        visible_area: "80%",
                        presize: false
                    },
                    responsiveLevels: [1240, 1024, 778, 480],
                    visibilityLevels: [1240, 1024, 778, 480],
                    gridwidth: [1240, 1024, 778, 480],
                    gridheight: [660, 550, 500, 400],
                    lazyType: "none",
                    parallax: {
                        type: "scroll",
                        origo: "enterpoint",
                        speed: 400,
                        levels: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 46, 47, 48, 49, 50, 55],
                        type: "scroll",
                    },
                    shadow: 0,
                    spinner: "off",
                    stopLoop: "off",
                    stopAfterLoops: -1,
                    stopAtSlide: -1,
                    shuffle: "off",
                    autoHeight: "off",
                    hideThumbsOnMobile: "off",
                    hideSliderAtLimit: 0,
                    hideCaptionAtLimit: 0,
                    hideAllCaptionAtLilmit: 0,
                    debugMode: false,
                    fallbacks: {
                        simplifyAll: "off",
                        nextSlideOnWindowFocus: "off",
                        disableFocusListener: false,
                    }
                });
            }
        });	/*ready*/
    }



    if ($('.hero-V22').length > 0) {

        var revapi1064;
        $(window).on('load', function () {
            if ($("#rev_slider_1064_1").revolution == undefined) {
                revslider_showDoubleJqueryError("#rev_slider_1064_1");
            } else {
                revapi1064 = $("#rev_slider_1064_1").show().revolution({
                    sliderType: "standard",
                    jsFileLocation: "revolution/js/",
                    sliderLayout: "fullscreen",
                    dottedOverlay: "none",
                    delay: 9000,
                    navigation: {
                        keyboardNavigation: "off",
                        keyboard_direction: "horizontal",
                        mouseScrollNavigation: "off",
                        mouseScrollReverse: "default",
                        onHoverStop: "off",
                        touch: {
                            touchenabled: "on",
                            swipe_threshold: 75,
                            swipe_min_touches: 1,
                            swipe_direction: "vertical",
                            drag_block_vertical: false
                        }
                    },
                    responsiveLevels: [1240, 1024, 778, 480],
                    visibilityLevels: [1240, 1024, 778, 480],
                    gridwidth: [1240, 1024, 778, 480],
                    gridheight: [868, 768, 960, 720],
                    lazyType: "none",
                    shadow: 0,
                    spinner: "off",
                    stopLoop: "on",
                    stopAfterLoops: 0,
                    stopAtSlide: 1,
                    shuffle: "off",
                    autoHeight: "off",
                    fullScreenAutoWidth: "off",
                    fullScreenAlignForce: "off",
                    fullScreenOffsetContainer: ".header",
                    fullScreenOffset: "",
                    disableProgressBar: "on",
                    hideThumbsOnMobile: "off",
                    hideSliderAtLimit: 0,
                    hideCaptionAtLimit: 0,
                    hideAllCaptionAtLilmit: 0,
                    debugMode: false,
                    fallbacks: {
                        simplifyAll: "off",
                        nextSlideOnWindowFocus: "off",
                        disableFocusListener: false,
                    }
                });
            }
        });	/*ready*/

    }


    if ($('.hero_V23').length > 0) {
        var revapi24;
        $(window).on('load', function() {
            if($("#rev_slider_24_1").revolution == undefined){
                revslider_showDoubleJqueryError("#rev_slider_24_1");
            }else{
                revapi24 = $("#rev_slider_24_1").show().revolution({
                    sliderType:"standard",
                    jsFileLocation:"revolution/js/",
                    sliderLayout:"fullscreen",
                    dottedOverlay:"none",
                    delay:9000,
                    navigation: {
                        keyboardNavigation:"off",
                        keyboard_direction: "horizontal",
                        mouseScrollNavigation:"off",
                         mouseScrollReverse:"default",
                        onHoverStop:"off",
                        bullets: {
                            enable:true,
                            hide_onmobile:false,
                            style:"bullet-bar",
                            hide_onleave:false,
                            direction:"horizontal",
                            h_align:"center",
                            v_align:"bottom",
                            h_offset:0,
                            v_offset:50,
                            space:5,
                            tmp:''
                        }
                    },
                    responsiveLevels:[1240,1024,778,480],
                    visibilityLevels:[1240,1024,778,480],
                    gridwidth:[1240,1024,778,480],
                    gridheight:[868,768,960,720],
                    lazyType:"none",
                    shadow:0,
                    spinner:"off",
                    stopLoop:"off",
                    stopAfterLoops:-1,
                    stopAtSlide:-1,
                    shuffle:"off",
                    autoHeight:"off",
                    fullScreenAutoWidth:"off",
                    fullScreenAlignForce:"off",
                    fullScreenOffsetContainer: "",
                    fullScreenOffset: "0px",
                    hideThumbsOnMobile:"off",
                    hideSliderAtLimit:0,
                    hideCaptionAtLimit:0,
                    hideAllCaptionAtLilmit:0,
                    debugMode:false,
                    fallbacks: {
                        simplifyAll:"off",
                        nextSlideOnWindowFocus:"off",
                        disableFocusListener:false,
                    }
                });
            }

            if(revapi24) revapi24.revSliderSlicey();
        });	/*ready*/
    }




    if ($('.fancyGallery').length > 0) {
        $(function () {
            $(".fancyGallery").fancybox({
                buttons : [
                    // Default
                    'slideShow',
                    'fullScreen',
                    'thumbs',
                    'share',
                    'close',
                    // Activation
                    'download',
                    'zoom'
                ]
            });
        });
    }



    $(window).on('load', function(){
        if ($('.fotoliaCircular-menu').length > 0) {
            if ($('.fotoliaCircular-menu .circle a').length == 7) {
                $('.fotoliaCircular-menu').addClass('f7ml');
            }
            if ($('.fotoliaCircular-menu .circle a').length == 6) {
                $('.fotoliaCircular-menu').addClass('f6ml');
            }
            if ($('.fotoliaCircular-menu .circle a').length == 5) {
                $('.fotoliaCircular-menu').addClass('f5ml');
            }
            if ($('.fotoliaCircular-menu .circle a').length == 4) {
                $('.fotoliaCircular-menu').addClass('f4ml');
            }
            if ($('.fotoliaCircular-menu .circle a').length == 3) {
                $('.fotoliaCircular-menu').addClass('f3ml');
            }
            if ($('.fotoliaCircular-menu .circle a').length == 2) {
                $('.fotoliaCircular-menu').addClass('f2ml');
            }

        }
    });


