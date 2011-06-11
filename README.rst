georegistry - The Geospatial Health RESTful Webservice
=============================================================

Written By: Alan Viars, et. al.

Copyright 2011 Columbia Univeristy / The Earth Institute



MongoDB Setup:
==============
Install MongoDB
::
    wget http://fastdl.mongodb.org/linux/mongodb-linux-x86_64-1.8.2.tgz
    tar zxvf mongodb-linux-x86_64-1.6.5.tgz
    cd mongodb-linux-x86_64-1.6.5/bin

Start the database:
:: 
    ./mongod --dbpath=/home/alan/.data/
    
I like to add a line in my .basrc to easily start MongoDB
::
    alias mgdb='/home/alan/.bin/mongodb-linux-x86_64-1.8.2/bin/mongod --dbpath=/home/alan/.data/'


Enter the Mongo shell
::
    >mongo
    db = connect("localhost/georegistry02");
    use <collection_name>;
    db.<collection_name>.find();
    db.<collection_name>.find().forEach(printjson);

Create Indexes
::
    db.<collection_name>.ensureIndex( { 'geometry_centroid' : "2d" } )
    db.<collection_name>.ensureIndex( { 'country_code' : 1 } )
    db.<collection_name>.ensureIndex( { 'id' : 1 } )

Display everythin in the collection
::
    db.<collection_name>.find().forEach(printjson);


Setup georegistry:
===========
These instruction may need to be modified based on your flavor/version of Linux/Unix.

For example, you could install python-imaging with pip, by typing:
::
    sudo pip install PIL


Noy you need to install 

Setup on Ubuntu 10.10
::
    sudo apt-get install lib-geos-c1 python-imaging git-core mercurlial build-essental python2.6-dev python-setuptools libdecodeqr0 libdecodeqr-dev libqrencode3 libqrencode-dev
    sudo easy_install pip
    git clone git://github.com/mvpdev/georegistry.git
    cd georegistry
    sudo pip install -r requirements.txt
    python manage.py syncdb
    python managae.py runserver


Now that you have the server running, move on to the tutorial
