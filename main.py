from flask import Flask, render_template, request, jsonify
from firebase import firebase
import json
from pyngrok import ngrok

from collections import Counter, defaultdict
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
    """
    Processes a list of JSON objects to count the occurrences of specific keywords
    and their related categories.

    Args:
        data (list): List of JSON objects to be processed.

    Returns:
        Counter: A Counter object containing the frequency of keywords.
    """
    unique_students = set()
    for obj in data:
        unique_students.add(obj["User"])
    print(f"Number of different students: {len(unique_students)}")
    print(f"Students: {list(unique_students)}")

    user_actions = defaultdict(Counter)
    # Step 3: Iterate through each object in the array
    # Iterate through each object in the data
    for obj in data:
        user = obj["User"]
        description = obj.get("Description", "")
        
        # Update the user's action counter based on the description
        if "Chamfer" in description:
            user_actions[user]["Chamfer"] += 1
        elif "Extrude" in description:
            user_actions[user]["Extrude"] += 1
        elif "Revolute" in description:
            user_actions[user]["Revolute"] += 1
        elif "Move" in description:
            user_actions[user]["Move"] += 1
        elif "Suppress" in description:
            user_actions[user]["Suppress"] += 1
        elif "Unsuppress" in description:
            user_actions[user]["Unsuppress"] += 1
        elif "Unfix" in description:
            user_actions[user]["Unfix"] += 1
        elif "Hide" in description:
            user_actions[user]["Suppress"] += 1
        elif "Insert feature" in description:
            user_actions[user]["Insert feature"] += 1
        elif "Insert tab" in description:
            user_actions[user]["Insert tab"] += 1
        elif "Edit" in description:
            user_actions[user]["Edit"] += 1
        elif "Delete" in description:
            user_actions[user]["Delete"] += 1
        elif "Copy" in description:
            user_actions[user]["Copy"] += 1
        elif "Tab Bridge" in description:
            user_actions[user]["Tab Bridge"] += 1
        elif "User StudentA1 imported" in description:
            user_actions[user]["User StudentA1 imported"] += 1
        elif "User StudentA1 exported" in description:
            user_actions[user]["User StudentA1 exported"] += 1
        elif "Change" in description:
            user_actions[user]["Change"] += 1
        elif "Tab" in description and "Assembly" in description:
            user_actions[user]["Tab: Assembly"] += 1
        elif "Tab" in description and "Part Studio" in description:
            user_actions[user]["Tab: Part Studio"] += 1
        elif "Insert new tab" in description and 'Assembly' in description:
            user_actions[user]["Insert new tab: Assembly"] += 1
        elif "Insert new tab" in description and 'Part Studio' in description:
            user_actions[user]["Insert new tab: Part Studio"] += 1
        elif "Show" in description and 'Planar' in description:
            user_actions[user]["Show: Planar"] += 1
        elif "Rename tab" in description:
            user_actions[user]["Rename tab"] += 1
        elif "Insert" in description and "Part" in description:
            user_actions[user]["Insert: Part"] += 1
        elif "Fix" in description and "Part" in description:
            user_actions[user]["Fix: Part"] += 1
        elif "Show Sketch" in description:
            user_actions[user]["Show Sketch"] += 1
        else:
            user_actions[user][description] += 1
    return user_actions




def fetch_data_from_firestore():
    """
    Fetches data from the Firebase Firestore database.

    Returns:
        dict: Data fetched from Firestore in JSON format.
    """
    data = FBconn.get('/analytics/', None) #firebase db name
    data_to_return = json.loads(data['data'])
    return data_to_return

# Fetch data from Firestore when initializing the app
raw_data = fetch_data_from_firestore()
# Define chatbot patterns
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

# Add patterns based on fetched data
if(raw_data ):
    for student in raw_data.keys():
        for key in raw_data[student].keys():
            pattern = (rf'(?i)(.*{student}.*{key}.*)', [f'The number of {key} done by {student} is {raw_data[student][key]}'])
            patterns.append(pattern)
            pattern2 = (rf'(?i)(.*{key}.*{student}.*)', [f'The number of {key} done by {student} is {raw_data[student][key]}'])
            patterns.append(pattern2)

# Initialize chatbot with defined patterns
chatbot_instance = Chat(patterns, reflections)

@app.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint to handle chat requests.

    Expects JSON data with a 'message' key.

    Returns:
        JSON: A JSON object containing the chatbot's response.
    """
    user_message = request.json.get('message')
    response = chatbot_instance.respond(user_message)
    return jsonify({'response': response})

@app.route('/chatbot')
def chatbot():
    """
    Renders the chatbot interface page.

    Returns:
        HTML: The rendered chatbot interface template.
    """
    return render_template('chatbot.html')

@app.route('/upload', methods=['POST'])
def upload():
    """
    Handles file upload and processes JSON files.

    Expects a file upload with the 'file' key.

    Returns:
        HTML or JSON: Renders index.html with updated data or returns an error message.
    """
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
    """
    Endpoint to fetch data from Firestore.

    Returns:
        JSON: Data fetched from Firestore or an error message.
    """
    try:
        data = fetch_data_from_firestore()
        print(data)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """
    Renders the index page with data from Firestore.

    Returns:
        HTML: The rendered index template with data.
    """
    data = fetch_data_from_firestore()
    return render_template('index.html', json_content=data)

if __name__ == '__main__':
    app.run(debug=True)


