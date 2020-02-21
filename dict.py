import numpy as np
import string
import time

class word_node():
    def __init__(self,w,f,is_word):
        self.w = w
        self.f = f
        self.total_f = self.f
        self.is_word = is_word
        self.nexts = [None] * 26
        
    def add_next(self,node,c):
        self.nexts[ord(c)-ord('a')] = node

    def add_f(self,f):
        self.total_f += f

    def next(self,c):
        return self.nexts[ord(c)-ord('a')]

class word_dict():
    def __init__(self):
        self.root = word_node('',0,False)

    def add(self,w,f):
        c_node = self.root
        for i in range(len(w)-1):
            c_node.add_f(f)
            if c_node.next(w[i]) is None:
                new_node = word_node(w[:i+1],0,False)
                c_node.add_next(new_node,w[i])
            c_node = c_node.next(w[i])
        c_node.add_f(f)
        if c_node.next(w[-1]) is None:
            new_node = word_node(w,f,True)
            c_node.add_next(new_node,w[-1])
        else:
            c_node = c_node.next(w[-1])
            c_node.f = f
            c_node.is_word = True

    def search(self,w):
        c_node = self.root
        for c in w:
            c_node = c_node.next(c)
            if c_node is None:
                return None
        return c_node

    def predict(self,css,pss):
        wps = self.get_initial_wps()
        for i in range(len(css)):
            cs = css[i]
            ps = pss[i]
            wps = self.predict_next(wps,cs,ps)
        return wps

    def get_initial_wps(self):
        return [[self.root,1]]
    
    def predict_next(self,old_wps,cs,ps):
        wps = []
        for wp in old_wps:
            c_node = wp[0]
            c_p = wp[1]
            for j in range(len(cs)):
                c = cs[j].lower()
                p = ps[j]
                if not c_node.next(c) is None:
                    p = c_p * p * c_node.next(c).total_f/c_node.total_f
                    wps.append([c_node.next(c),p])
        return wps

    def get_words(self,wps):
        words = []
        total_p = 0
        for wp in wps:
            c_node = wp[0]
            c_p = wp[1]
            if c_node.is_word:
                w = c_node.w
                p = c_p/c_node.total_f*c_node.f
                total_p += p
                words.append([w,p])
        for wp in words:
            wp[1] /= total_p
        return words


raw_dict_pair = []
dict_len = 10000

with open('dict','r') as f:
    for i in range(dict_len):
        strs = f.readline().strip('\n').split(' ')
        raw_dict_pair.append([strs[0],int(strs[1])])

w_dict = word_dict()

for p in raw_dict_pair:
    w = p[0]
    f = p[1]
    w_dict.add(w,f)

wps = w_dict.predict([['a','b','c'],['s','b','c'],['s','b','c']],[[0.3,0.3,0.4],[0.3,0.3,0.4],[0.3,0.3,0.4]])
words = w_dict.get_words(wps)
print(words)