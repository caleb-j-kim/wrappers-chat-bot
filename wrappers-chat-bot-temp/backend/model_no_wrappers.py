import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.feature_selection import RFE

# Sample dataset and preprocessing
dataset = [
    ("Hello", "Hi there! How can I assist you?"),
    ("How are you?", "I'm a bot, but thank you for asking!"),
    ("What is your name?", "I am your helpful chatbot."),
    ("Tell me a joke", "Why did the computer go to the doctor? It had a virus!"),
    ("Bye", "Goodbye! Have a great day!")
]
questions, responses = zip(*dataset)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)
y = np.arange(len(responses))

model_no_wrapper = SVC(kernel="linear")
model_no_wrapper.fit(X, y)

# Load the vectorizer and model for the wrapper method.
with open('path/to/vectorizer_with_wrapper.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('path/to/model_with_wrapper.pkl', 'rb') as f:
    model_no_wrapper = pickle.load(f)

# Load the vectorizer and model. Update 'path/to' with the actual paths to your files.
with open('path/to/vectorizer_no_wrapper.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('path/to/model_no_wrapper.pkl', 'rb') as f:
    model_no_wrapper = pickle.load(f)

# Define your responses. This can be a list or a dictionary.
responses = [
    "Response for label 0",
    "Response for label 1",
    "Response for label 2",
    # Add more responses corresponding to your model's output labels.
]

def chatbot_response_no_wrapper(user_input: str) -> str:
    # Transform the user input using the vectorizer and predict using the model.
    input_vec = vectorizer.transform([user_input])
    pred = model_no_wrapper.predict(input_vec)
    return responses[pred[0]]