function addRating(type){
		var rating = {
			rate: $("#id_rate").val(),
			slug: $("#id_slug").val(),
		};
		jQuery.post("/resources/add_"+type+"_rating/",rating,
			function(response){
				if(response.succes == "True"){
					$("#id_rate_value").text(response.new_rate);
					$("#id_rate").fadeOut();
					$("#id_submit").fadeOut();
				}
			
			},"json");
		}; 

$(document).ready(function(){
	
	//Add professor field
	$('#id_subject').change(
	function addProfessor(){
		var subject = {
			subject: $("#id_subject").val(),
		};
		jQuery.post("/resources/add_resource_professor/",subject,
			function(response){
				if(response.succes == "True"){
					$("#professor_field").remove()
					$(response.html).insertAfter($("#id_subject").parent());
				}
			
			},"json");
		});    
		
	function statusBox(){
		$('<div id="loading">Carregando...</div>').insertAfter($("#id_subject"))
		.ajaxStart(function(){$(this).show();})
		.ajaxStop(function(){$(this).hide();})
		
	}
	statusBox();
	$("#id_subject").val("").attr('selected','selected');
});
