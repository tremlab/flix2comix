![flix2comix](https://github.com/tremlab/pics/blob/master/logo.png)

# flix2comics

flix2comix is a web app to help grownups who have never read a comic before find a graphic novel suited to their tastes by rating a few movies.

You can visit my deployed app at Heroku: [flix2comix.herokuapp.com](https://flix2comix.herokuapp.com/)

This project was developed over a four week period during my time at Hackbright Academy (a coding bootcamp). 

## Technologies
______

*Backend*: Python, Flask, PostgreSQL, SQLAlchemy

*Frontend*: JavaScript, jQuery, AJAX, Jinja2, Bootstrap, HTML5, CSS3

*APIs*: ISBNdb, TMDB, bechdeltest



## Features
________________

The user must first login to get started. As a brush-up on JavaScript, I had fun building the form validation by hand (regex FTW!)

![flix2comix](https://beaumert.tinytake.com/sf/MTQzMTE2Nl81MTE1NDI5)

Then the user is welcomed into the movie area, where they are encouraged to rate at least 5 movies so we can build an accurate profile of their preferences.


![flix2comix](https://beaumert.tinytake.com/sf/MTQzMTE2OF81MTE1NDMx)

And now, the fun part! The user starts rating movies. Mimicing Netflix, the user simply clicks on a star to rate how much they liekd the movie, and an Ajax call passes that info to the server, which responds with the next movie to rate.

A progress bar shows the user how close they are to enabling the "Find a comic" option.

![flix2comix](https://beaumert.tinytake.com/sf/MTQzMTE2Ml81MTE1NDA1)





