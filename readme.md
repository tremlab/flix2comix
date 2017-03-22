![flix2comix](https://github.com/tremlab/pics/blob/master/logo.png)

# flix2comics

flix2comix is a web app to help grownups who have never read a comic before find a graphic novel suited to their tastes by rating a few movies.

You can visit my deployed app at Heroku: [flix2comix.herokuapp.com](https://flix2comix.herokuapp.com/)

This project was developed over a four week period during my time at Hackbright Academy (a coding bootcamp). 

______

## Technologies

*Backend*: Python, Flask, PostgreSQL, SQLAlchemy

*Frontend*: JavaScript, jQuery, AJAX, Jinja2, Bootstrap, HTML5, CSS3

*APIs*: ISBNdb, TMDB, bechdeltest


________________
## Features

The user must first login to get started. As a brush-up on JavaScript, I had fun building the form validation by hand (regex FTW!)

![flix2comix](https://github.com/tremlab/pics/blob/master/register.png)

Then the user is welcomed into the movie area, where they are encouraged to rate at least 5 movies so we can build an accurate profile of their preferences.


![flix2comix](https://github.com/tremlab/pics/blob/master/intro.png)

And now, the fun part! The user starts rating movies. Mimicing Netflix, the user simply clicks on a star to rate how much they liked the movie, and an Ajax call passes that info to the Flask server, which responds with the json for next movie to rate.

A progress bar shows the user how close they are to enabling the "Find my comic" option.

![flix2comix](https://github.com/tremlab/pics/blob/master/madmax.png)

Once they've rated more than 5 movies, the magic happens! Clicking "Find my comic" brings the user to their first graphic novel recommendation.

![flix2comix](https://github.com/tremlab/pics/blob/master/summer.png)

This book is the logged in the users profile for future reference, and then the user can click to get the second closest matching book, and so on.

________________
## Under the Hood

The front-end of this app is pretty straightforward, but alot of effort and love went into the data structure and alogrithm. 

I could have used randomized, pseudo-user data, to mimic a Netflix/Spotify/Amazon type functionality, but since I really do want this app to help people find a graphic novel they will like - from day one - I decided to use a small data set of rich, well-thought-out rankings to compare movies to comics.

This was one of the most fun aspects of my project. I enlisted the help of my many film & comic buff friends to help me "type" each piece of media in a Survey Monkey survey. 

![flix2comix](https://github.com/tremlab/pics/blob/master/survey.png)

By defining qualites that both movies and comics share, I am able to extract trends from which movies the user loves or hates, average that out to a unique user profile, and then find a comic that most closely matches.

I have plenty of work to do on this front! Once I build an admin page, it will be much easier for my colleagues to add new media on the fly, which will allow for more diverse choices for the user.  And then I will be free to tighten up the algorithm with more subtle weighting.

________________
## New Features

In my next phase I plan to:

- Implement React on the front end.
- Build out a smarter user page, where users can rank comics, and edit/delete previous movie ratings.
- Email users with their comic recommendation, and a follow up email two weeks later to see how they liked their comic.
- Build an admin page for superusers to add/update media content.
- hash passwords.
- Allow users to tweet their comic discovery.


________________
## Acknowledgements

![flix2comix](https://github.com/tremlab/pics/blob/master/thanks.png)







