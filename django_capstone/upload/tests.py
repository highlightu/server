#from django.test import TestCase
from face_detection import face_detection
import os
# Create your tests here.

original_candidate = {'00:01:15':0.5, '00:01:16':1, '00:01:17':0.7, '00:01:18':0.8,'00:01:19':0.9}

x = 0
y = 0
w = 500
h = 500

current_path = os.getcwd()
print(current_path)
output = face_detection(current_path+"/test.mp4", original_candidate, x, y, w, h)
print(output)
