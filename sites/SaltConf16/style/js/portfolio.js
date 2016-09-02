
/************************************************************************/// /* SORTING *//************************************************************************/

(function($) {
	$.fn.sorted = function(customOptions) {
		var options = {
			reversed: false,
			by: function(a) {
				return a.text();
			}
		};
		$.extend(options, customOptions);
	
		$data = $(this);
		arr = $data.get();
		arr.sort(function(a, b) {
			
		   	var valA = options.by($(a));
		   	var valB = options.by($(b));
			if (options.reversed) {
				return (valA < valB) ? 1 : (valA > valB) ? -1 : 0;				
			} else {		
				return (valA < valB) ? -1 : (valA > valB) ? 1 : 0;	
			}
		});
		return $(arr);
	};

})(jQuery);

$(function() {
  
  var read_button = function(class_names) {
    var r = {
      selected: false,
      type: 0
    };
    for (var i=0; i < class_names.length; i++) {
      if (class_names[i].indexOf('selected-') == 0) {
        r.selected = true;
      }
      if (class_names[i].indexOf('segment-') == 0) {
        r.segment = class_names[i].split('-')[1];
      }
    };
    return r;
  };
  
  var determine_sort = function($buttons) {
    var $selected = $buttons.parent().filter('[class*="selected-"]');
    return $selected.find('a').attr('data-value');
  };
  
  var determine_kind = function($buttons) {
    var $selected = $buttons.parent().filter('[class*="selected-"]');
    return $selected.find('a').attr('data-value');
  };
  
  var $preferences = {
    duration: 800,
    easing: 'easeInOutQuad',
    adjustHeight: false
  };
  
  var $list = $('#gallery');
  var $data = $list.clone();
  
  var $controls = $('.gallerynav');
  
  $controls.each(function(i) {
    
    var $control = $(this);
    var $buttons = $control.find('a');
    
    $buttons.bind('click', function(e) {
      
      var $button = $(this);
      var $button_container = $button.parent();
      var button_properties = read_button($button_container.attr('class').split(' '));      
      var selected = button_properties.selected;
      var button_segment = button_properties.segment;

      if (!selected) {

        $buttons.parent().removeClass('selected-1'); $button_container.addClass('selected-' + 1);
        
        var sorting_type = determine_sort($controls.eq(1).find('a'));
        var sorting_kind = determine_kind($controls.eq(0).find('a'));
        
        if (sorting_kind == 'all') {
          var $filtered_data = $data.find('li');
        } else {
          var $filtered_data = $data.find('li.' + sorting_kind);
        }
        
        if (sorting_type == 'size') {
          var $sorted_data = $filtered_data.sorted({
            by: function(v) {
              return parseFloat($(v).find('span').text());
            }
          });
        } else {
          var $sorted_data = $filtered_data.sorted({
            by: function(v) {
              return $(v).find('strong').text().toLowerCase();
            }
          });
        }
        
        $list.quicksand($sorted_data, function() {
    
    $(document).ready(function(){
			$("#gallery a[rel^='prettyPhoto']").prettyPhoto({theme:'light_square', autoplay_slideshow: false});
		});
		
    $(function() {
    // OPACITY OF BUTTON SET TO 50%
    $("ul.grid img").css("opacity","1.0");
    		
    // ON MOUSE OVER
    $("ul.grid img").hover(function () {
    										  
    // SET OPACITY TO 100%
    $(this).stop().animate({
    opacity: 0.5
    }, "slow");
    },
    		
    // ON MOUSE OUT
    function () {
    			
    // SET OPACITY BACK TO 50%
    $(this).stop().animate({
    opacity: 1.0
    }, "slow");
    });
    });
                                
	$("a.zoom2 img").mouseover(function(){
		$(this).stop(true,true);
		$(this).fadeTo(300, 0.5);
	});
	
	$("a.zoom2 img").mouseout(function(){
		$(this).fadeTo(400, 1.0);
	});
	
	
	$("a.play2 img").mouseover(function(){
		$(this).stop(true,true);
		$(this).fadeTo(300, 0.5);
	});
	
	$("a.play2 img").mouseout(function(){
		$(this).fadeTo(400, 1.0);
	});
	
    });
}  
      e.preventDefault();
    });
    
  }); 
  
});