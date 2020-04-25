$(document).ready(function(){
	$("#fileBox").hide()
	$("#messageBox").hide()
	$("#messageformatfile").click(function(){
		$("#fileBox").show()
		$("#messageBox").hide()	
	});

	$("#messageformattext").click(function(){
		$("#messageBox").show()
		$("#fileBox").hide()
	});
});