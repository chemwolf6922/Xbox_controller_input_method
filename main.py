from flask import Flask, render_template, request, jsonify
import joystickInput
import threading


controller = joystickInput.XBoxController()

class controllerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        global controller
        while True:
            controller.process_events()

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/getInfo',methods=['GET'])
def getInfo():
    return jsonify(
        LSX = controller.states['LSX'],
        LSY = controller.states['LSY'],
        RSX = controller.states['RSX'],
        RSY = controller.states['RSY'],
        targetKey = "X",
        inputText = "hahaha",
        candidates = "this is test",
        selectedCandidate = 1
    )

if __name__ == '__main__':
    cThread = controllerThread()
    cThread.start()
    app.run()