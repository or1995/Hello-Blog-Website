var searchinput = document.getElementById("id_search");
var burgericon = document.querySelector(".burgericon");
var shade = document.querySelector(".shade");

searchinput.addEventListener("keyup", function(event) {
  	if (event.keyCode === 13) {
    	event.preventDefault();
    	document.querySelector(".searchbutton").click();
  	}
});

burgericon.addEventListener("click", function() {
	document.querySelector(".content-sidebar").classList.add("shownsidebar");
	document.querySelector(".shade").classList.add("showshade");
})

shade.addEventListener("click", function() {
	document.querySelector(".content-sidebar").classList.remove("shownsidebar");
	document.querySelector(".shade").classList.remove("showshade");
})

