from flask import Flask, render_template, request, jsonify
import joystickInput
import threading
import inference
import string
import random
import time
import logging
import tensorflow as tf
from tensorflow import keras
import input_method

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

class app_thread(threading.Thread):
    def __init__(self,c_thread,p_thread):
        threading.Thread.__init__(self)
        self.c_thread = c_thread
        self.p_thread = p_thread
        self.running = False
        self.target_key = ""
        self.input_text = "inference"
        self.candidates = ""
        self.selected_candidate = 0

    def stop(self):
        self.running = False

    def run(self):
        self.c_thread.start()
        self.p_thread.start()

raw_dict_pair = []
dict_len = 10000
with open('dict','r') as f:
    for i in range(dict_len):
        strs = f.readline().strip('\n').split(' ')
        raw_dict_pair.append([strs[0],int(strs[1])])
w_dict = input_method.word_dict()
for p in raw_dict_pair:
    w = p[0]
    f = p[1]
    w_dict.add(w,f)
classifier = keras.models.load_model('classifier.h5')
controller = joystickInput.XBoxController()
input_history = inference.input_data(w_dict)
c_thread = controller_thread(controller)
p_thread = inference.process_thread(classifier,controller,input_history)
a_thread = app_thread(c_thread,p_thread)

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/getInfo',methods=['GET'])
def getInfo():
    ws = input_history.get_words()
    wstr = ""
    for wp in ws:
        wstr += wp[0]
        wstr += " "
    return jsonify(
        LSX = controller.states['LSX'],
        LSY = controller.states['LSY'],
        RSX = controller.states['RSX'],
        RSY = controller.states['RSY'],
        targetKey = a_thread.target_key,
        inputText = input_history.input_text,
        candidates = wstr,
        selectedCandidate = input_history.c_index
    )

if __name__ == '__main__':
    a_thread.start()
    app.run()