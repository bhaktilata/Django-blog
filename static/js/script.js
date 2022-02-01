$(document).ready(function () {
    $('.navbar-collapse a').each(function(){
        let location = window.location.protocol + '//' + window.location.host + window.location.pathname;
        let link = this.href;
        if(location == link){
            $(this).parent().addClass('active');
        }
    });
});

$('ul.dropdown-menu [data-toggle=dropdown]').on('click', function (event) {
 // Avoid following the href location when clicking
  event.preventDefault();
        // Avoid having the menu to close when clicking
  event.stopPropagation();
        // If a menu is already open we close it
  $('ul.dropdown-menu [data-toggle=dropdown]').parent().removeClass('open');
        // opening the one you clicked on
  $(this).parent().addClass('open');
 });
