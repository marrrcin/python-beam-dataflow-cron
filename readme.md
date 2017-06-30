# Google DataFlow python - App Engine deployment
Full description and implementation details are in my blogpost: 

http://zablo.net/blog/post/python-apache-beam-google-dataflow-cron

---
This repository contains basic project, which can be used as an example of how to deploy Google Dataflow (Apache Beam) pipeline to App Engine in order to run it as as CRON job.
*It only works on App Engine Flex Environment*, due to I/O used by Apache Beam (on App Engine Standard it throws an error about Read-only file system).
## Description
1. **setup.py** file is important - without it, Dataflow engine will be unable to distribute packages across dynamically spawned DF workers
1. **app.yaml** contains definition of App Engine app, which will spawn Dataflow pipeline
1. **cron.yaml** contains definition of App Engine CRON, which will ping one of the App endpoints (in order to spawn Dataflow pipeline)
1. **appengine_config.py** adds dependencies to locally installed packages (from **lib** folder)

## Instruction
1. Remember to put ```__init__.py``` files into all local packages
1. Install all required packages into local **lib** folder: ```pip install -r requirements.txt -t lib```
1. To deploy App Engine app, run: ```gcloud app deploy app.yaml```
1. To deploy App Engine CRON, run: ```gcloud app deploy cron.yaml```
