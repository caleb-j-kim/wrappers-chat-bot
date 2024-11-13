import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.feature_selection import RFE

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

# Apply Recursive Feature Elimination (RFE)
model_with_wrapper = SVC(kernel="linear")
selector = RFE(model_with_wrapper, n_features_to_select=10, step=1)
X_selected = selector.fit_transform(X, y)

# Train the model on selected features
model_with_wrapper.fit(X_selected, y)

# Define response function
def chatbot_response_with_wrapper(user_input: str) -> str:
    input_vec = vectorizer.transform([user_input])
    input_vec_selected = selector.transform(input_vec)
    pred = model_with_wrapper.predict(input_vec_selected)
    return responses[pred[0]]
