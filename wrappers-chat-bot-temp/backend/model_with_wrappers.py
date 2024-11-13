import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.feature_selection import RFE

# Intro prompts and preprocessing
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

model_with_wrapper = SVC(kernel="linear")
selector = RFE(model_with_wrapper, n_features_to_select=10, step=1)
selector.fit(X, y)
X_selected = selector.transform(X)

model_with_wrapper.fit(X_selected, y)

# Load the vectorizer and model for the wrapper method.
with open('path/to/vectorizer_with_wrapper.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('path/to/model_with_wrapper.pkl', 'rb') as f:
    model_with_wrapper = pickle.load(f)

# Define your responses corresponding to the model's output labels.
responses = [
    "Response for label 0 with wrapper",
    "Response for label 1 with wrapper",
    "Response for label 2 with wrapper",
    # Add more responses as needed.
]
# Load the vectorizer and model for the wrapper method.
with open('path/to/vectorizer_with_wrapper.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('path/to/model_with_wrapper.pkl', 'rb') as f:
    model_with_wrapper = pickle.load(f)

# Define your responses corresponding to the model's output labels.
responses = [
    "Response for label 0 with wrapper",
    "Response for label 1 with wrapper",
    "Response for label 2 with wrapper",
    # Add more responses as needed.
]

def chatbot_response_with_wrapper(user_input: str) -> str:
    # Transform the user input and predict using the model with the wrapper method.
    input_vec = vectorizer.transform([user_input])
    pred = model_with_wrapper.predict(input_vec)
    return responses[pred[0]]
