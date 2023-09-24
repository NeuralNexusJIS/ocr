import os 
import io
import json
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
import requests
from PIL import Image, ImageDraw, ImageFont
import time
credential = json.load(open('credential.json'))
API_KEY = credential['API_KEY']
ENDPOINT = credential['ENDPOINT']  

cv_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

image_url = 'image/A-sample-prescription-containing-handwritten-texts-over-the-printed-lines.png'
response = cv_client.read_in_stream(open(image_url,'rb'), language='en', raw=True)
operationLocation = response.headers["Operation-Location"]
operation_id= operationLocation.split("/")[-1]
time.sleep(1)
result = cv_client.get_read_result(operation_id)
print(result)
print(result.status)
print(result.analyze_result)

if result.status == OperationStatusCodes.succeeded:
    read_results = result.analyze_result.read_results
    for analyzed_result in read_results:
        for line in analyzed_result.lines:
            print(line.text)
            