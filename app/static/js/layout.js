$(document).ready(function(){
	$("#fileBox").hide()
	$("#messageBox").hide()
	$("#searchBox").hide()
	$("#submitButton").hide()
	$("#passphraseBox").hide()
	$("#messageformatfile").click(function(){
		$("#fileBox").show()
		$("#messageBox").hide()
		$("#submitButton").show()
	});
	$("#messageformattext").click(function(){
		$("#messageBox").show()
		$("#fileBox").hide()
		$("#submitButton").show()
	});

	$("#formSubmit").click(function(){
		var checked = $('input:checked').length;
		if (checked<2){
	        alert("Please check at least one of Encyption or Sign");
	        return false;
	    }
	});
	$("#encrypt").click(function(){
		if($("#searchBox").is(":visible")){
			$("#searchBox").hide()
		}else{
			$("#searchBox").show()
		}
	});
	$("#verify").click(function(){
		if($("#searchBox").is(":visible")){
			$("#searchBox").hide()
		}else{
			$("#searchBox").show()
		}
	});
	$("#decrypt").click(function(){
		if($("#passphraseBox").is(":visible")){
			$("#passphraseBox").hide()
		}else{
			$("#passphraseBox").show()
		}
	});
	$("#formSubmitDec").click(function(){
		var checked = $('input:checked').length;
		if (checked<2){
	        alert("Please check at least one of Decryption or Verify");
	        return false;
	    }
	});
});
