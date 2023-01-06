import os
import re
import openai
import reader
import pyaudio
import pydub
import pocketsphinx
from flask import Flask, redirect, render_template, request, url_for
import speech_recognition as sr

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
language = 'en'

@app.route("/", methods=("GET", "POST"))
def index():
    
    if (request.args.get('command')):
        reader.text_to_speech(request.args.get('command'), request.args.get('gender')) 
        response="Speaking..."
        return response, 200, {'Content-Type': 'text/plain'}

    elif request.method == 'POST' and ('record' in request.form):
        init_rec = sr.Recognizer()
        with sr.Microphone() as source:
            audio_data = init_rec.record(source, duration=15)
            text = init_rec.recognize_sphinx(audio_data)
            return render_template("index.html", transcript=text, imgList={}, gender=request.form['submitGender'])
    elif request.method == "POST" and ('transcript' in request.form):
            
            if (request.form['submitMaxButtons'] == ''):
                maxButtons = 18; 
            else: 
                maxButtons = int(request.form['submitMaxButtons'])

            if (request.form['submitExtractionType']=="keywords"):
                if (int(request.form['submitGradeLevel']) > 0): 
                    gradedText = openai.Completion.create(
                        model="text-davinci-003",
                        prompt="Summarize this for a grade " + request.form['submitGradeLevel'] + " student: " + request.form['transcript'], 
                        temperature=0,
                        max_tokens=64,
                        top_p=1.0,
                        frequency_penalty=0.0,
                        presence_penalty=0.0, 
                    )
                    prompt = "Extract keywords from this text: " + gradedText 
                else:
                    prompt = "Extract keywords from this text: " + request.form['transcript']
                
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt, 
                    temperature=0,
                    max_tokens=maxButtons,
                    top_p=1.0,
                    frequency_penalty=0.8,
                    presence_penalty=0.0, 
                )
                resultString = response.choices[0].text.strip()
            elif (request.form['submitExtractionType']=="verbatim"):
                resultString = request.form['transcript'].strip()
            
            resultList = re.split(r"Keywords: |[\b\W\b]+", resultString)
            imgList = {}
            for result in resultList:
                if result != '': 
                    imgResponse = openai.Image.create(
                        prompt=result,
                        n=1,
                        size="256x256"
                    )
                    imageUrl = imgResponse['data'][0]['url']
                    imgList[result]=imageUrl
            return render_template("index.html", imgList=imgList, gender=request.form['submitGender'])
    else:
        result = request.args.get("result")
        return render_template("index.html", result=result, imgList={}, gender='female')