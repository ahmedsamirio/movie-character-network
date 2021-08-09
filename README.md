# Movie Maps

A web app deployed on herkou that graphs a network of characters in a movie according to their interactions inferred from their dialogue in the movie script.

## Installation

All extra libraries required to run the app locally are present in `requirement.txt`, also all the nltk packages required are present in `nltk.txt`.

There is a python virutal environment that you can activate directly using `source characternetworkenv/bin/activate`.

## Project Motivation

This is a little project that I did to learn more about deploying webapps, network graphs and nlp. I didn't aim to make a perfect application that correctly graphs interactions between characters in any movie script, nor do I think that it's possible since there are many variations in any given script that reduces the ability of hard rules to infer such interactions. 

That doesn't mean that you can't dissect a single movie script and graph the interactions in a very meticulous way, but it rather restricts any thought that this dissection would generalize to every other script out there, as evident by this web app.

This project is rather a fun way to look into the movies you love and see how they are different from each other using their network graphs, as some movies can have multiple storylines, which can be evident in their networks, like the movie "Babel" or "The Lord of The Rings: The Two Towers"

[babel](https://ahmedsamirio.github.io/images/network/babel.png)
[lotr](https://ahmedsamirio.github.io/images/network/lotr.png)

And some movies can be really centralized around one character like "Thor: Ragnarok".

[thor](https://ahmedsamirio.github.io/images/network/thor.png)

## File Descriptions

1. `moviemapsapp/`: A module for the flask web app
2. `moviemapsenv/`: A python virutal environment the contains all dependencies
3. `data/`: All the movie scripts downloaded from IMSDB
4. `wrangling_scripts/`: A module containing scraping, text cleaning, network preparation and graphing functions
5. `Procfile`: A file that tells heroku what do when starting the web app
6. `moviemaps.py`: A script that runs the web app 
7. `nltk.txt`: A text file containing the nltk downloadable packages for heroku
8. `requirements.txt`: A text file containing the dependencies for running the web app

## Usage

You can tinker with the deployed web app in here https://movie-maps.herokuapp.com/.

If you are up to it you can clone this repo and customize the web app's interface, or customize the network grapsh themselves or how they are made and run the web app locally. However, in order to run the web app locally, you have to uncomment this line `app.run(host='0.0.0.0', port=3000, debug=True)` in `moviemaps.py`.

You can also read this [blog post](https://ahmedsamirio.github.io/2021-8-9-Movie-Maps/) if you want to understand more about the flow of the code.

