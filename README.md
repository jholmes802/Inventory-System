# 1073-Inventory-System
 FRC Part Inventory System.
 This is intended to make managing a stock of parts easier for FRC teams, and other organizations alike. 
 This project is aimed at being open-source so developers can modify parts to best fit their uses.

## How does it work/What is the flow
This uses a python http.server webserver hosted at either localhost:80 or localhost:8080 based on operating system.

AS it stands there /src/main_server.py is what runs and hosts the server. It processes all http transfers/calls.
The server makes called to a few objects either...
    -/src/posts.py which handels the data being sent back and forth.
    -/src/pages.py creates pages from a bank of functions.
    - The server also reads certain files direct from a file under /web/ these are fonts, css, and js files.

There are other python files used to manage data input and output, database management(done with SQLAlchemy) and other functions.

## How do i start?
Well its a simple as ensureing the requirements.txt is installed. Using...
> python -m pip install -r requirements.txt

The primary web server is run from /src/main_server.py
Running this in a terminal will show the address it is being served at.
This can be set by the user by changing the host var in the file.
If it is only to run on that computer without a network, then "localhost" is fine.
It should be set to "localhost" currently.


