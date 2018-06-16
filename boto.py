"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json

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
        'response': ['He he he', 'You are very silly', 'That makes me giggle']
    },
    'heartbroke': {
        'word': ['hurt', 'heartbreak', 'heartbroken', 'heartbroke'],
        'response': []
    },
    'inlove': {
        'word': ['love', 'heart', 'girlfriend', 'boyfriend', 'wedding', 'marriage', 'husband', 'wife', 'child', 'children', 'son', 'daughter'],
        'response': []
    },
    'laughing': {
        'word': ['funny', 'laugh', 'laughing', 'joke', 'hilarious'],
        'response': []
    },
    'money': {
        'word': ['money', 'cash', 'coins', 'coin', 'shekel', 'shekels', 'dollar', 'dollars', 'cost', 'costs', 'cheap', 'expensive'],
        'response': []
    },
    'no': {
        'word': ['no', 'false', 'bad', 'can\'t', 'shouldn\'t', 'wouldn\'t', 'won\'t', 'couldn\'t', 'haven\'t'],
        'response': []
    },
    'ok': {
        'word': ['yes', 'good', 'ok', 'okay'],
        'response': []
    },
    'takeoff': {
        'word': ['moon', 'fly', 'mars', 'astronaut', 'liftoff', 'takeoff', 'blastoff', 'rocket', 'rocketship', 'buzz'],
        'response': []
    }
}


def evaluate_user_input(user_message):
    user_message = user_message.lower().split(' ')

    for animation in animation_dict:
        for word in animation_dict[animation]['word']:
            for user_word in user_message:
                if user_word == word:
                    return animation

    return 'confused'


def is_question(user_message):
    if user_message[-1] == '?':
        return True
    else:
        return False


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    is_question(user_message)
    animation = evaluate_user_input(user_message)

    if animation == 'takeoff':
        boto_message = 'Launching in 3, 2, 1'
    elif animation == 'confused':
        boto_message = 'I don\'t understand'
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
