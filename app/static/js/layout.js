$(document).ready(function(){
	$("#fileBox").hide()
	$("#messageBox").hide()
	$("#searchBox").hide()
	$("#submitButton").hide()
	$("#messageformatfile").click(function(){
		$("#fileBox").show()
		$("#messageBox").hide()
		$("#searchBox").show()
		$("#submitButton").show()	
	});

	$("#messageformattext").click(function(){
		$("#messageBox").show()
		$("#fileBox").hide()
		$("#searchBox").show()
		$("#submitButton").show()
	});
});