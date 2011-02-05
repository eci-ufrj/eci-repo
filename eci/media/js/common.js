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
	//fancybox add_professor_form POST logic
	$("#add_professor_form").bind("submit", function() {
				if (!$('#name_verify').is(":visible")) {
					var form_data = $('#add_professor_form').serialize();
					jQuery.post("/resources/add_professor/", form_data, function(response){
						if (response.succes == "True") {
							$('#professor_div').slideUp();
							$(response.html).insertAfter($("#professor_div"));
							$('#add_professor_succes').slideDown();
						}
						if (response.succes == "True") {
							$('#id_professor').append($('<option></option>').val(response.id_professor).html(response.name_professor));
						}
						if (response.error) {
							$('#p_name_error').html(response.error);
						}
					}, "json");
					
				}
					return false;
				
				});
	
	//Add professor field
	$('#id_subject').change(
	function addProfessor(){
		var subject = {
			subject: $("#id_subject").val(),
		};
		$('#div_loading').slideDown();
		jQuery.post("/resources/add_resource_professor/",subject,
			function(response){
				if(response.succes == "True"){
					$("#professor_field").remove()
					$(response.html).insertAfter($("#id_subject").parent());
				}
				$("#add_professor").fancybox({
					'scrolling'		: 'no',
					'titleShow'		: false,
					'onClosed'		: function() {
					    $("#login_error").hide();
					}
				});	
				$("#fancybox-content").css({'border-color':'#608E9D'});
				$("#add_professor_subject").html($("#id_subject option:selected").text());
				$("#add_professor_subject_input").val($("#id_subject option:selected").val());
				
			},"json");
			$('#div_loading').ajaxStop(function(){$(this).slideUp();})
		});    
	
	/*function statusBox(){
		$('<div id="loading">Carregando...</div>').insertAfter($("#id_subject"))
		.ajaxStart(function(){$(this).show();})
		.ajaxStop(function(){$(this).hide();})
		
	}
	statusBox();*/
	$("#id_subject").val("").attr('selected','selected');
	
});
