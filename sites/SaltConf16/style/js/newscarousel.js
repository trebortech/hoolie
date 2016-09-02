/************************************************************************/// // NEWS ///************************************************************************/

/**
 * We use the initCallback callback
 * to assign functionality to the controls
 */
function mycarousel_initCallback(carousel) {

    jQuery('#newslist-next').bind('click', function() {
        carousel.next();
        return false;
    });

    jQuery('#newslist-prev').bind('click', function() {
        carousel.prev();
        return false;
    });
};

// Ride the carousel...
jQuery(document).ready(function() {
    jQuery("#newslist").jcarousel({
        scroll: 1,
        initCallback: mycarousel_initCallback,

        buttonNextHTML: null,
        buttonPrevHTML: null,
        vertical: true,
        itemLastOutCallback: {
           onAfterAnimation: disableCustomButtons
        },
        itemLastInCallback: {
           onAfterAnimation: disableCustomButtons
        }
    });
});




function disableCustomButtons(carousel){
    
    var prev_class = 'jcarousel-prev-disabled jcarousel-prev-disabled-vertical';
    if (carousel.first == 1) {
    $('#newslist-prev').attr('disabled', 'true').addClass(prev_class);
    } else {
    

$('#newslist-prev').removeAttr('disabled').removeClass(prev_class);
    }
  
    var next_class = 'jcarousel-next-disabled jcarousel-next-disabled-vertical';
    if (carousel.last == carousel.size()) {
    $('#newslist-next').attr('disabled', 'true').addClass(next_class);
    } else {
   $('#newslist-next').removeAttr('disabled').removeClass(next_class);
    }

};