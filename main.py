from flask import Flask, render_template, request, jsonify
from firebase import firebase
import json
# from pyngrok import ngrok

from collections import Counter
import nltk
from nltk.chat.util import Chat, reflections

FBconn = firebase.FirebaseApplication('https://braude-92cfa-default-rtdb.europe-west1.firebasedatabase.app/',None) #firebase db url

# Initialize NLTK resources
nltk.download('punkt')
nltk.download('wordnet')

#!ngrok authtoken 2kFSSDLyys45fskfBCtXvRitxDT_7Qq1QNzvYYRrmAAnFo5xn
app = Flask(__name__)

# Set the authtoken and create a public URL
# ngrok.set_auth_token('2bcUwDOFwTWFQnUax6JMXZjnf8u_2pLSVQj2iZJCinp6TwuUv')  # Replace 'your_authtoken' with your actual authtoken
# public_url = ngrok.connect(5000, bind_tls=True)  # Specify port as an integer and bind_tls as True
# print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:5000\"")

def indexing(data):
    frequency_counter = Counter()
    # Step 3: Iterate through each object in the array
    for obj in data:
        # Step 4: Extract keys and values from each object
        for key, value in obj.items():
            # Step 5: Count frequencies of each key-value pair
            if key == "Time":
                # Count occurrences of the key "Time" itself
                frequency_counter[key] += 1
            elif key == "Description":
                # Check for special conditions in "Description" values
                if "Chamfer" in value:
                    frequency_counter["Chamfer"] += 1
                elif "Extrude" in value:
                    # Count occurrences of "Extrude" within the values of "Description"
                    frequency_counter["Extrude"] += 1
                elif "Revolute" in value:
                    frequency_counter["Revolute"] += 1
                elif "Move" in value:
                    frequency_counter["Move"] += 1
                elif "Suppress" in value:
                    frequency_counter["Suppress"] += 1
                elif "Unsuppress" in value:
                    frequency_counter["Unuppress"] += 1
                elif "Unfix" in value:
                    frequency_counter["Unfix"] += 1
                elif "Hide" in value:
                    frequency_counter["Suppress"] += 1
                elif "Insert feature" in value:
                    frequency_counter["Insert feature"] += 1
                elif "Insert tab" in value:
                    frequency_counter["Insert tab"] += 1
                elif "Edit" in value:
                    frequency_counter["Edit"] += 1
                elif "Delete" in value:
                    frequency_counter["Delete"] += 1
                elif "Copy" in value:
                    frequency_counter["Copy"] += 1
                elif "Tab Bridge" in value:
                    frequency_counter["Tab Bridge"] += 1
                elif "User StudentA1 imported" in value:
                    frequency_counter["User StudentA1 imported"] += 1
                elif "User StudentA1 exported" in value:
                    frequency_counter["User StudentA1 exported"] += 1
                elif "Change" in value:
                    frequency_counter["Change"] += 1
                elif "Tab" in value and "Assembly" in value:
                    frequency_counter["Tab: Assembly"] += 1
                elif "Tab" in value and "Part Studio" in value:
                    frequency_counter["Tab: Part Studio"] += 1
                elif "Insert new tab" in value and 'Assembly' in value:
                    frequency_counter["Insert new tab: Assembly"] += 1
                elif "Insert new tab" in value and 'Part Studio' in value:
                    frequency_counter["Insert new tab: Part Studio"] += 1
                elif "Show" in value and 'Planar' in value:
                    frequency_counter["Show: Planar"] += 1
                elif "Rename tab" in value:
                    frequency_counter["Rename tab"] += 1
                elif "Insert" in value and "Part" in value:
                    frequency_counter["Insert: Part"] += 1
                elif "Fix" in value and "Part" in value:
                    frequency_counter["Fix: Part"] += 1
                elif "Show Sketch" in value:
                    frequency_counter["Show Sketch"] += 1
                else:
                    frequency_counter[value] += 1
    return frequency_counter




def fetch_data_from_firestore():
    data = FBconn.get('/analytics/', None) #firebase db name
    data_to_return = json.loads(data['data'])
    return data_to_return

# Fetch data from Firestore when initializing the app
raw_data = fetch_data_from_firestore()

patterns = [
    (r'hi|hello|hey', ['Hello!', 'Hi there!', 'Hey!']),
    (r'how are you?', ["I'm good, thank you!", "I'm doing well, thanks for asking."]),
    (r'what is your name?', ['You can call me zebraGPT.', 'I go by the name zebraGPT.']),
    (r'(.*) your name?', ['You can call me zebraGPT.', 'I go by the name zebraGPT.']),
    (r'how old are you?', ["I'm ageless.", "I exist outside of time."]),
    (r'what can you do?', ["I can chat with you, answer questions, and help with information.", "I can assist you with various tasks and answer your queries."]),
    (r'who created you?', ["I was created by chay-tech Team.", "chay himself is my creator."]),
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
]

if(raw_data ):
    for key in raw_data.keys():
        pattern = (rf'(?i)(.*{key}.*)', [f'The number of {key} is {raw_data[key]}'])
        patterns.append(pattern)

chatbot_instance = Chat(patterns, reflections)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = chatbot_instance.respond(user_message)
    return jsonify({'response': response})

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        file_content = file.read().decode('utf-8')
        try:
            json_content = json.loads(file_content)
            json_as_index = indexing(json_content)
            
            # Convert Counter object to dictionary
            counter_dict = {}
            for key, value in json_as_index.items():
                counter_dict[key] = value
            # Convert dictionary to JSON string
            json_obj = json.dumps(counter_dict, indent=4)
            print(counter_dict)
            # Store JSON content in Firestore
            result = FBconn.put('/analytics/', 'data' ,json_obj) #firebase db name

            # Process the JSON content here
            return render_template('index.html', json_content=fetch_data_from_firestore())
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON file'}), 400
    else:
        return jsonify({'error': 'Invalid file type, only JSON files are allowed'}), 400

@app.route('/getData', methods=['GET'])
def get_data():
    try:
        data = fetch_data_from_firestore()
        print(data)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    data = fetch_data_from_firestore()
    return render_template('index.html', json_content=data)

if __name__ == '__main__':
    app.run(debug=True)


