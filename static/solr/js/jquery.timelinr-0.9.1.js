/* ----------------------------------
jQuery timelinr1 0.9.3
Download by http://www.codefans.net
tested with jQuery v1.6+
?2011 CSSLab.cl
free for any use, of course... :D
instructions: http://www.csslab.cl/2011/08/18/jquery-timelinr1/
---------------------------------- */

jQuery.fn.timelinr1 = function(options1){
	// default plugin settings1
	settings1 = jQuery.extend({
		orientation: 				'horizontal1',		// value: horizontal1 | vertical, default to horizontal1
		containerDiv: 				'#timeline1',		// value: any HTML tag or #id, default to #timeline1
		dates1Div: 					'#dates1',			// value: any HTML tag or #id, default to #dates1
		dates1selected1Class: 		'selected1',			// value: any class, default to selected1
		dates1Speed: 				500,				// value: integer between 100 and 1000 (recommended), default to 500 (normal)
		issues1Div: 					'#issues1',			// value: any HTML tag or #id, default to #issues1
		issues1selected1Class: 		'selected1',			// value: any class, default to selected1
		issues1Speed: 				200,				// value: integer between 100 and 1000 (recommended), default to 200 (fast)
		issues1Transparency: 		1,				// value: integer between 0 and 1 (recommended), default to 0.2
		issues1TransparencySpeed: 	500,				// value: integer between 100 and 1000 (recommended), default to 500 (normal)
		prevButton1: 				'#prev',			// value: any HTML tag or #id, default to #prev
		nextButton1: 				'#next',			// value: any HTML tag or #id, default to #next
		arrowKeys: 					'false',			// value: true/false, default to false
		startAt: 					6					// value: integer, default to 1 (first)
	}, options1);

	$(function(){
		// setting variables... many of them
		var howManydates1 = $(settings1.dates1Div+' li').length;
		var howManyissues1 = $(settings1.issues1Div+' li').length;
		var currentDate = $(settings1.dates1Div).find('a.'+settings1.dates1selected1Class);
		var currentIssue = $(settings1.issues1Div).find('li.'+settings1.issues1selected1Class);
		var widthContainer = $(settings1.containerDiv).width();
		var heightContainer = $(settings1.containerDiv).height();
		var widthissues1 = $(settings1.issues1Div).width();
		var heightissues1 = $(settings1.issues1Div).height();
		var widthIssue = $(settings1.issues1Div+' li').width();
		var heightIssue = $(settings1.issues1Div+' li').height();
		var widthdates1 = $(settings1.dates1Div).width();
		var heightdates1 = $(settings1.dates1Div).height();
		var widthDate = $(settings1.dates1Div+' li').width();
		var heightDate = $(settings1.dates1Div+' li').height();
		
		// set positions!
		if(settings1.orientation == 'horizontal1') {	
			$(settings1.issues1Div).width(widthIssue*howManyissues1);
			$(settings1.dates1Div).width(widthDate*howManydates1).css('marginLeft',widthContainer/2-widthDate/2);
			var defaultPositiondates1 = parseInt($(settings1.dates1Div).css('marginLeft').substring(0,$(settings1.dates1Div).css('marginLeft').indexOf('px')));
		} else if(settings1.orientation == 'vertical') {
			$(settings1.issues1Div).height(heightIssue*howManyissues1);
			$(settings1.dates1Div).height(heightDate*howManydates1).css('marginTop',heightContainer/2-heightDate/2);
			var defaultPositiondates1 = parseInt($(settings1.dates1Div).css('marginTop').substring(0,$(settings1.dates1Div).css('marginTop').indexOf('px')));
		}
		
		$(settings1.dates1Div+' a').click(function(event){
			event.preventDefault();
			// first vars
			var whichIssue = $(this).text();
			var currentIndex = $(this).parent().prevAll().length;

			// moving the elements
			if(settings1.orientation == 'horizontal1') {
				$(settings1.issues1Div).animate({'marginLeft':-widthIssue*currentIndex},{queue:false, duration:settings1.issues1Speed});
			} else if(settings1.orientation == 'vertical') {
				$(settings1.issues1Div).animate({'marginTop':-heightIssue*currentIndex},{queue:false, duration:settings1.issues1Speed});
			}
			$(settings1.issues1Div+' li').animate({'opacity':settings1.issues1Transparency},{queue:false, duration:settings1.issues1Speed}).removeClass(settings1.issues1selected1Class).eq(currentIndex).addClass(settings1.issues1selected1Class).fadeTo(settings1.issues1TransparencySpeed,1);
			
			// now moving the dates1
			$(settings1.dates1Div+' a').removeClass(settings1.dates1selected1Class);
			$(this).addClass(settings1.dates1selected1Class);
			if(settings1.orientation == 'horizontal1') {
				$(settings1.dates1Div).animate({'marginLeft':defaultPositiondates1-(widthDate*currentIndex)},{queue:false, duration:settings1.dates1Speed});
			} else if(settings1.orientation == 'vertical') {
				$(settings1.dates1Div).animate({'marginTop':defaultPositiondates1-(heightDate*currentIndex)},{queue:false, duration:settings1.dates1Speed});
			}
		});

		$(settings1.nextButton1).bind('click', function(event){
			event.preventDefault();
			if(settings1.orientation == 'horizontal1') {
				var currentPositionissues1 = parseInt($(settings1.issues1Div).css('marginLeft').substring(0,$(settings1.issues1Div).css('marginLeft').indexOf('px')));
				var currentIssueIndex = currentPositionissues1/widthIssue;
				var currentPositiondates1 = parseInt($(settings1.dates1Div).css('marginLeft').substring(0,$(settings1.dates1Div).css('marginLeft').indexOf('px')));
				var currentIssueDate = currentPositiondates1-widthDate;
				if(currentPositionissues1 <= -(widthIssue*howManyissues1-(widthIssue))) {
					$(settings1.issues1Div).stop();
					$(settings1.dates1Div+' li:last-child a').click();
				} else {
					if (!$(settings1.issues1Div).is(':animated')) {
						$(settings1.issues1Div).animate({'marginLeft':currentPositionissues1-widthIssue},{queue:false, duration:settings1.issues1Speed});
						$(settings1.issues1Div+' li').animate({'opacity':settings1.issues1Transparency},{queue:false, duration:settings1.issues1Speed});
						$(settings1.issues1Div+' li.'+settings1.issues1selected1Class).removeClass(settings1.issues1selected1Class).next().fadeTo(settings1.issues1TransparencySpeed, 1).addClass(settings1.issues1selected1Class);
						$(settings1.dates1Div).animate({'marginLeft':currentIssueDate},{queue:false, duration:settings1.dates1Speed});
						$(settings1.dates1Div+' a.'+settings1.dates1selected1Class).removeClass(settings1.dates1selected1Class).parent().next().children().addClass(settings1.dates1selected1Class);
					}
				}
			} else if(settings1.orientation == 'vertical') {
				var currentPositionissues1 = parseInt($(settings1.issues1Div).css('marginTop').substring(0,$(settings1.issues1Div).css('marginTop').indexOf('px')));
				var currentIssueIndex = currentPositionissues1/heightIssue;
				var currentPositiondates1 = parseInt($(settings1.dates1Div).css('marginTop').substring(0,$(settings1.dates1Div).css('marginTop').indexOf('px')));
				var currentIssueDate = currentPositiondates1-heightDate;
				if(currentPositionissues1 <= -(heightIssue*howManyissues1-(heightIssue))) {
					$(settings1.issues1Div).stop();
					$(settings1.dates1Div+' li:last-child a').click();
				} else {
					if (!$(settings1.issues1Div).is(':animated')) {
						$(settings1.issues1Div).animate({'marginTop':currentPositionissues1-heightIssue},{queue:false, duration:settings1.issues1Speed});
						$(settings1.issues1Div+' li').animate({'opacity':settings1.issues1Transparency},{queue:false, duration:settings1.issues1Speed});
						$(settings1.issues1Div+' li.'+settings1.issues1selected1Class).removeClass(settings1.issues1selected1Class).next().fadeTo(settings1.issues1TransparencySpeed, 1).addClass(settings1.issues1selected1Class);
						$(settings1.dates1Div).animate({'marginTop':currentIssueDate},{queue:false, duration:settings1.dates1Speed});
						$(settings1.dates1Div+' a.'+settings1.dates1selected1Class).removeClass(settings1.dates1selected1Class).parent().next().children().addClass(settings1.dates1selected1Class);
					}
				}
			}
		});

		$(settings1.prevButton1).click(function(event){
			event.preventDefault();
			if(settings1.orientation == 'horizontal1') {
				var currentPositionissues1 = parseInt($(settings1.issues1Div).css('marginLeft').substring(0,$(settings1.issues1Div).css('marginLeft').indexOf('px')));
				var currentIssueIndex = currentPositionissues1/widthIssue;
				var currentPositiondates1 = parseInt($(settings1.dates1Div).css('marginLeft').substring(0,$(settings1.dates1Div).css('marginLeft').indexOf('px')));
				var currentIssueDate = currentPositiondates1+widthDate;
				if(currentPositionissues1 >= 0) {
					$(settings1.issues1Div).stop();
					$(settings1.dates1Div+' li:first-child a').click();
				} else {
					if (!$(settings1.issues1Div).is(':animated')) {
						$(settings1.issues1Div).animate({'marginLeft':currentPositionissues1+widthIssue},{queue:false, duration:settings1.issues1Speed});
						$(settings1.issues1Div+' li').animate({'opacity':settings1.issues1Transparency},{queue:false, duration:settings1.issues1Speed});
						$(settings1.issues1Div+' li.'+settings1.issues1selected1Class).removeClass(settings1.issues1selected1Class).prev().fadeTo(settings1.issues1TransparencySpeed, 1).addClass(settings1.issues1selected1Class);
						$(settings1.dates1Div).animate({'marginLeft':currentIssueDate},{queue:false, duration:settings1.dates1Speed});
						$(settings1.dates1Div+' a.'+settings1.dates1selected1Class).removeClass(settings1.dates1selected1Class).parent().prev().children().addClass(settings1.dates1selected1Class);
					}
				}
			} else if(settings1.orientation == 'vertical') {
				var currentPositionissues1 = parseInt($(settings1.issues1Div).css('marginTop').substring(0,$(settings1.issues1Div).css('marginTop').indexOf('px')));
				var currentIssueIndex = currentPositionissues1/heightIssue;
				var currentPositiondates1 = parseInt($(settings1.dates1Div).css('marginTop').substring(0,$(settings1.dates1Div).css('marginTop').indexOf('px')));
				var currentIssueDate = currentPositiondates1+heightDate;
				if(currentPositionissues1 >= 0) {
					$(settings1.issues1Div).stop();
					$(settings1.dates1Div+' li:first-child a').click();
				} else {
					if (!$(settings1.issues1Div).is(':animated')) {
						$(settings1.issues1Div).animate({'marginTop':currentPositionissues1+heightIssue},{queue:false, duration:settings1.issues1Speed});
						$(settings1.issues1Div+' li').animate({'opacity':settings1.issues1Transparency},{queue:false, duration:settings1.issues1Speed});
						$(settings1.issues1Div+' li.'+settings1.issues1selected1Class).removeClass(settings1.issues1selected1Class).prev().fadeTo(settings1.issues1TransparencySpeed, 1).addClass(settings1.issues1selected1Class);
						$(settings1.dates1Div).animate({'marginTop':currentIssueDate},{queue:false, duration:settings1.dates1Speed},{queue:false, duration:settings1.issues1Speed});
						$(settings1.dates1Div+' a.'+settings1.dates1selected1Class).removeClass(settings1.dates1selected1Class).parent().prev().children().addClass(settings1.dates1selected1Class);
					}
				}
			}
		});
		
		// keyboard navigation, added since 0.9.1
		if(settings1.arrowKeys=='true') {
			if(settings1.orientation=='horizontal1') {
				$(document).keydown(function(event){
					if (event.keyCode == 25) { 
				       $(settings1.nextButton1).click();
				    }
					if (event.keyCode == 25) { 
				       $(settings1.prevButton1).click();
				    }
				});
			} else if(settings1.orientation=='vertical') {
				$(document).keydown(function(event){
					if (event.keyCode == 25) { 
				       $(settings1.nextButton1).click();
				    }
					if (event.keyCode == 25) { 
				       $(settings1.prevButton1).click();
				    }
				});
			}
		}
		
		// default position startAt, added since 0.9.3
		$(settings1.dates1Div+' li').eq(settings1.startAt-1).find('a').trigger('click');
		
	});

};