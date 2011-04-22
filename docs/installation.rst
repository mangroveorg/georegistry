



Installing Georegistry:
=======================
Georegistry requires MongoDB, Python, PostgreSQL, Django, and a variety of
related dependences.  It also requires a web server to run in a production mode.

This document outlines Georegistry configuration for on Ubuntu 10.10 Linux
system running Apache2 as the web server. you may need to adjust these
directions slighly or significantly to get the service to run on other flavors
of Linux, Unix, Mac OS X, or Windows.


MongoDB Setup:
==============

Georegistry requires MongoDB and for special geospatial indicies to be created.
Follow the steps below carefully.

Install MongoDB:
----------------
Install mongo on your system.
::
    wget http://fastdl.mongodb.org/linux/mongodb-linux-x86_64-1.8.0.tgz
    tar zxvf mongodb-linux-x86_64-1.8.0.tgz
    cd mongodb-linux-x86_64-1.8.0/bin

Make a directory for the data.  We are using the directory /home/alan/.data as
an example.  The point is to create a directory to hold the data files.
::
    mkdir /home/alan/.data/

Start the database:
:: 
    ./mongod --dbpath=/home/alan/.data/
    
I like to add a line in my .basrc to easily start MongoDB. (adjust for your
environment)
::
    alias mgdb='/home/alan/.bin/mongodb-linux-x86_64-1.8.0/bin/mongod --dbpath=/home/alan/.data/'

To re-read baschrc without opening anew window, type:
::
    source .bashrc

Create the Necessary Indecies:
------------------------------
Enter the Mongo shell and connect to your database and collection.  We are
assuming the names georegistry02/georegistry02 respecitvley.
::
    >mongo
    db = connect("localhost/georegistry02");
    use georegistry02;


Create the necessary indecies. Do this for your main, historical, and verified
collections.  These should correspond to the values in the settings.py file
which is part of the Georegistry Django application.
::
    db.geometry_coordinates.ensureIndex( { loc : "2d" } )
    db.<collection_name>.ensureIndex( { geometry_coordinates : "2d" } )
    db.<collection_name>.ensureIndex( { 'country_code' : 1 } )
    db.<collection_name>.ensureIndex( { 'id' : 1 } )
    db.<collection_name>.ensureIndex( { 'classifiers.subcategory' : 1 } );
    db.<collection_name>.ensureIndex( { 'classifiers.category' : 1 } );
    db.<collection_name>.ensureIndex( { 'classifiers.type' : 1 } );

Just as an FYI, here is how to display everything in the collection as JSON.
::
    db.<collection_name>.find().forEach(printjson);


Install prerequisites for Georegistry:
======================================
These instruction may need to be modified based on your flavor/version of
Linux/Unix.

For example, you could install python-imaging with pip, by typing:
::
    sudo pip install PIL
 
...or you could install it via a Linux distrobution package such as Ubuntu 10.10
::
    sudo apt-get install python-imaging



Setup on Ubuntu 10.10:
----------------------
Grab the necessary prerequisite Ubuntu packages
::
    sudo apt-get update
    sudo apt-get install python-imaging git-core build-essental python2.6-dev python-setuptools libdecodeqr0 libdecodeqr-dev libqrencode3 libqrencode-dev
    sudo easy_install pip

Install Django 1.3
::
    sudo pip install Django
    
Download the Georegistry application:
::
    git clone git://github.com/mvpdev/georegistry.git
    cd georegistry

Install more prereqiusites per the requirements file:
::
    sudo pip install -r requirements.txt

Create the database
::
    python manage.py syncdb
    
Run the development server:
::
    python managae.py runserver


Now that you have the server running in a develoment environment.  See
georegistry/apache/READE.rst for instructions to congigure the application with Apache2.

Notes for Max OSX Users:
------------------------

These tips may help setup qrencode, whih requires some C libraries.
::
    brew install qrencode
    env DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH ARCHFLAGS="-arch x86_64" pip install -r requirements.txt
or
::
    brew install qrencode
    pip install -r requirements.txt