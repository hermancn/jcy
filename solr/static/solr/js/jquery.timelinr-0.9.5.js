/* ----------------------------------
jQuery Timelinr 0.9.3
Download by http://www.codefans.net
tested with jQuery v1.6+
?2011 CSSLab.cl
free for any use, of course... :D
instructions: http://www.csslab.cl/2011/08/18/jquery-timelinr21/
---------------------------------- */

jQuery.fn.timelinr3 = function(options){
	// default plugin settings2
	settings2 = jQuery.extend({
		orientation2: 				'horizontal',		// value: horizontal | vertical, default to horizontal
		containerDiv2: 				'#timeline3',		// value: any HTML tag or #id, default to #timeline3
		dates3Div: 					'#dates3',			// value: any HTML tag or #id, default to #dates3
		dates3SelectedClass: 		'selected3',			// value: any class, default to selected3
		dates3Speed: 				500,				// value: integer between 100 and 1000 (recommended), default to 500 (normal)
		issues3Div: 					'#issues3',			// value: any HTML tag or #id, default to #issues3
		issues3SelectedClass: 		'selected3',			// value: any class, default to selected3
		issues3Speed: 				200,				// value: integer between 100 and 1000 (recommended), default to 200 (fast)
		issues3Transparency: 		1,				// value: integer between 0 and 1 (recommended), default to 0.2
		issues3TransparencySpeed: 	500,				// value: integer between 100 and 1000 (recommended), default to 500 (normal)
		prevButton: 				'#prev',			// value: any HTML tag or #id, default to #prev
		nextButton: 				'#next',			// value: any HTML tag or #id, default to #next
		arrowKeys: 					'false',			// value: true/false, default to false
		startAt: 					8					// value: integer, default to 1 (first)
	}, options);

	$(function(){
		// setting variables... many of them
		var howManyDates = $(settings2.dates3Div+' li').length;
		var howManyIssues = $(settings2.issues3Div+' li').length;
		var currentDate = $(settings2.dates3Div).find('a.'+settings2.dates3SelectedClass);
		var currentIssue = $(settings2.issues3Div).find('li.'+settings2.issues3SelectedClass);
		var widthContainer = $(settings2.containerDiv2).width();
		var heightContainer = $(settings2.containerDiv2).height();
		var widthIssues = $(settings2.issues3Div).width();
		var heightIssues = $(settings2.issues3Div).height();
		var widthIssue = $(settings2.issues3Div+' li').width();
		var heightIssue = $(settings2.issues3Div+' li').height();
		var widthDates = $(settings2.dates3Div).width();
		var heightDates = $(settings2.dates3Div).height();
		var widthDate = $(settings2.dates3Div+' li').width();
		var heightDate = $(settings2.dates3Div+' li').height();
		
		// set positions!
		if(settings2.orientation2 == 'horizontal') {	
			$(settings2.issues3Div).width(widthIssue*howManyIssues);
			$(settings2.dates3Div).width(widthDate*howManyDates).css('marginLeft',widthContainer/2-widthDate/2);
			var defaultPositionDates = parseInt($(settings2.dates3Div).css('marginLeft').substring(0,$(settings2.dates3Div).css('marginLeft').indexOf('px')));
		} else if(settings2.orientation2 == 'vertical') {
			$(settings2.issues3Div).height(heightIssue*howManyIssues);
			$(settings2.dates3Div).height(heightDate*howManyDates).css('marginTop',heightContainer/2-heightDate/2);
			var defaultPositionDates = parseInt($(settings2.dates3Div).css('marginTop').substring(0,$(settings2.dates3Div).css('marginTop').indexOf('px')));
		}
		
		$(settings2.dates3Div+' a').click(function(event){
			event.preventDefault();
			// first vars
			var whichIssue = $(this).text();
			var currentIndex = $(this).parent().prevAll().length;

			// moving the elements
			if(settings2.orientation2 == 'horizontal') {
				$(settings2.issues3Div).animate({'marginLeft':-widthIssue*currentIndex},{queue:false, duration:settings2.issues3Speed});
			} else if(settings2.orientation2 == 'vertical') {
				$(settings2.issues3Div).animate({'marginTop':-heightIssue*currentIndex},{queue:false, duration:settings2.issues3Speed});
			}
			$(settings2.issues3Div+' li').animate({'opacity':settings2.issues3Transparency},{queue:false, duration:settings2.issues3Speed}).removeClass(settings2.issues3SelectedClass).eq(currentIndex).addClass(settings2.issues3SelectedClass).fadeTo(settings2.issues3TransparencySpeed,1);
			
			// now moving the dates3
			$(settings2.dates3Div+' a').removeClass(settings2.dates3SelectedClass);
			$(this).addClass(settings2.dates3SelectedClass);
			if(settings2.orientation2 == 'horizontal') {
				$(settings2.dates3Div).animate({'marginLeft':defaultPositionDates-(widthDate*currentIndex)},{queue:false, duration:settings2.dates3Speed});
			} else if(settings2.orientation2 == 'vertical') {
				$(settings2.dates3Div).animate({'marginTop':defaultPositionDates-(heightDate*currentIndex)},{queue:false, duration:settings2.dates3Speed});
			}
		});

		$(settings2.nextButton).bind('click', function(event){
			event.preventDefault();
			if(settings2.orientation2 == 'horizontal') {
				var currentPositionIssues = parseInt($(settings2.issues3Div).css('marginLeft').substring(0,$(settings2.issues3Div).css('marginLeft').indexOf('px')));
				var currentIssueIndex = currentPositionIssues/widthIssue;
				var currentPositionDates = parseInt($(settings2.dates3Div).css('marginLeft').substring(0,$(settings2.dates3Div).css('marginLeft').indexOf('px')));
				var currentIssueDate = currentPositionDates-widthDate;
				if(currentPositionIssues <= -(widthIssue*howManyIssues-(widthIssue))) {
					$(settings2.issues3Div).stop();
					$(settings2.dates3Div+' li:last-child a').click();
				} else {
					if (!$(settings2.issues3Div).is(':animated')) {
						$(settings2.issues3Div).animate({'marginLeft':currentPositionIssues-widthIssue},{queue:false, duration:settings2.issues3Speed});
						$(settings2.issues3Div+' li').animate({'opacity':settings2.issues3Transparency},{queue:false, duration:settings2.issues3Speed});
						$(settings2.issues3Div+' li.'+settings2.issues3SelectedClass).removeClass(settings2.issues3SelectedClass).next().fadeTo(settings2.issues3TransparencySpeed, 1).addClass(settings2.issues3SelectedClass);
						$(settings2.dates3Div).animate({'marginLeft':currentIssueDate},{queue:false, duration:settings2.dates3Speed});
						$(settings2.dates3Div+' a.'+settings2.dates3SelectedClass).removeClass(settings2.dates3SelectedClass).parent().next().children().addClass(settings2.dates3SelectedClass);
					}
				}
			} else if(settings2.orientation2 == 'vertical') {
				var currentPositionIssues = parseInt($(settings2.issues3Div).css('marginTop').substring(0,$(settings2.issues3Div).css('marginTop').indexOf('px')));
				var currentIssueIndex = currentPositionIssues/heightIssue;
				var currentPositionDates = parseInt($(settings2.dates3Div).css('marginTop').substring(0,$(settings2.dates3Div).css('marginTop').indexOf('px')));
				var currentIssueDate = currentPositionDates-heightDate;
				if(currentPositionIssues <= -(heightIssue*howManyIssues-(heightIssue))) {
					$(settings2.issues3Div).stop();
					$(settings2.dates3Div+' li:last-child a').click();
				} else {
					if (!$(settings2.issues3Div).is(':animated')) {
						$(settings2.issues3Div).animate({'marginTop':currentPositionIssues-heightIssue},{queue:false, duration:settings2.issues3Speed});
						$(settings2.issues3Div+' li').animate({'opacity':settings2.issues3Transparency},{queue:false, duration:settings2.issues3Speed});
						$(settings2.issues3Div+' li.'+settings2.issues3SelectedClass).removeClass(settings2.issues3SelectedClass).next().fadeTo(settings2.issues3TransparencySpeed, 1).addClass(settings2.issues3SelectedClass);
						$(settings2.dates3Div).animate({'marginTop':currentIssueDate},{queue:false, duration:settings2.dates3Speed});
						$(settings2.dates3Div+' a.'+settings2.dates3SelectedClass).removeClass(settings2.dates3SelectedClass).parent().next().children().addClass(settings2.dates3SelectedClass);
					}
				}
			}
		});

		$(settings2.prevButton).click(function(event){
			event.preventDefault();
			if(settings2.orientation2 == 'horizontal') {
				var currentPositionIssues = parseInt($(settings2.issues3Div).css('marginLeft').substring(0,$(settings2.issues3Div).css('marginLeft').indexOf('px')));
				var currentIssueIndex = currentPositionIssues/widthIssue;
				var currentPositionDates = parseInt($(settings2.dates3Div).css('marginLeft').substring(0,$(settings2.dates3Div).css('marginLeft').indexOf('px')));
				var currentIssueDate = currentPositionDates+widthDate;
				if(currentPositionIssues >= 0) {
					$(settings2.issues3Div).stop();
					$(settings2.dates3Div+' li:first-child a').click();
				} else {
					if (!$(settings2.issues3Div).is(':animated')) {
						$(settings2.issues3Div).animate({'marginLeft':currentPositionIssues+widthIssue},{queue:false, duration:settings2.issues3Speed});
						$(settings2.issues3Div+' li').animate({'opacity':settings2.issues3Transparency},{queue:false, duration:settings2.issues3Speed});
						$(settings2.issues3Div+' li.'+settings2.issues3SelectedClass).removeClass(settings2.issues3SelectedClass).prev().fadeTo(settings2.issues3TransparencySpeed, 1).addClass(settings2.issues3SelectedClass);
						$(settings2.dates3Div).animate({'marginLeft':currentIssueDate},{queue:false, duration:settings2.dates3Speed});
						$(settings2.dates3Div+' a.'+settings2.dates3SelectedClass).removeClass(settings2.dates3SelectedClass).parent().prev().children().addClass(settings2.dates3SelectedClass);
					}
				}
			} else if(settings2.orientation2 == 'vertical') {
				var currentPositionIssues = parseInt($(settings2.issues3Div).css('marginTop').substring(0,$(settings2.issues3Div).css('marginTop').indexOf('px')));
				var currentIssueIndex = currentPositionIssues/heightIssue;
				var currentPositionDates = parseInt($(settings2.dates3Div).css('marginTop').substring(0,$(settings2.dates3Div).css('marginTop').indexOf('px')));
				var currentIssueDate = currentPositionDates+heightDate;
				if(currentPositionIssues >= 0) {
					$(settings2.issues3Div).stop();
					$(settings2.dates3Div+' li:first-child a').click();
				} else {
					if (!$(settings2.issues3Div).is(':animated')) {
						$(settings2.issues3Div).animate({'marginTop':currentPositionIssues+heightIssue},{queue:false, duration:settings2.issues3Speed});
						$(settings2.issues3Div+' li').animate({'opacity':settings2.issues3Transparency},{queue:false, duration:settings2.issues3Speed});
						$(settings2.issues3Div+' li.'+settings2.issues3SelectedClass).removeClass(settings2.issues3SelectedClass).prev().fadeTo(settings2.issues3TransparencySpeed, 1).addClass(settings2.issues3SelectedClass);
						$(settings2.dates3Div).animate({'marginTop':currentIssueDate},{queue:false, duration:settings2.dates3Speed},{queue:false, duration:settings2.issues3Speed});
						$(settings2.dates3Div+' a.'+settings2.dates3SelectedClass).removeClass(settings2.dates3SelectedClass).parent().prev().children().addClass(settings2.dates3SelectedClass);
					}
				}
			}
		});
		
		// keyboard navigation, added since 0.9.1
		if(settings2.arrowKeys=='true') {
			if(settings2.orientation2=='horizontal') {
				$(document).keydown(function(event){
					if (event.keyCode == 25) { 
				       $(settings2.nextButton).click();
				    }
					if (event.keyCode == 25) { 
				       $(settings2.prevButton).click();
				    }
				});
			} else if(settings2.orientation2=='vertical') {
				$(document).keydown(function(event){
					if (event.keyCode == 25) { 
				       $(settings2.nextButton).click();
				    }
					if (event.keyCode == 25) { 
				       $(settings2.prevButton).click();
				    }
				});
			}
		}
		
		// default position startAt, added since 0.9.3
		$(settings2.dates3Div+' li').eq(settings2.startAt-1).find('a').trigger('click');
		
	});

};






