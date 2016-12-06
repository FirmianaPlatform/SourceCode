/*window.onscroll = function(){
        var t = document.documentElement.scrollTop || document.body.scrollTop;
        var div_up = document.getElementById("uptop");
        t > 300 ? div_up.style.display="block" : div_up.style.display="none";
    }
 */
function scroTop() {
	document.body.scrollTop = document.documentElement.scrollTop = 0;
}
/*
var naviga_offsetTop = 0;

function my_getElementsByClassName(class_name) {
	var el = [];

	_el = document.getElementsByTagName('*');

	for (var i = 0; i < _el.length; i++) {
		if (_el[i].className == class_name) {
			el[el.length] = _el[i];
		}
	}
	return el;
}

function naviga_stay_top() {
	var a_navigation_bar = [];
	if (document.getElementsByClassName) {//Chrome, FF 
		a_navigation_bar = document.getElementById("stay");
	} else {//IE 
		a_navigation_bar = my_getElementsByClassName("content");
	}
	var scrollTop = document.body.scrollTop
			|| document.documentElement.scrollTop;

	if (scrollTop > naviga_offsetTop) {
		a_navigation_bar.style.marginTop = scrollTop + "px";
	} else {
		a_navigation_bar.style.marginTop = naviga_offsetTop + "px";
	}
}

window.onload = function() {

	var a_navigation_bar = [];
	if (document.getElementsByClassName) {//Chrome, FF 
		a_navigation_bar = document.getElementById("stay");
	} else {//IE 
		a_navigation_bar = my_getElementsByClassName("navigation");
	}
	naviga_offsetTop = a_navigation_bar.offsetTop;

	// window.onscroll= naviga_stay_top; 
	// document.onmousewheel= naviga_stay_top; 
	if (window.attachEvent) //IE 
	{
		window.attachEvent("onmousewheel", naviga_stay_top);
		window.attachEvent("onscroll", naviga_stay_top);

		document.attachEvent("onmousewheel", naviga_stay_top);
		document.attachEvent("onscroll", naviga_stay_top);
	} else {//Chrome ,FF 
		window.addEventListener("mousewheel", naviga_stay_top, false);
		window.addEventListener("scroll", naviga_stay_top, false);

		document.addEventListener("mousewheel", naviga_stay_top, false);
		document.addEventListener("scroll", naviga_stay_top, false);
	}

}*/