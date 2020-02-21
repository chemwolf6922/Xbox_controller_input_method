from flask import Flask, render_template, request, jsonify
import joystickInput
import threading
import datacollection
import string
import random
import time
import logging

class controller_thread(threading.Thread):
    def __init__(self,controller):
        threading.Thread.__init__(self)
        self.controller = controller
        self.running = False

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.controller.process_events()

class data_collection_thread(threading.Thread):
    def __init__(self,c_thread,l_thread):
        threading.Thread.__init__(self)
        self.c_thread = c_thread
        self.l_thread = l_thread
        self.running = False
        self.target_key = ""
        self.input_text = "data collection"
        self.candidates = ""
        self.selected_candidate = 0

    def stop(self):
        self.running = False

    def run(self):
        self.c_thread.start()
        self.l_thread.start()
        alphabet = list(string.ascii_uppercase)
        testset = alphabet * 20
        random.seed(time.time)
        for i in range(10):
            random.shuffle(testset)
        for c in testset:
            self.target_key = str(c)
            self.l_thread.set_new_charactor(c)
            while self.l_thread.new_charactor_in:
                time.sleep(0.01)
        self.l_thread.stop()
        self.c_thread.stop()
        self.target_key = ""

controller = joystickInput.XBoxController()
c_thread = controller_thread(controller)
l_thread = l_thread = datacollection.log_thread('log/data_gui',controller)
d_thread = data_collection_thread(c_thread,l_thread)

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

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
        targetKey = d_thread.target_key,
        inputText = d_thread.target_key,
        candidates = d_thread.candidates,
        selectedCandidate = d_thread.selected_candidate
    )

if __name__ == '__main__':
    d_thread.start()
    app.run()