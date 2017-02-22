// flix2comix.js
"use strict"

document.addEventListener ("DOMContentLoaded", function() 
    {
        $('input').on('focus', fHandleEnter);   // toggle?
        $('input').on('blur', fHandleExit);
        $('input').on('blur', fEnableSubmit);

        $('#signUpButton').on('click', fDisplayRegForm);
        $('#cancelReg').on('click', fHideRegForm);
        $('#loginButton').on('click', fDisplayLoginForm);
        $('#cancelLogin').on('click', fHideLoginForm);

        $('#email').on('blur', fValidateEmail);
        $('#password2').on('blur', fPasswordsMatch);
    } // closes anon function
); // closes DOM event listener

console.log("connected!!!!!!!");

function fHandleEnter(evt) {
    $(this).addClass("highlight");
}

function fHandleExit(evt) {
    $(this).removeClass("highlight");
}

function fDisplayRegForm(evt) {
    $('#registerForm').removeClass('hidden');
    $('#notSignedIn').hide();
    console.log("clicky reg");
}

function fHideRegForm(evt) {
    $('#registerForm').addClass('hidden');
    $('#notSignedIn').show();
    console.log("clicky cancel");
}

function fDisplayLoginForm(evt) {
    $('#loginForm').removeClass('hidden');
    $('#notSignedIn').hide();
    console.log("clicky login");
}

function fHideLoginForm(evt) {
    $('#loginForm').addClass('hidden');
    $('#notSignedIn').show();
    console.log("clicky cancel login");
}

function fPasswordsMatch(evt) {
    if ($('#password').val() === $('#password2').val()) {
        $('#passMatch').empty();        
    }

    else {
        $('#passMatch').html('<p>passwords do not match. :(</p>');
    }
}
// TEST!!!!!!!!!!!!!!!
function fValidateEmail(evt) {
    var emailInput = $('#email').val();
    if (emailInput.length > 0) {
        var emailRegEx = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        if (emailRegEx.test(emailInput)) {
            $('#emailValid').empty();        
        }

        else {
            $('#emailValid').html('<p>please enter a valid email. :(</p>');
        }
    }
}


function fEnableSubmit(evt) {
    if (
        $('#email').val().length > 0 && 
        $('#password').val().length > 0 &&
        //$('#emailValid').length == 0 &&
        $('#password').val() === $('#password2').val()
    )
        {
        $('#registerButton').prop('disabled', false);
        }

}

// function isNotEmpty(inputElm, errMsg, errElm) {
//    var isValid = (inputElm.val().trim() !== "");
//    postValidate(isValid, errMsg, errElm, inputElm);
//    return isValid;
// }