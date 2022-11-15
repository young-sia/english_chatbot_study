from flask import Flask, request, jsonify, render_template, abort
import os
import requests
import json
import pusher
import google.cloud.dialogflow as dialogflow

app = Flask(__name__)


@app.route('/')
def index():
    app.logger.info('start the page')
    return render_template('chatbot_page.html')


@app.route('/pick_one')
def pick_page():
    return render_template('pick_one_subject.html')


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    if data['queryResult']['queryText'] == 'yes':
        reply = {
            "fulfillmentText": "Ok. Great",
        }
        return jsonify(reply)

    elif data['queryResult']['queryText'] == 'no':
        reply = {
            "fulfillmentText": "Ok. Booking cancelled.",
        }
        return jsonify(reply)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response.query_result.fulfillment_text


@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = {"message": fulfillment_text}
    return jsonify(response_text)


@app.route('/project/<project_name>/send_message', methods=['POST'])
def project_message(project_name):
    message = request.form['message']
    try:
        project_id = project_name_id[project_name]
    except KeyError:
        abort(404)
        return
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = {"message": fulfillment_text}
    return jsonify(response_text)


project_name_id = {
    'example_project': 'newagent-xmaw'
}

# run Flask app
if __name__ == "__main__":
    app.run()
