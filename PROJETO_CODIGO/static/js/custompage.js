////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// jQuery
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
var resizeId;

$(document).ready(function($) {
    "use strict";
	
	$('.navbar-nav .nav-link').on('click', function(){
		$('.navbar-collapse').collapse('hide');
	});

//  "img" into "background-image" transfer

    $("[data-background-image]").each(function() {
        $(this).css("background-image", "url("+ $(this).attr("data-background-image") +")" );
    });

    $(".background--image, .img-into-bg").each(function() {
        $(this).css("background-image", "url("+ $(this).find("img").attr("src") +")" );
    });

//  Custom background color

    $("[data-background-color]").each(function() {
        $(this).css("background-color", $(this).attr("data-background-color")  );
    });


    // Particles effect in the "background" class

    $(".background--particles").particleground({
        density: 15000,
        lineWidth: 0.2,
        lineColor: "#515151",
        dotColor: "#313131",
        parallax: false,
        proximity: 200
    });


 



    // Magnific images popup

    $(".popup-image").magnificPopup({
        type:'image',
        fixedContentPos: false,
        gallery: { enabled:true },
        removalDelay: 300,
        mainClass: 'mfp-fade',
        callbacks: {
            // This prevents pushing the entire page to the right after opening Magnific popup image
            open: function() {
                $(".page-wrapper, .navbar-nav").css("margin-right", getScrollBarWidth());
            },
            close: function() {
                $(".page-wrapper, .navbar-nav").css("margin-right", 0);
            }
        }
    });


	
	//  Form Validation

    $(".form .btn[type='submit']").on("click", function(e){		
        var button = $(this);
        var form = $(this).closest("form");
        button.prepend("<div class='status'></div>");		
        form.validate({
            submitHandler: function() {
                $.post("assets/php/email.php", form.serialize(),  function(response) {
				console.log(response);
                    button.find(".status").append(response);
                    form.addClass("submitted");
                });
                return false;
            }
        });
    });

    heroHeight();

});

// On RESIZE actions



// On RESIZE actions

$(window).on("load", function(){
    if ( $(window).scrollTop() > 0 ) {
        $(".navbar").addClass("bg-black")
    }
    else {
        $(".navbar").removeClass("bg-black")
    }
});

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Functions
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Do after resize

function doneResizing(){
    heroHeight();
}

// Set Hero height

function heroHeight(){
    $("#hero").height( $(window).height() );
}

// Smooth Scroll

$('a[href*="#"]')
    .not('[href="#"]')
    .not('[href="#0"]')
    .on("click", function(event) {
        if (
            location.pathname.replace(/^\//, '') === this.pathname.replace(/^\//, '')
            &&
            location.hostname === this.hostname
        ) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                event.preventDefault();
                $('html, body').animate({
                    scrollTop: target.offset().top
                }, 1000, function() {
                    var $target = $(target);
                    $target.focus();
                    if ($target.is(":focus")) {
                        return false;
                    } else {
                        $target.attr('tabindex','-1');
                        $target.focus();
                    }
                });
            }
        }
    });

// Return scrollbar width

function getScrollBarWidth () {
    var $outer = $('<div>').css({visibility: 'hidden', width: 100, overflow: 'scroll'}).appendTo('body'),
        widthWithScroll = $('<div>').css({width: '100%'}).appendTo($outer).outerWidth();
    $outer.remove();
    return 100 - widthWithScroll;
}
