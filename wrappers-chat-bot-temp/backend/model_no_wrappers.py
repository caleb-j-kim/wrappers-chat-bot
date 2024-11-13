import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

# Sample dataset and responses
dataset = [
    ("Hello", "Hi there! How can I assist you?"),
    ("I need help registering for classes", "Okay great! Please send me your ENCS_Degree_Plan.xlsm file."),
    ("Bye", "Goodbye! Have a great day!")
]
questions, responses = zip(*dataset)

# Vectorize questions
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)
y = np.arange(len(responses))

# Train the model
model_no_wrapper = SVC(kernel="linear")
model_no_wrapper.fit(X, y)

# Define response function
def chatbot_response_no_wrapper(user_input: str) -> str:
    input_vec = vectorizer.transform([user_input])
    pred = model_no_wrapper.predict(input_vec)
    return responses[pred[0]]
