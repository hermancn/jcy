/* ----------------------------------
jQuery Timelinr 0.9.3
Download by http://www.codefans.net
tested with jQuery v1.6+
?2011 CSSLab.cl
free for any use, of course... :D
instructions: http://www.csslab.cl/2011/08/18/jquery-timelinr21/
---------------------------------- */

jQuery.fn.timelinr2 = function(options){
	// default plugin settings1
	settings1 = jQuery.extend({
		orientation1: 				'horizontal',		// value: horizontal | vertical, default to horizontal
		containerDiv1: 				'#timeline2',		// value: any HTML tag or #id, default to #timeline2
		dates2Div: 					'#dates2',			// value: any HTML tag or #id, default to #dates2
		dates2SelectedClass: 		'selected2',			// value: any class, default to selected2
		dates2Speed: 				500,				// value: integer between 100 and 1000 (recommended), default to 500 (normal)
		issues2Div: 					'#issues2',			// value: any HTML tag or #id, default to #issues2
		issues2SelectedClass: 		'selected2',			// value: any class, default to selected2
		issues2Speed: 				200,				// value: integer between 100 and 1000 (recommended), default to 200 (fast)
		issues2Transparency: 		1,				// value: integer between 0 and 1 (recommended), default to 0.2
		issues2TransparencySpeed: 	500,				// value: integer between 100 and 1000 (recommended), default to 500 (normal)
		prevButton: 				'#prev',			// value: any HTML tag or #id, default to #prev
		nextButton: 				'#next',			// value: any HTML tag or #id, default to #next
		arrowKeys: 					'false',			// value: true/false, default to false
		startAt: 					6					// value: integer, default to 1 (first)
	}, options);

	$(function(){
		// setting variables... many of them
		var howManyDates = $(settings1.dates2Div+' li').length;
		var howManyIssues = $(settings1.issues2Div+' li').length;
		var currentDate = $(settings1.dates2Div).find('a.'+settings1.dates2SelectedClass);
		var currentIssue = $(settings1.issues2Div).find('li.'+settings1.issues2SelectedClass);
		var widthContainer = $(settings1.containerDiv1).width();
		var heightContainer = $(settings1.containerDiv1).height();
		var widthIssues = $(settings1.issues2Div).width();
		var heightIssues = $(settings1.issues2Div).height();
		var widthIssue = $(settings1.issues2Div+' li').width();
		var heightIssue = $(settings1.issues2Div+' li').height();
		var widthDates = $(settings1.dates2Div).width();
		var heightDates = $(settings1.dates2Div).height();
		var widthDate = $(settings1.dates2Div+' li').width();
		var heightDate = $(settings1.dates2Div+' li').height();
		
		// set positions!
		if(settings1.orientation1 == 'horizontal') {	
			$(settings1.issues2Div).width(widthIssue*howManyIssues);
			$(settings1.dates2Div).width(widthDate*howManyDates).css('marginLeft',widthContainer/2-widthDate/2);
			var defaultPositionDates = parseInt($(settings1.dates2Div).css('marginLeft').substring(0,$(settings1.dates2Div).css('marginLeft').indexOf('px')));
		} else if(settings1.orientation1 == 'vertical') {
			$(settings1.issues2Div).height(heightIssue*howManyIssues);
			$(settings1.dates2Div).height(heightDate*howManyDates).css('marginTop',heightContainer/2-heightDate/2);
			var defaultPositionDates = parseInt($(settings1.dates2Div).css('marginTop').substring(0,$(settings1.dates2Div).css('marginTop').indexOf('px')));
		}
		
		$(settings1.dates2Div+' a').click(function(event){
			event.preventDefault();
			// first vars
			var whichIssue = $(this).text();
			var currentIndex = $(this).parent().prevAll().length;

			// moving the elements
			if(settings1.orientation1 == 'horizontal') {
				$(settings1.issues2Div).animate({'marginLeft':-widthIssue*currentIndex},{queue:false, duration:settings1.issues2Speed});
			} else if(settings1.orientation1 == 'vertical') {
				$(settings1.issues2Div).animate({'marginTop':-heightIssue*currentIndex},{queue:false, duration:settings1.issues2Speed});
			}
			$(settings1.issues2Div+' li').animate({'opacity':settings1.issues2Transparency},{queue:false, duration:settings1.issues2Speed}).removeClass(settings1.issues2SelectedClass).eq(currentIndex).addClass(settings1.issues2SelectedClass).fadeTo(settings1.issues2TransparencySpeed,1);
			
			// now moving the dates2
			$(settings1.dates2Div+' a').removeClass(settings1.dates2SelectedClass);
			$(this).addClass(settings1.dates2SelectedClass);
			if(settings1.orientation1 == 'horizontal') {
				$(settings1.dates2Div).animate({'marginLeft':defaultPositionDates-(widthDate*currentIndex)},{queue:false, duration:settings1.dates2Speed});
			} else if(settings1.orientation1 == 'vertical') {
				$(settings1.dates2Div).animate({'marginTop':defaultPositionDates-(heightDate*currentIndex)},{queue:false, duration:settings1.dates2Speed});
			}
		});

		$(settings1.nextButton).bind('click', function(event){
			event.preventDefault();
			if(settings1.orientation1 == 'horizontal') {
				var currentPositionIssues = parseInt($(settings1.issues2Div).css('marginLeft').substring(0,$(settings1.issues2Div).css('marginLeft').indexOf('px')));
				var currentIssueIndex = currentPositionIssues/widthIssue;
				var currentPositionDates = parseInt($(settings1.dates2Div).css('marginLeft').substring(0,$(settings1.dates2Div).css('marginLeft').indexOf('px')));
				var currentIssueDate = currentPositionDates-widthDate;
				if(currentPositionIssues <= -(widthIssue*howManyIssues-(widthIssue))) {
					$(settings1.issues2Div).stop();
					$(settings1.dates2Div+' li:last-child a').click();
				} else {
					if (!$(settings1.issues2Div).is(':animated')) {
						$(settings1.issues2Div).animate({'marginLeft':currentPositionIssues-widthIssue},{queue:false, duration:settings1.issues2Speed});
						$(settings1.issues2Div+' li').animate({'opacity':settings1.issues2Transparency},{queue:false, duration:settings1.issues2Speed});
						$(settings1.issues2Div+' li.'+settings1.issues2SelectedClass).removeClass(settings1.issues2SelectedClass).next().fadeTo(settings1.issues2TransparencySpeed, 1).addClass(settings1.issues2SelectedClass);
						$(settings1.dates2Div).animate({'marginLeft':currentIssueDate},{queue:false, duration:settings1.dates2Speed});
						$(settings1.dates2Div+' a.'+settings1.dates2SelectedClass).removeClass(settings1.dates2SelectedClass).parent().next().children().addClass(settings1.dates2SelectedClass);
					}
				}
			} else if(settings1.orientation1 == 'vertical') {
				var currentPositionIssues = parseInt($(settings1.issues2Div).css('marginTop').substring(0,$(settings1.issues2Div).css('marginTop').indexOf('px')));
				var currentIssueIndex = currentPositionIssues/heightIssue;
				var currentPositionDates = parseInt($(settings1.dates2Div).css('marginTop').substring(0,$(settings1.dates2Div).css('marginTop').indexOf('px')));
				var currentIssueDate = currentPositionDates-heightDate;
				if(currentPositionIssues <= -(heightIssue*howManyIssues-(heightIssue))) {
					$(settings1.issues2Div).stop();
					$(settings1.dates2Div+' li:last-child a').click();
				} else {
					if (!$(settings1.issues2Div).is(':animated')) {
						$(settings1.issues2Div).animate({'marginTop':currentPositionIssues-heightIssue},{queue:false, duration:settings1.issues2Speed});
						$(settings1.issues2Div+' li').animate({'opacity':settings1.issues2Transparency},{queue:false, duration:settings1.issues2Speed});
						$(settings1.issues2Div+' li.'+settings1.issues2SelectedClass).removeClass(settings1.issues2SelectedClass).next().fadeTo(settings1.issues2TransparencySpeed, 1).addClass(settings1.issues2SelectedClass);
						$(settings1.dates2Div).animate({'marginTop':currentIssueDate},{queue:false, duration:settings1.dates2Speed});
						$(settings1.dates2Div+' a.'+settings1.dates2SelectedClass).removeClass(settings1.dates2SelectedClass).parent().next().children().addClass(settings1.dates2SelectedClass);
					}
				}
			}
		});

		$(settings1.prevButton).click(function(event){
			event.preventDefault();
			if(settings1.orientation1 == 'horizontal') {
				var currentPositionIssues = parseInt($(settings1.issues2Div).css('marginLeft').substring(0,$(settings1.issues2Div).css('marginLeft').indexOf('px')));
				var currentIssueIndex = currentPositionIssues/widthIssue;
				var currentPositionDates = parseInt($(settings1.dates2Div).css('marginLeft').substring(0,$(settings1.dates2Div).css('marginLeft').indexOf('px')));
				var currentIssueDate = currentPositionDates+widthDate;
				if(currentPositionIssues >= 0) {
					$(settings1.issues2Div).stop();
					$(settings1.dates2Div+' li:first-child a').click();
				} else {
					if (!$(settings1.issues2Div).is(':animated')) {
						$(settings1.issues2Div).animate({'marginLeft':currentPositionIssues+widthIssue},{queue:false, duration:settings1.issues2Speed});
						$(settings1.issues2Div+' li').animate({'opacity':settings1.issues2Transparency},{queue:false, duration:settings1.issues2Speed});
						$(settings1.issues2Div+' li.'+settings1.issues2SelectedClass).removeClass(settings1.issues2SelectedClass).prev().fadeTo(settings1.issues2TransparencySpeed, 1).addClass(settings1.issues2SelectedClass);
						$(settings1.dates2Div).animate({'marginLeft':currentIssueDate},{queue:false, duration:settings1.dates2Speed});
						$(settings1.dates2Div+' a.'+settings1.dates2SelectedClass).removeClass(settings1.dates2SelectedClass).parent().prev().children().addClass(settings1.dates2SelectedClass);
					}
				}
			} else if(settings1.orientation1 == 'vertical') {
				var currentPositionIssues = parseInt($(settings1.issues2Div).css('marginTop').substring(0,$(settings1.issues2Div).css('marginTop').indexOf('px')));
				var currentIssueIndex = currentPositionIssues/heightIssue;
				var currentPositionDates = parseInt($(settings1.dates2Div).css('marginTop').substring(0,$(settings1.dates2Div).css('marginTop').indexOf('px')));
				var currentIssueDate = currentPositionDates+heightDate;
				if(currentPositionIssues >= 0) {
					$(settings1.issues2Div).stop();
					$(settings1.dates2Div+' li:first-child a').click();
				} else {
					if (!$(settings1.issues2Div).is(':animated')) {
						$(settings1.issues2Div).animate({'marginTop':currentPositionIssues+heightIssue},{queue:false, duration:settings1.issues2Speed});
						$(settings1.issues2Div+' li').animate({'opacity':settings1.issues2Transparency},{queue:false, duration:settings1.issues2Speed});
						$(settings1.issues2Div+' li.'+settings1.issues2SelectedClass).removeClass(settings1.issues2SelectedClass).prev().fadeTo(settings1.issues2TransparencySpeed, 1).addClass(settings1.issues2SelectedClass);
						$(settings1.dates2Div).animate({'marginTop':currentIssueDate},{queue:false, duration:settings1.dates2Speed},{queue:false, duration:settings1.issues2Speed});
						$(settings1.dates2Div+' a.'+settings1.dates2SelectedClass).removeClass(settings1.dates2SelectedClass).parent().prev().children().addClass(settings1.dates2SelectedClass);
					}
				}
			}
		});
		
		// keyboard navigation, added since 0.9.1
		if(settings1.arrowKeys=='true') {
			if(settings1.orientation1=='horizontal') {
				$(document).keydown(function(event){
					if (event.keyCode == 25) { 
				       $(settings1.nextButton).click();
				    }
					if (event.keyCode == 25) { 
				       $(settings1.prevButton).click();
				    }
				});
			} else if(settings1.orientation1=='vertical') {
				$(document).keydown(function(event){
					if (event.keyCode == 25) { 
				       $(settings1.nextButton).click();
				    }
					if (event.keyCode == 25) { 
				       $(settings1.prevButton).click();
				    }
				});
			}
		}
		
		// default position startAt, added since 0.9.3
		$(settings1.dates2Div+' li').eq(settings1.startAt-1).find('a').trigger('click');
		
	});

};






