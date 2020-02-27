/**
	Void Mega Menu
**/


jQuery(window).on('load', function() {

	"use strict";

	/* ========== Sticky on scroll ========== */
	function stickyNav() {

		var	noSticky = $('.no-sticky'),
			viewportSm = $('.viewport-sm'),
			viewportLgNosticky = $('.viewport-lg.no-sticky'),
			viewportLgNostickyBody = viewportLgNosticky.parent('body'),
			headerTransparentLg = $('.viewport-lg.header-transparent'),
			headerTransparentLgBody = headerTransparentLg.parent('body'),
			headerOpacityLg = $('.viewport-lg.header-opacity'),
			headerOpacityLgBody = headerOpacityLg.parent('body');
		noSticky.removeClass('sticky');
		viewportSm.removeClass('sticky');
		headerTransparentLg.add(headerTransparentLgBody).add(headerOpacityLg).add(headerOpacityLgBody).add(viewportLgNostickyBody).add(viewportLgNosticky).css("margin-top", "0");

		var logoCenterWidth = $('.logoCenter .logo img').width(),
			menuCenterOneWidth = $('.center-menu-1 .vmm-menu').width(),
			menuCenterOneListMenu = $('.center-menu-1 .vmm-menu > ul'),
			menuCenterOneListWidth = menuCenterOneWidth - logoCenterWidth;

		if ($(window).width() < 1200) {
			menuCenterOneListMenu.outerWidth( menuCenterOneWidth );
		} else {
			menuCenterOneListMenu.outerWidth( menuCenterOneListWidth / 2 );
		}

		$('.logoCenter').width(logoCenterWidth);

	}



	/* ========== Horizontal navigation menu ========== */
	if ($('.vmm-header').length) {

		var vmmHeader = $('.vmm-header'),
			logo = vmmHeader.find('.logo'),
			logoImg = logo.find('img'),
			logoSrc = logoImg.attr('src'),
			logoClone = logo.clone(),
			mobileLogoSrc = logo.data('mobile-logo'),
			burgerMenu = vmmHeader.find('.burger-menu'),
			vmmMenuListWrapper = $('.vmm-menu > ul'),
			vmmMenuListDropdown = $('.vmm-menu ul li:has(ul)'),
			headerShadow = $('.vmm-header.header-shadow'),
			headerTransparent = $('.vmm-header.header-transparent'),
			headerOpacity = $('.vmm-header.header-opacity'),
			megaMenuFullwidthContainer = $('.mega-menu-fullwidth .mega-menu-container');

		/* ========== Center menu 1 ========== */
		$('.center-menu-1 .vmm-menu > ul:first-child').after('<div class="logoCenter"></div>');
		$('.logoCenter').html(logoClone);

		/* ========== Mega menu fullwidth wrap container ========== */
		megaMenuFullwidthContainer.each(function(){
			$(this).children().wrapAll('<div class="mega-menu-fullwidth-container"></div>');
		});

		/* ========== Window resize ========== */
		$(window).on("resize", function() {

			var megaMenuContainer = $('.mega-menu-fullwidth-container');

			if ($(window).width() < 1200) {

				logoImg.attr('src', mobileLogoSrc);
				vmmHeader.removeClass('viewport-lg');
				vmmHeader.addClass('viewport-sm');
				headerTransparent.removeClass('header-transparent-on');
				headerOpacity.removeClass('header-opacity-on');
				megaMenuContainer.removeClass('container');

			} else {

				logoImg.attr('src', logoSrc);
				vmmHeader.removeClass('viewport-sm');
				vmmHeader.addClass('viewport-lg');
				headerTransparent.addClass('header-transparent-on');
				headerOpacity.addClass('header-opacity-on');
				megaMenuContainer.addClass('container');

			}

			stickyNav();

		}).resize();

		/* ========== Dropdown Menu Toggle ========== */
		burgerMenu.on("click", function(){
			$(this).toggleClass('menu-open');
			vmmMenuListWrapper.slideToggle(300);
		});

		vmmMenuListDropdown.each(function(){
			$(this).append( '<span class="dropdown-plus"></span>' );
			$(this).addClass('dropdown_menu');
		});

		$('.dropdown-plus').on("click", function(){
			$(this).prev('ul').slideToggle(300);
			$(this).toggleClass('dropdown-open');
		});

		$('.dropdown_menu a').append('<span></span>');

		/* ========== Added header shadow ========== */
		headerShadow.append('<div class="header-shadow-wrapper"></div>');

		/* ========== Sticky on scroll ========== */
		$(window).on("scroll", function() {
			stickyNav();
		}).scroll();

		/* ========== Menu hover transition ========== */
		var listMenuHover4 = $('.vmm-menu.menu-hover-4 > ul > li > a');
		listMenuHover4.append('<div class="hover-transition"></div>');

	}

	/* ========== Menu icon color ========== */
	$('.vmm-menu-icon').css('color', function () {
		var iconColorAttr = $(this).data('fa-color');
		return iconColorAttr;
	});


	if ($('.vmm-menu ul li ul li').closest('li').has('ul').length) {
        $('.vmm-menu ul li ul li.dropdown_menu').addClass('vmm3rdchild');
    }

	$('li.dropdown_menu.vmm3rdchild').on('click', function(){
		$(this).toggleClass('vm3rshow');
	});
});