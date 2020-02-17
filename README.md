# How To Run
## Docker compose
> docker-compose up
## Docker run
> docker run -e FLASK_APP=webapp.py -p 5000:5000 jsicotte/programming-challenge:latest flask run -h 0.0.0.0
## Command Line
> python3 -m venv venv
> source venv/bin/activate
> pip install -r requirements.txt
> export FLASK_APP=webapp.py
> flask run 
