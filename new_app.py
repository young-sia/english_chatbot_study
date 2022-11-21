from flask import Flask, request, jsonify, render_template, abort
import os
import requests
import json
import pusher
import google.cloud.dialogflow as dialogflow
import speech_recognition as sr


app = Flask(__name__)
project_name_id = {
    'example_project': 'newagent-xmaw'
}


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


def detect_intent_audio(project_name):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        message = r.recognize_google(audio)
        return message


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
        return None
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = {"message": fulfillment_text}
    return jsonify(response_text)
