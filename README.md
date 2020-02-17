# How To Run
## Docker compose
> docker-compose up
## Docker run
> docker run -e FLASK_APP=webapp.py -p 5000:5000 jsicotte/programming-challenge:latest flask run -h 0.0.0.0
## CLI

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=webapp.py
flask run 
```
# REST API
To compare two text elements:
## Request
```baash
curl -H "Content-Type: application/json" -d '{"document_a":"value1","document_b":"value2"}' -X POST  http://localhost:5000/
```
## Response
```javascript
{
  "distance_score": {
    "edit_distance": "1",
    "max_distance": "8",
    "score": "0.875"
  }
}
```
