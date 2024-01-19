from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
import pandas as pd

import random


app = Flask(__name__)



@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    response = VoiceResponse()
    gather = Gather(input='dtmf speech', timeout=5, num_digits=1,action='/roll', method='POST')
    gather.say('Welcome to the MVSR Engineering College call center. For speech input say one. For DTMF input press two.')
    response.append(gather)
    return str(response) 
    # Process the user's choice
    
@app.route("/roll", methods=['POST'])
def answered():
    response = VoiceResponse()
    if 'Digits' in  request.form:
        # If the user chose DTMF input
        gather = Gather(input='dtmf', timeout=3, num_digits=12, action='/process_dtmf', method='POST')
        gather.say('Please enter your Roll number using the keypad.')
        response.append(gather)
    elif 'SpeechResult' in  request.form:
        # If the user chose speech input
        gather = Gather(input='speech', timeout=12, num_digits=12, action='/process_speech', method='POST')
        gather.say('Please say your Roll Number.')
        response.append(gather)
   
    else:
        # Invalid input
        response.say('Sorry, I did not understand your choice. Please try again.')
        response.redirect('/answer')

    return str(response)


@app.route('/process_speech', methods=['POST'])
def process_speech():
    roll_number = request.values.get('SpeechResult')

    # TODO: Add code to verify the roll number
    if (roll_number=='245119737040'):
        response = VoiceResponse()
        response.say("Roll number verified. Press 1 to know your academic details, Press 2 to order your certificates, Press 3 for any other queries")
        response.gather(num_digits=1, action='/menu', method='POST')
        return str(response)
    else:
        response = VoiceResponse()
        gather = Gather(input='speech', timeout=6, num_digits=12, action='/process_speech', method='POST')
        gather.say('Invalid roll number. Please say your roll number again.')
        response.append(gather)
        return str(response)

@app.route('/process_dtmf', methods=['POST'])
def process_dtmf():
    roll_number = request.values.get('Digits', None)
    
    if (roll_number=='245119737040'):
        response = VoiceResponse()
        response.say("Roll number verified. Press 1 to know your academic details, Press 2 to order your certificates, Press 3 for any other queries")
        response.gather(num_digits=1, action='/menu', method='POST')
        return str(response)
        
    else:
        response = VoiceResponse()
        response.say("Invalid roll number. Please try again.")
        response.gather(num_digits=12, action='/process_dtmf', method='POST')
        return str(response)
    
    
@app.route("/menu", methods=['GET', 'POST'])
def menu():
    digit_pressed = request.values.get('Digits', None)
    if digit_pressed == '1':
        response = VoiceResponse()
        gather = Gather(input='dtmf', timeout=5, num_digits=1,action='/academic_menu', method='POST')
        gather.say('To know your attendance percentage, Press 1. To know your exam results, Press 2. To know your timetable, Press 3. To know your fee details, Press 4.')
        response.append(gather)
        return str(response) 
        
    elif digit_pressed == '2':
        response = VoiceResponse()
        gather = Gather(input='dtmf', timeout=8,num_digits=1, action='/certificate_menu',method='POST')
        gather.say("To order a transcript, press 1. To order a degree certificate, press 2. To order a mark sheet, press 3.")
        response.append(gather)
        return str(response)
    elif digit_pressed == '3':
        response = VoiceResponse()
        gather = Gather(input='speech', timeout=3, action='/query-speech')
        gather.say('Please say your query.')
        response.append(gather)
        return str(response)
    else:
        response = VoiceResponse()
        response.say("Invalid selection. Please try again.")
        response.gather(num_digits=1, action='/menu', method='POST')
        return str(response)


@app.route("/academic_menu", methods=['GET', 'POST'])
def academic_menu():
    digit_pressed = request.values.get('Digits', None)
    if digit_pressed == '1':
        response = VoiceResponse()
        att = random.randint(50,85)
        response.say("Attendace Percentage is "+ str(att))
        return str(response)
    elif digit_pressed == '2':
        response = VoiceResponse()
        res = random.random() * 10
        response.say("GPA Percentage is "+ str(res))
        return str(response)
    elif digit_pressed == '3':
        response = VoiceResponse()
        response.say("Not Avialabel")
        return str(response)
    elif digit_pressed == '4':
        response = VoiceResponse()
        res = random.randint(50,85) *1000
        response.say("Remaing Due is "+ str(res))
    else:
        response = VoiceResponse()
        response.say("Invalid selection. Please try again.")
        response.gather(num_digits=1, action='/academic_menu', method='POST')
        return str(response)
    

        
# @app.route('/query-speech', methods=['POST'])
# def query():
#     # Get the speech input from the request parameters
#     speech_result = request.form['SpeechResult']

#     # Process the speech input as per your requirements

#     return 'Speech input processed: ' + speech_result

# @app.route('/address-speech', methods=['POST'])
# def address():
#     # Get the speech input from the request parameters
#     speech_result = request.form['SpeechResult']
#     response = VoiceResponse()
#     gather = Gather(num_digits=1, timeout=7, action='/order_certificate', method='POST')
#     gather.say('Speech input processed: ' + speech_result + 'is confirmed.')
#     response.append(gather)
#     return str(response)


@app.route("/order_certificate", methods=['GET', 'POST'])
def order_certificate():
    student_id = request.values.get('Digits', None)
    # TODO: Add code to retrieve student's information and process the certificate order
    response = VoiceResponse()
    response.say("Thank you for your order. Your certificate will be delivered to your registered address within 7-10 business days.")
    response.hangup()
    return str(response)

def make_payment():
    credit_card_number = request.values.get('Digits', None)
    # TODO: Add code to process the payment
    response = VoiceResponse()
    response.say("Thank you for your payment. Your certificate will be delivered to your registered address within 7-10 business days.")
    response.hangup()
    return str(response)


if __name__ == "__main__":
    app.run(debug=True)
