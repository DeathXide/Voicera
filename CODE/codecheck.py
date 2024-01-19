from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin-hrutu:Fire%401234@cluster0.vwlmw.mongodb.net")
db = client["mvsr"]
data = db['data']
tt = db['s']
student = data.find_one({'roll': '245119737040'})
global stu
stu = (student)

app = Flask(__name__)


@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    response = VoiceResponse()
    gather = Gather(input='dtmf speech', timeout=5, num_digits=1,action='/inputType', method='POST')
    gather.say('Welcome to the MVSR Engineering College call center. For speech input say one. For DTMF input press two.')
    response.append(gather)
    return str(response) 

@app.route("/inputType", methods=['POST'])
def inputs():
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
    student = data.find_one({'roll': roll_number}) 
    global stu 
    stu = student if student else False   
    if (stu):
        response = VoiceResponse()
        response.say("Verify the Roll Number using the 4 Digit Code")
        response.gather(num_digits=4, timeout=12, action='/auth', method='POST')
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
    student = data.find_one({'roll': roll_number}) 
    global stu 
    stu = student if student else False   
    if (stu):
        response = VoiceResponse()
        response.say("Verify the Roll Number using the 4 Digit Code")
        response.gather(num_digits=4,timeout=12, action='/auth', method='POST')
        return str(response)
        
    else:
        response = VoiceResponse()
        response.say("Invalid roll number. Please try again.")
        response.gather(num_digits=12,timeout=12, action='/process_dtmf', method='POST')
        return str(response)
    
@app.route('/auth', methods=['POST'])
def auth():
    global stu
    code = request.values.get('Digits', None)
    ogcode = stu['phone'][-4:] 
    if (code == ogcode):
        response = VoiceResponse()
        response.say("Roll number verified. Welcome "+ stu['name'] +" Press 1 to know your academic details, Press 2 to order your certificates, Press 3 for any other queries")
        response.gather(num_digits=1,timeout=12, action='/menu', method='POST')
        return str(response)        
    else:
        response = VoiceResponse()
        response.say("Invalid Code. Please try again. Verify the Roll Number using the 4 Digit Code")
        response.gather(num_digits=4,timeout=12, action='/auth', method='POST')
        return str(response)



    
@app.route("/menu", methods=['POST'])
def menu():
    digit_pressed = request.values.get('Digits', None)
    if digit_pressed == '1':
        response = VoiceResponse()
        gather = Gather(input='dtmf', timeout=5, num_digits=1,action='/academic_menu', method='POST')
        gather.say('To know your attendance percentage, Press 1. To know your exam results, Press 2. To know your timetable, Press 3. To know your fee details, Press 4. To Exit call Press 5')
        response.append(gather)
        return str(response) 
        
    elif digit_pressed == '2':
        response = VoiceResponse()
        gather = Gather(input='dtmf', timeout=8,num_digits=1, action='/certificate_menu',method='POST')
        gather.say("To order a memos, press 1. To order a degree certificate, press 2. To order a mark sheet, press 3.")
        response.append(gather)
        return str(response)
    elif digit_pressed == '3':
        response = VoiceResponse()
        gather = Gather(input='speech', timeout=5, action='/query-speech')
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
        att = stu['attendance']
        response.say("Attendace Percentage is "+ str(att))
        response.redirect('/menu?Digits=1',method='POST')
        return str(response)
    elif digit_pressed == '2':
        response = VoiceResponse()
        gpa = stu['gpa']
        response.say("GPA Percentage is "+ str(gpa))
        response.redirect('/menu?Digits=1',method='POST')
        return str(response)
    elif digit_pressed == '3':
        response = VoiceResponse()
        gather = Gather(input='dtmf', timeout=8,num_digits=1, action='/timetable',method='POST')
        gather.say("For Monday, press 1. For Tuesday, press 2. For Wednesday, press 3. For Thursday, press 4. For Friday, press 5.")
        response.append(gather)
        response.redirect('/menu?Digits=1',method='POST')
        return str(response)
    elif digit_pressed == '4':
        response = VoiceResponse()
        fee = stu['fee']
        response.say("Remaing Due is "+ str(fee))
        response.redirect('/menu?Digits=1',method='POST')
        return str(response)
    elif digit_pressed == '5':
        response = VoiceResponse()
        response.say("Thank you for Calling M V S R Call Center")
        response.hangup()
        return str(response)
    else:
        response = VoiceResponse()
        response.say("Invalid selection. Please try again.")
        response.gather(num_digits=1, timeout=12 , action='/academic_menu', method='POST')
        return str(response)
    
