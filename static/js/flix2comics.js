// flix2comix.js


// $( function() {
//     // onload....
//     // all event listeners here
    $('input').on('focus', highlight);
    $('input').on('blur', unhighlight);

    $('#password2').on('blur', passwordsMatch);


// }

console.log("connected!!!!!!!");

function highlight(evt) {
    $(this).addClass("highlight");
}

function unhighlight(evt) {
    $(this).removeClass("highlight");
}

function passwordsMatch(evt) {
    if ($('#password').val() === $('#password2').val()) {
        $('#passMatch').empty();        
    }

    else {
        $('#passMatch').html('<p>passwords do not match. :(</p>')
    }
}

// function isNotEmpty(inputElm, errMsg, errElm) {
//    var isValid = (inputElm.val().trim() !== "");
//    postValidate(isValid, errMsg, errElm, inputElm);
//    return isValid;
// }