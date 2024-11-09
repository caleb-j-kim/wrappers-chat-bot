import numpy as np
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

model_with_wrapper = SVC(kernel="linear")
selector = RFE(model_with_wrapper, n_features_to_select=10, step=1)
selector.fit(X, y)
X_selected = selector.transform(X)

model_with_wrapper.fit(X_selected, y)

def chatbot_response_with_wrapper(user_input):
    input_vec = vectorizer.transform([user_input])
    input_vec_sel = selector.transform(input_vec)
    pred = model_with_wrapper.predict(input_vec_sel)
    return responses[pred[0]]
