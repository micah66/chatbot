"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import random
import requests

animation_dict = {
    'afraid': {
        'word': ['scared', 'afraid', 'scary', 'monster', 'frightened', 'fright', 'worry', 'worried', 'nervous'],
        'response': ['That does sound very scary.', 'I\'m sorry you were frightened.']
    },
    'bored': {
        'word': ['bored', 'sleepy', 'sleep', 'boring'],
        'response': ['You are boring me too.']
    },
    'crying': {
        'word': ['sad', 'sadness', 'upset', 'cry', 'cried'],
        'response': ['Awwww, that is very sad!']
    },
    'dancing': {
        'word': ['dance', 'dancing', 'moves', 'party', 'music'],
        'response': ['I love to dance!', 'Look at me sick moves', 'Watch me do the robot']
    },
    'dog': {
        'word': ['dog', 'dogs', 'animal', 'animals', 'pet', 'pets', 'cat', 'cats'],
        'response': ['I love dogs', 'Dogs are my favorite pet', 'I love dogs, but I don\'t love cats.']
    },
    'excited': {
        'word': ['excited', 'suprise', 'excitement', 'excite'],
        'response': ['That\'s very exciting!', 'I\'m so excited, and I just can\'t hide it.', 'How exciting!']
    },
    'giggling': {
        'word': ['silly', 'giggle', 'giggling'],
        'response': ['He he he', 'You are very silly.', 'That makes me giggle.']
    },
    'heartbroke': {
        'word': ['hurt', 'heartbreak', 'heartbroken', 'heartbroke'],
        'response': ['Awwwww that is heartbreaking.', 'That breaks my heart.', 'My heart goes out for you.']
    },
    'inlove': {
        'word': ['love', 'heart', 'girlfriend', 'boyfriend', 'wedding', 'marriage', 'husband', 'wife', 'child', 'children', 'son', 'daughter'],
        'response': ['That is very sweet!', 'Love is in the air.', 'Love is a beautiful thing.']
    },
    'laughing': {
        'word': ['funny', 'laugh', 'laughing', 'hilarious'],
        'response': ['Ha ha ha!', 'That is very funny.']
    },
    'money': {
        'word': ['money', 'cash', 'coins', 'coin', 'shekel', 'shekels', 'dollar', 'dollars', 'cost', 'costs', 'cheap', 'expensive'],
        'response': ['Dolla dolla bill yo', 'I\'m all about the money', 'I\'m just here so I don\'t get fined.']
    },
    'no': {
        'word': ['no', 'false', 'bad', 'can\'t', 'shouldn\'t', 'wouldn\'t', 'won\'t', 'couldn\'t', 'haven\'t'],
        'response': ['Nooooooooooo', 'The answer is no.', 'This is false.']
    },
    'ok': {
        'word': ['yes', 'good', 'ok', 'okay'],
        'response': ['Yes.', 'This is true.', 'That is correct.']
    },
    'takeoff': {
        'word': ['moon', 'fly', 'mars', 'astronaut', 'liftoff', 'takeoff', 'blastoff', 'rocket', 'rocketship', 'buzz'],
        'response': ['3, 2, 1, blastoff.', 'Houston, we have a problem.', 'To infinity, and beyond.']
    }
}

swear_words = ['crap', 'jerk', 'ass']


def evaluate_user_input(user_message):
    user_message = user_message.lower().split(' ')

    for animation in animation_dict:
        for word in animation_dict[animation]['word']:
            for user_word in user_message:
                if user_word == word:
                    return animation

    return 'confused'


def get_boto_response(animation):
    if animation in animation_dict:
        return random.choice(animation_dict[animation]['response'])
    else:
        return 'I don\'t understand'


def check_user_swear(user_message):
    for word in user_message.split(' '):
        if word in swear_words:
            return word
    return False


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    is_question(user_message)
    animation = evaluate_user_input(user_message)
    if check_user_swear(user_message):
        boto_message = f'Excume me, but I\'m going to have to ask you not to say the word, {check_user_swear(user_message)}'
    else:
        boto_message = get_boto_response(animation)
    return json.dumps({"animation": animation, "msg": boto_message})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
