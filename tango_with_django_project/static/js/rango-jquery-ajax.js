$(document).ready( function() {

    // JQuery code to related to rango application to be added in here.
    // For all the JQury commands they follow a similar pattern: Select & Act
    // Select an element, and then act on the element
    // Code aalso reflects ajax functions...

    $("#about-btn").addClass('btn btn-primary')

    $("#about-btn").click( function(event) {
    alert("You clicked the button using JQuery!");
	});

	$("#about-btn").click( function(event) {
		msgstr = $("#msg").html()
        msgstr = msgstr + " Kiran!!!"
        $("#msg").html(msgstr)
 	});

    $("p").hover( function() {
            $(this).css('color', 'red');
    },
    function() {
            $(this).css('color', 'blue');
    });


    // Example for ajax functionality with JQuery...
 	$('#likes').click( function(){
	    var catid;
	    catid = $(this).attr("data-catid");
	    $.get('/rango/like_category/', {category_id: catid}, function(data){
	               $('#like_count').html(data);
	               $('#likes').hide();
	    });
	});

	$('#suggestion').keyup( function(){
		var query;
		query = $(this).val();
		$.get('/rango/suggest_category/', {suggestion: query}, function(data){
			$('#cats').html(data);
		});// end block of get frunction
	}); // end block for keyup function...

	// JQuery for adding auto page to the category.html...
	/*$('.rango-add').click( function(){
		//alert("You clicked the button using JQuery! rango-add");
		var catid = $(this).attr("data-catid");
		var url = $(this).attr("data-url")
		var title = $(this).attr("data-title")
		$.get('/rango/auto_add_page/', {category_id: catid, url:url, title:title}, function(data){
			$('#pages').html(data);
          	me.hide();
		)};
	});//end block for click function...*/

   $('.rango-add').click(function(){
   	  //alert("You clicked the button using JQuery! rango-add");
   	  var catid = $(this).attr("data-catid");
      //var title = $(this).atrr("data-title");
      var url = $(this).attr("data-url");
   	  $.get('/rango/auto_add_page', {category_id: catid, url: url, title: "title-###"}, function(data){
        $('#pages').html(data);
        me.hide();
      });
      /*var catid = $(this).attr("data-catid");
      var title = $(this).atrr("data-title");
      var url = $(this).attr("data-url");
      $.get('/rango/auto_add_page/', {category_id: catid, url: url, title: title}, function(data){
          $('#pages').html(data);
          me.hide();
      });*/
    });


}); //end of ready function