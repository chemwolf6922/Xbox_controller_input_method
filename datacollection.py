import joystickInput
import threading
import time
import string
import random

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

class log_thread(threading.Thread):
    def __init__(self,log_file_name,controller):
        threading.Thread.__init__(self)
        self.new_charactor = None

        self.input_detected = False
        self.record_counter = 0
        self.record_finished = True
        self.new_charactor_in = False

        self.log_file = open(log_file_name,'a')
        self.controller = controller
        self.running = False
    
    def log_info(self):
        if not self.new_charactor is None:
            self.log_file.write(self.new_charactor+'\n')
            self.log_file.flush()
            self.new_charactor = None

        LSX = self.controller.states['LSX']
        LSY = self.controller.states['LSY']
        RSX = self.controller.states['RSX']
        RSY = self.controller.states['RSY']
        self.input_detected = ((LSX**2+LSY**2)**0.5 >= 32767) or ((RSX**2+RSY**2)**0.5 >= 32767)
        
        
        if self.input_detected and self.new_charactor_in and self.record_finished:
            self.record_finished = False
            self.record_counter = 20

        if self.record_counter > 0:
            self.record_counter -= 1
            log_str = ','.join([str(i) for i in [LSX,LSY,RSX,RSY]])+'\n'
            self.log_file.write(log_str)
            self.log_file.flush()
            if self.record_counter == 0:
                self.record_finished = True
                self.new_charactor_in = False
            

    def set_new_charactor(self,charactor):
        self.new_charactor_in = True
        self.new_charactor = charactor

    def stop(self):
        self.running = False
        self.log_file.close()

    def run(self):
        self.running = True
        while self.running:
            time.sleep(0.01)
            self.log_info()



if __name__ == '__main__':
    controller = joystickInput.XBoxController()
    c_thread = controller_thread(controller)
    c_thread.start()
    l_thread = log_thread('log/data',controller)
    l_thread.start()
    alphabet = list(string.ascii_uppercase)
    testset = alphabet*20
    random.seed(time.time)
    for i in range(10):
        random.shuffle(testset)
    for c in testset:
        print(c)
        l_thread.set_new_charactor(c)
        while l_thread.new_charactor_in:
            time.sleep(0.01)
    l_thread.stop()
    c_thread.stop()