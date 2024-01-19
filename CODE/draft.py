from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from pymongo import MongoClient
client = MongoClient("mongodb+srv://admin-hrutu:Fire%401234@cluster0.vwlmw.mongodb.net")
db = client["mvsr"]
data = db['data']
tt = db['s']
tts = tt.find_one({'day': 'Monday'})


for i in tts['timetable']:
    print(i['time'] + " " + i['subject'])