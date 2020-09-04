/* This function shows or hides the next "button"
depending on validations made to the field*/
function showNextButton(button_id, status){
	var button_id_element = document.getElementById(button_id);
	if (status == 'show'){
		button_id_element.style.display = "initial";
	}
	else{
		button_id_element.style.display = "none";
	}
}

function validateEmpty(field_id, button_id){
	var userInput = document.getElementById(field_id);
	userInput.addEventListener("input",

	function() {
		if (userInput.value != ""){
			showNextButton(button_id, 'show');
		}
		else{
			showNextButton(button_id, 'dont_show');
		}
});
}

function validatePhoneNumber(phone_number_id, phone_number_errors, phone_number_button = ''){
	var phoneNumber = document.getElementById(phone_number_id);
	var error_div = document.getElementById(phone_number_errors);
	phoneNumber.addEventListener("input",

	function(){
		if(phoneNumber.value.match(/^07\d{8}$/g)){
			error_div.innerHTML = "";
			if(phone_number_button !=''){
				showNextButton(phone_number_button, 'show');
			}
		}
		else{
			error_div.innerHTML = "Use this format: 07XXXXXXXX";
			if(phone_number_button != ''){
				showNextButton(phone_number_button, 'dont_show');
			}
		}
	});
}


function validatePassword(password_id, password_error_div, password_button){
	var password = document.getElementById(password_id);
	var password_error_div = document.getElementById(password_error_div);
	password.addEventListener("input",
		function(){
			if(password.value.length >= 8){
				password_error_div.innerHTML = "";
				showNextButton(password_button, 'show');
			}
			else{
				password_error_div.innerHTML = "Your password has to be at least 8 characters.";
				showNextButton(password_button, 'dont_show');
			}
		});
}

/*prevent submission through enter key*/
document.addEventListener("keydown",
function(e){
	if(e.keyCode == 13){
		e.preventDefault();
	}
}
);