from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime



app = Flask(__name__)
app.secret_key = 'mysecretkey'

users = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('chat'))
        else:
            return render_template('index.html', error='Invalid username or password')
    else:
        return render_template('index.html', error=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users:
            return render_template('register.html', error='Username already taken')
        else:
            users[username] = password
            session['username'] = username
            return redirect(url_for('chat'))
    else:
        return render_template('register.html', error=None)

class ChatBot:
    def __init__(self):
        self.messages = []

    def send_message(self, message):
        self.messages.append(('user', message))
        response = self.get_response(message)
        self.messages.append(('bot', response))
        return response

    def get_response(self, message):
        # replace this with your own chatbot logic
        return f"Sorry, I don't understand '{message}'."

    def get_messages(self):
        return self.messages


bot = ChatBot()

@app.route('/chat')
def chat():
    if 'username' in session:
        username = session['username']
        messages = bot.get_messages()
        if len(messages) == 0:
            bot.send_message(f"Hello, {username}! How can I help you today?")
        return render_template('chat.html', username=username, messages=messages)
    else:
        return redirect(url_for('index'))

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    bot.send_message(message)
    return redirect(url_for('chat'))

if __name__ == '__main__':
    app.run()
