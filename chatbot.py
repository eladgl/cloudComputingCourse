import nltk
from nltk.chat.util import Chat, reflections
from main import fetch_data_from_firestore, app
from flask import render_template, request, jsonify

nltk.download('punkt')
nltk.download('wordnet')

data = fetch_data_from_firestore()

patterns = [
    (r'hi|hello|hey', ['Hello!', 'Hi there!', 'Hey!']),
    (r'how are you?', ["I'm good, thank you!", "I'm doing well, thanks for asking."]),
    (r'what is your name?', ['You can call me ChatGPT.', 'I go by the name ChatGPT.']),
    (r'(.*) your name?', ['You can call me ChatGPT.', 'I go by the name ChatGPT.']),
    (r'how old are you?', ["I'm ageless.", "I exist outside of time."]),
    (r'what can you do?', ["I can chat with you, answer questions, and help with information.", "I can assist you with various tasks and answer your queries."]),
    (r'who created you?', ["I was created by OpenAI.", "OpenAI is my creator."]),
    (r'tell me a joke', ["Why don't scientists trust atoms? Because they make up everything!", "Why did the computer go to the doctor? Because it had a virus!"]),
    (r'what is your favorite color?', ["I like all colors, but I don't have a preference.", "I don't have a favorite color, but I think all colors are interesting."]),
    (r'do you like music?', ["I don't have the ability to listen to music, but I know a lot about it!", "Music is fascinating! What kind of music do you like?"]),
    (r'can you help me?', ["Of course! What do you need help with?", "I'm here to help. How can I assist you?"]),
    (r'what is the capital of France?', ["The capital of France is Paris."]),
    (r'tell me a fun fact', ["Did you know that honey never spoils?", "A single cloud can weigh more than a million pounds."]),
    (r'what is the weather like?', ["I can't check the weather, but you can use a weather app or website for that."]),
    (r'do you have any hobbies?', ["I enjoy chatting and helping people with their questions.", "My hobby is to assist and provide information."]),
    (r'where do you live?', ["I exist in the digital world.", "I'm based in the cloud."]),
    (r'what languages can you speak?', ["I can communicate in many languages, including English, Spanish, French, and more.", "I can understand and respond in multiple languages."]),
    (r'can you solve math problems?', ["Yes, I can help with math problems. What do you need to calculate?", "Sure, tell me the math problem, and I'll do my best to solve it."]),
    (r'what is artificial intelligence?', ["Artificial intelligence is the simulation of human intelligence in machines that are programmed to think and learn.", "AI refers to the ability of machines to perform tasks that would typically require human intelligence."]),
    (r'who is the president of the United States?', ["The current president of the United States is Joe Biden."]),
    (r'what is your favorite food?', ["I don't eat food, but I know a lot about different cuisines.", "I don't have a favorite food, but I can tell you about various dishes."]),
    (r'can you tell me a story?', ["Sure! Once upon a time, in a land far away...", "I'd love to tell you a story. Once there was a curious mind..."]),
    (r'what is the meaning of life?', ["The meaning of life is a philosophical question that has been debated for centuries.", "Many people believe that the meaning of life is to find happiness and purpose."]),
    (r'what is your favorite book?', ["I don't read books, but I can help you find information about many books.", "I don't have a favorite book, but I can recommend some if you'd like."]),
    (r'do you play games?', ["I don't play games, but I know a lot about them!", "I can provide information about many games, but I don't play them myself."]),
    (r'(.*)', [lambda match: f'The number of {match.group(1)} is {data.get(match.group(1), "unknown")}']),
]

chatbot_instance = Chat(patterns, reflections)


@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = chatbot_instance.respond(user_message)
    return jsonify({'response': response})