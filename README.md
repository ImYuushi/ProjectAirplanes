# Project Airplanes

This is a framework I did in my spare time for doing Object Detection in satelite images provided by NASA, trying to automate what the Project Sungrazer is doing manually.

## Project Sungrazer

This is a community-based project run by NASA/US Naval Labratory. People look through satelite images looking for comments and submit their findings.

## How this code works

There are three different major steps: datacollection, dataprocessing and the actual training. Datacollection is responsible for dowloading and saving the various data (Images and the files containing the data used for labeling, i. e. previous confirmations of comets).

Dataprocessing processes this data and converts it into a form usable by training.

Training does... well... training (and saving the models)

## How to run this code

In the Code library there is a Config file, where various options can be selected, mainly parameters for training and which steps to run within datacollection and processing (this is done because for example maybe we dont want to spend 35 hours downloading the images every time we run the code D:)

After this is done, just run the 3 files one by one. This only needs to be done once to set up (and everytime we want to add data from more years (don't add 2021 for training, the labeling is up to date as for writing of this README, you will just waste 30 hrs... like me...))

Same needs to be repeated for datapreprocessing and training.

