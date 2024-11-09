import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

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

def chatbot_response_no_wrapper(user_input):
    input_vec = vectorizer.transform([user_input])
    pred = model_no_wrapper.predict(input_vec)
    return responses[pred[0]]
