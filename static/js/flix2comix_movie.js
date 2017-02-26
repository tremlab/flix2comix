// flix2comix.js
"use strict"


document.addEventListener ("DOMContentLoaded", function() 
    {
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

