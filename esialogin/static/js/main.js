(function () {
	"use strict";
	$('.sl-button1').click(function(){
		$('body').toggleClass('sl-en');
		$('.sl1').toggleClass('nodisplay');
		$('.sl0').toggleClass('nodisplay');
		document.cookie = "slver=1;path=/";
	});
	$('.sl-button0').click(function(){
		$('body').toggleClass('sl-en');
		$('.sl1').toggleClass('nodisplay');
		$('.sl0').toggleClass('nodisplay');
		$('body').removeClass('sl-1');
		$('body').removeClass('sl-2');
		document.cookie = "slver=0;path=/";
	});
	$('.sl-f0').click(function(){
		$('body').removeClass('sl-1');
		$('body').removeClass('sl-2');
		document.cookie = "fontsize=0;path=/";
	});
	$('.sl-f1').click(function(){
		$('body').toggleClass('sl-1');
		$('body').removeClass('sl-2');
		document.cookie = "fontsize=1;path=/";
	});
	$('.sl-f2').click(function(){
		$('body').removeClass('sl-1');
		$('body').toggleClass('sl-2');
		document.cookie = "fontsize=2;path=/";
	});

	var treeviewMenu = $('.app-menu');

	// Toggle Sidebar
	$('[data-toggle="sidebar"]').click(function(event) {
		event.preventDefault();
		$('.app').toggleClass('sidenav-toggled');
	});

	// Activate sidebar treeview toggle
	$("[data-toggle='treeview']").click(function(event) {
		event.preventDefault();
		if(!$(this).parent().hasClass('is-expanded')) {
			treeviewMenu.find("[data-toggle='treeview']").parent().removeClass('is-expanded');
		}
		$(this).parent().toggleClass('is-expanded');
	});

	// Set initial active toggle
	$("[data-toggle='treeview.'].is-expanded").parent().toggleClass('is-expanded');

	//Activate bootstrip tooltips
	$("[data-toggle='tooltip']").tooltip();


})();

function readCookie(name) {
	var nameEQ = encodeURIComponent(name) + "=";
	var ca = document.cookie.split(';');
	for (var i = 0; i < ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0) === ' ')
			c = c.substring(1, c.length);
		if (c.indexOf(nameEQ) === 0)
			return decodeURIComponent(c.substring(nameEQ.length, c.length));
	}
	return null;
}