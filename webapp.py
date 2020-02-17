from flask import Flask
from flask import request
from TextScore import text_score
app = Flask(__name__)


@app.route('/', methods=['POST'])
def hello():
    document_a = request.json['document_a']
    document_b = request.json['document_b']
    distance_score = text_score(document_a, document_b)
    return {
        "distance_score": {
            "edit_distance": f"{distance_score.edit_distance}",
            "max_distance": f"{distance_score.max_score}",
            "score": f"{distance_score.percentage_score()}"
        }
    }
if __name__ == '__main__':
    app.run()