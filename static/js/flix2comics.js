// flix2comix.js
"use strict"


document.addEventListener ("DOMContentLoaded", function() 
    {
        $('#loginForm > input').on('focus', fHandleEnter);   // toggle?
        $('#registerForm > input').on('focus', fHandleEnter);   // toggle?
        $('#loginForm > input').on('blur', fHandleExit);
        $('#registerForm > input').on('blur', fEnableSubmit);

        $('#signUpButton').on('click', fDisplayRegForm);
        $('#cancelReg').on('click', fHideRegForm);
        $('#loginButton').on('click', fDisplayLoginForm);
        $('#cancelLogin').on('click', fHideLoginForm);
        $('#editUserButton').on('click', fDisplayUserForm);
        $('#cancelEditUser').on('click', fHideUserForm);

        $('#email').on('blur', fValidateEmail);
        $('#password2').on('blur', fPasswordsMatch);

        $('#startButton').on('click', fGetMovie);
        $('#startButton').on('click', function () {$('#intro').hide()});

        $('.monkey > p').on('click', function () {console.log('click star')});


    } // closes anon function
); // closes DOM event listener

console.log("connected!!!!!!!");


function fGetMovie(evt) {
    $.get('/getMovie', fDisplayMovie);
    console.log('click start');
}

function fDisplayMovie(results) {
    $('#movieStars').html(results);
}

function fRateMovie(evt) {
    console.log(this);

    // var formInputs = {
    //     "movie_id": $(this).data("movie"),
    //     "rating": $(this).data("rating")
    // };
    // console.log(movie_id);

    // $.post('/rate', formInputs, fDisplayMovie)

}

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

function fDisplayUserForm(evt) {
    $('#editUserForm').removeClass('hidden');
    $('#editUserButton').hide();
    console.log("clicky reg");
}

function fHideUserForm(evt) {
    $('#editUserForm').addClass('hidden');
    $('#editUserButton').show();
    console.log("clicky cancel");
}


function fEnableSubmit(evt) {
    if (
        $('#email').val().length > 0 && 
        $('#password').val().length > 0 &&
        $('#password').val() === $('#password2').val()
        // confirm email ok?
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