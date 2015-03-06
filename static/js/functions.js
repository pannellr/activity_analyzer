$( document ).ready(function() {

    $('.add-category').click(function(e){
	e.preventDefault();
	alert('click');
	// prepend category form elements
	$(this).prepend('<h2>form</h2>');
    });

});
