#from django.test import TestCase
from face_detection import face_detection
import os
# Create your tests here.

current_path = os.getcwd()
print(current_path)
output = face_detection(current_path+"/test.mp4")
print(output)
