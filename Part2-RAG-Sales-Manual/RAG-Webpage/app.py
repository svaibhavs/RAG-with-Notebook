## Assisted by WCA@IBM
## Latest GenAI contribution: ibm/granite-20b-code-instruct-v2from flask import Flask, render_template
from flask import Flask, render_template, request, jsonify, make_response

app = Flask(__name__)

@app.route("/", methods=["GET", "OPTIONS"])
def index():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "GET":
        return _corsify_actual_response(render_template('index.html'))
    else:
        raise RuntimeError("Weird - don't know how to handle method {}".format(request.method))

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
  
@app.route('/healthz')
# Added healthcheck endpoint
def healthz():
    return "ok"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
