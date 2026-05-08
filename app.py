import json

# Open the questions.json file and load it into Python
with open("questions.json", "r", encoding="utf-8") as file:
    questions = json.load(file)

# Print only the first question dictionary
print(questions[0])
