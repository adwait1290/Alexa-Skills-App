import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
app = Flask(__name__)
ask = Ask(app,"/news_reader")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

def get_headlines():
	user_pass_dict = {'user':'Adwait_TV',
			'passwd':'1234wasdf',
			'api_type':'json'}
	sess = requests.Session()
	sess.headers.update({'User-Agent':'I am testing Alexa: Adwait'})
	time.sleep(1)
	sess.post('https://www.reddit.com/api/login',data = user_pass_dict)
	url = 'https://www.reddit.com/r/worldnews/.json?limit=10'
	html = sess.get(url)
	data = json.loads(html.content.decode('utf-8'))
	titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
	titles = '...'.join([i for i in titles])
	a = titles.split('...')
	return a
	#return (a[0:z])

def get_local_headlines():
        user_pass_dict = {'user':'Adwait_TV',
                        'passwd':'1234wasdf',
                        'api_type':'json'}
        sess = requests.Session()
        sess.headers.update({'User-Agent':'I am testing Alexa: Adwait'})
        time.sleep(1)
        sess.post('https://www.reddit.com/api/login',data = user_pass_dict)
        url = 'https://www.reddit.com/r/USnews/.json?limit=10'
        html = sess.get(url)
        data = json.loads(html.content.decode('utf-8'))
        titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
        titles = '...'.join([i for i in titles])
        a = titles.split('...')
        return a
def get_tech_headlines():
        user_pass_dict = {'user':'Adwait_TV',
                        'passwd':'1234wasdf',
                        'api_type':'json'}
        sess = requests.Session()
        sess.headers.update({'User-Agent':'I am testing Alexa: Adwait'})
        time.sleep(1)
        sess.post('https://www.reddit.com/api/login',data = user_pass_dict)
        url = 'https://www.reddit.com/r/technology/.json?limit=10'
        html = sess.get(url)
        data = json.loads(html.content.decode('utf-8'))
        titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
        titles = '...'.join([i for i in titles])
        a = titles.split('...')
        return a

app.route('/news_reader')
@ask.launch
def start_skill():
	welcome_msg = "Hello HUMAN! What type of news would you like to hear? Technological Global or Local? Also How many headlines would you like to hear for this category?"
	return question(welcome_msg)
	
@ask.intent("YesIntent")
def how_many_headlines():
	msg = "How many of the top headlines would you like to hear?"
	return question(msg)
@ask.intent("NumIntent")
def share_headlines(number):
	print(number)
	print (100 * "**********************")
	y = get_headlines()
	num = int(number)
	headlines = y[0:num] 
	headline_msg = "The top {} news headline is {}".format(number,headlines)
	return statement(headline_msg)
@ask.intent("NoIntent")
def no_intent():
	bye_msg = "I'm not sure why you asked me to run. But. . . Okay. . Bye Felicia"
	return statement(bye_msg)
@ask.intent("GlobalIntent")
def share_headlines(number):
	y = get_headlines()
	num = int(number)
	if num == 1:
		headlines = y[0]
		headline_msg = "The top global news headline is {}".format(headlines)
		return statement(headline_msg)
	else:
		headlines = y[0:num]
		headline_msg = "The top {} global news headlines are {}".format(number,headlines)
		return statement(headline_msg)
@ask.intent("LocalIntent")
def share_headlines(number):
	y = get_local_headlines()
	num = int(number)
	if num == 1:
		headlines = y[0]
		y = get_local_headlines()
		headline_msg = "The top local news headline is {}".format(headlines)
		return statement(headline_msg)
	else:
		headlines = y[0:num]
		headline_msg = "The top {} local news headlines are {}".format(number,headlines)
		return statement(headline_msg)
@ask.intent("TechIntent")
def share_headlines(number):
        y = get_tech_headlines()
        num = int(number)
        if num == 1:
                headlines = y[0]
                y = get_local_headlines()
                headline_msg = "The top tech news headline is {}".format(headlines)
                return statement(headline_msg)
        else:
                headlines = y[0:num]
                headline_msg = "The top {} tech news headlines are {}".format(number,headlines)
                return statement(headline_msg)

app.run(debug=True)
	
