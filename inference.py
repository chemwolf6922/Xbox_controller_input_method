import joystickInput
import threading
import time
import string
import numpy as np
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

class input_data():
    def __init__(self,w_dict):
        self.css = []
        self.pss = []
        self.input_text = ""
        self.words = []
        self.w_dict = w_dict
        self.wps = self.w_dict.get_initial_wps()
        self.c_index = 0

    def add(self,cs,ps):
        self.css.append(cs)
        self.pss.append(ps)
        self.wps = self.w_dict.predict_next(self.wps,cs,ps)
        self.words = self.w_dict.get_words(self.wps)
        
    def get_words(self):
        return self.words

    def confirm_input(self):
        if len(self.words) > 0:
            if c_index >= len(self.words):
                c_index = len(self.words) - 1
            self.input_text += self.words[self.c_index]
            self.input_text += " "
        self.css = []
        self.pss = []
        self.wps = self.w_dict.get_initial_wps()
        self.words = []
        self.c_index = 0

    

class process_thread(threading.Thread):
    def __init__(self,model,controller,i_data):
        threading.Thread.__init__(self)

        self.time_out_counter = 0
        self.time_out = 20

        self.model = model
        self.controller = controller
        self.running = False

        self.i_data = i_data
    
    def process(self):
        if self.time_out_counter > 0:
            self.time_out_counter -= 1
            return

        LSX = self.controller.states['LSX']
        LSY = self.controller.states['LSY']
        RSX = self.controller.states['RSX']
        RSY = self.controller.states['RSY']

        input_detected = ((LSX**2+LSY**2)**0.5 >= 32767) or ((RSX**2+RSY**2)**0.5 >= 32767)
        if input_detected:
            d = np.asarray([LSX,LSY,RSX,RSY],dtype = np.float32)
            if d[0]**2+d[1]**2 < d[2]**2+d[3]**2:
                d[0] = 0
                d[1] = 0
            else:
                d[2] = 0
                d[3] = 0
            i_thread = inference_thread(self.model,d,self.i_data)
            i_thread.start()
            self.time_out_counter = self.time_out


    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            time.sleep(0.01)
            self.process()


class inference_thread(threading.Thread):
    def __init__(self,model,data,i_data):
        threading.Thread.__init__(self)
        self.model = model
        self.data = data
        self.i_data = i_data

    def run(self):
        result = self.model.predict_on_batch(self.data.reshape((1,4)))[0]
        pos = np.array(result)
        pos = np.argsort(pos)[::-1]
        ratio = np.array(result)
        ratio = np.sort(ratio)[::-1]
        s = 0
        i = 0
        for r in ratio:
            s += r
            i += 1
            if s > 0.99:
                break
        ps = ratio[:i]
        cs = [string.ascii_uppercase[p] for p in pos[:i]]
        self.i_data.add(cs,ps)
        # print(ratio[:i])
        # print([string.ascii_uppercase[p] for p in pos[:i]])

if __name__ == '__main__':
    classifier = keras.models.load_model('classifier.h5')
    controller = joystickInput.XBoxController()
    i_data = input_data()
    c_thread = controller_thread(controller)
    c_thread.start()
    p_thread = process_thread(classifier,controller,i_data)
    p_thread.start()
    print('System on')
    # time.sleep(20)
    # p_thread.stop()
    # c_thread.stop()
    # print('System off')

    