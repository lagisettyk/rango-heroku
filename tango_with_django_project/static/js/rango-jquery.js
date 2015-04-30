$(document).ready(function() {

    // JQuery code to related to rango application to be added in here.
    // For all the JQury commands they follow a similar pattern: Select & Act
    // Select an element, and then act on the element
    
    $("#about-btn").addClass('btn btn-primary')

    $("#about-btn").click( function(event) {
    alert("You clicked the button using JQuery!");
	});

	$("#about-btn").click( function(event) {
		msgstr = $("#msg").html()
        msgstr = msgstr + " Kiran!!!"
        $("#msg").html(msgstr)
 	});

    // Example for ajax functionality with JQuery...
 	$('#likes').click(function(){
	    var catid;
	    catid = $(this).attr("data-catid");
	    $.get('/rango/like_category/', {category_id: catid}, function(data){
	               $('#like_count').html(data);
	               $('#likes').hide();
	    });
	});


	$("p").hover( function() {
            $(this).css('color', 'red');
    },
    function() {
            $(this).css('color', 'blue');
    });

});