@app.route("/timetable", methods=['POST'])
def timetable():
    digit_pressed = request.values.get('Digits', None)
    if digit_pressed == '1':
        response = VoiceResponse()
        tts = tt.find_one({'day': 'Monday'})
        for i in tts['timetable']:
            response.say(i['time'] + " " + i['subject'])
        return str(response) 
        
    elif digit_pressed == '2':
        response = VoiceResponse()
        tts = tt.find_one({'day': 'Monday'})
        for i in tts['timetable']:
            response.say(i['time'] + " " + i['subject'])
        return str(response)
    elif digit_pressed == '3':
        response = VoiceResponse()
        tts = tt.find_one({'day': 'Tuesday'})
        for i in tts['timetable']:
            response.say(i['time'] + " " + i['subject'])
        return str(response)
    elif digit_pressed == '4':
        response = VoiceResponse()
        tts = tt.find_one({'day': 'Thursday'})
        for i in tts['timetable']:
            response.say(i['time'] + " " + i['subject'])
        return str(response)
    elif digit_pressed == '5':
        response = VoiceResponse()
        tts = tt.find_one({'day': 'Friday'})
        for i in tts['timetable']:
            response.say(i['time'] + " " + i['subject'])
        return str(response)
    else:
        response = VoiceResponse()
        response.say("Invalid Day. Please try again.")
        response.gather(num_digits=1,timeout=12, action='/timetable', method='POST')
        return str(response)
    
@app.route("/certificate_menu", methods=['GET', 'POST'])
def certificate_menu():
    digit_pressed = request.values.get('Digits', None)
    if digit_pressed == '1':
        response = VoiceResponse()
        order = stu['transcript']
        if(order):
            response.say("Order has Already Been Placed.Thank you for calling")
            response.hangup()
            return str(response)
        else:
            data.update_one({'_id' : stu['_id']},{'$set': {'transcript': 1}})
            response.say("Thank you for your order. Make the payment at your doorstep. Your Memo certificate will be delivered to your registered address within 7-10 business days.")
            response.hangup()
            return str(response)
    elif digit_pressed == '2':
        response = VoiceResponse()
        order = stu['degree']
        if(order):
            response.say("Order has Already Been Placed.Thank you for calling")
            response.hangup()
            return str(response)
        else:
            data.update_one({'_id' : stu['_id']},{'$set': {'degree': 1}})
            response.say("Thank you for your order. Make the payment at your doorstep. Your degree certificate will be delivered to your registered address within 7-10 business days.")
            response.hangup()
            return str(response)
    elif digit_pressed == '3':
        response = VoiceResponse()
        order = stu['marksheet']
        if(order):
            response.say("Order has Already Been Placed.Thank you for calling")
            response.hangup()
            return str(response)
        else:
            data.update_one({'_id' : stu['_id']},{'$set': {'marksheet': 1}})
            response.say("Thank you for your order. Make the payment at your doorstep. Your marksheet certificate will be delivered to your registered address within 7-10 business days.")
            response.hangup()
            return str(response)
    else:
        response = VoiceResponse()
        response.say("Invalid selection. Please try again.")
        response.gather(num_digits=1,timeout=12, action='/certificate_menu', method='POST')
        return str(response)
    
    

@app.route('/query-speech', methods=['POST'])
def query():
    # Get the speech input from the request parameters
    speech_result = request.values.get('SpeechResult', None)
    response = VoiceResponse()
    response.say("Let me repeat your query. " + speech_result)    
    response.say("Your query is registered.")
    return str(response)


if __name__ == "__main__":
    app.run(debug=True)
