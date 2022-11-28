from flask import Flask, render_template

app = Flask(__name__)
project_name_id = {
    'example_project': 'newagent-xmaw'
}


@app.route('/')
def index():
    app.logger.info('start the page')
    return render_template('index.html')


# @app.route('/manual')
# def pick_page():
#     return render_template('first_chatbot_pick_chatbot.html')


@app.route('/chatbot1')
def chatbot_page1():
    return render_template('first_chatbot_bot1.html')


@app.route('/chatbot2')
def chatbot_page2():
    return render_template('first_chatbot_bot2.html')


@app.route('/chatbot3')
def chatbot_page3():
    return render_template('first_chatbot_bot3.html')


# run Flask app
if __name__ == "__main__":
    app.run()
