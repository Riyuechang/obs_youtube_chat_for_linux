from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

#獲得顯示用網頁
@app.route("/index")
def index():
    return render_template('index.html')

#傳送聊天室訊息到網頁
@app.route("/send_message", methods=['GET'])
def send_message():
    author_name = request.args.get('author_name')
    message = request.args.get('message')
    data = {"author_name" : author_name, "message" : message}
    socketio.emit('send_message', data)
    return "Transmission completed"

#清空聊天室
@app.route("/clear")
def clear():
    socketio.emit('clear')
    return "clear"


if __name__ == '__main__':
    socketio.run(app, debug=True, host='127.0.0.1', port=3200)