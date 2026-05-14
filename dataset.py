
# -----------------------------
# IMPORT LIBRARIES
# -----------------------------

import requests  
import json      
import random    
import html      
import time      

# -----------------------------
# SETTINGS
# -----------------------------

# We want 50 questions for each game level
QUESTIONS_PER_LEVEL = 50

# The game has 15 difficulty levels
NUMBER_OF_LEVELS = 15

# Total wanted questions: 15 levels * 50 questions = 750 questions
TOTAL_QUESTIONS_NEEDED = QUESTIONS_PER_LEVEL * NUMBER_OF_LEVELS

# OpenTDB allows a maximum of 50 questions per API call
QUESTIONS_PER_API_CALL = 50

# This is the file where we will save our final dataset
OUTPUT_FILE = "questions.json"

LETTERS = ["A", "B", "C", "D"]

# This prevents the code from running forever if OpenTDB cannot give us enough questions
MAX_ROUNDS = 20


# OpenTDB only has 3 difficulty levels: easy, medium, hard.
# Our game has 15 levels, so we spread them like this:
DIFFICULTY_GROUPS = {
    "easy": range(1, 6),       # easy questions go to levels 1-5
    "medium": range(6, 11),    # medium questions go to levels 6-10
    "hard": range(11, 16)      # hard questions go to levels 11-15
}


# -----------------------------
# GET API TOKEN
# -----------------------------

def get_token():
    
    #The token helps OpenTDB remember which questions it already gave us.
    #This helps reduce duplicate questions when we make several API calls.

    url = "https://opentdb.com/api_token.php?command=request"

    response = requests.get(url)
    data = response.json()

    return data["token"]


# -----------------------------
# DOWNLOAD QUESTIONS FROM API
# -----------------------------

def download_questions(opentdb_difficulty, token):
    """
    Downloads 50 multiple-choice questions from OpenTDB.

    opentdb_difficulty can be:
    - "easy"
    - "medium"
    - "hard"
    """

    url = (
        "https://opentdb.com/api.php"
        f"?amount={QUESTIONS_PER_API_CALL}"
        f"&difficulty={opentdb_difficulty}"
        "&type=multiple"
        f"&token={token}"
    )

    response = requests.get(url)
    data = response.json()

    return data


# -----------------------------
# CHOOSE OUR GAME LEVEL
# -----------------------------

def choose_game_level(opentdb_difficulty, questions_by_level):

    # Get the possible levels for this OpenTDB difficulty
    possible_levels = list(DIFFICULTY_GROUPS[opentdb_difficulty])

    # Shuffle the possible levels so questions are spread more evenly
    random.shuffle(possible_levels)

    # Find the first level that still has space
    for level in possible_levels:
        if len(questions_by_level[level]) < QUESTIONS_PER_LEVEL:
            return level

    # If all levels in this group are already full, return None
    return None


# -----------------------------
# CONVERT QUESTION FORMAT
# -----------------------------

def convert_question(item, game_level):

    # Clean the question text
    question_text = html.unescape(item["question"])

    # Clean the correct answer
    correct_answer = html.unescape(item["correct_answer"])

    # Clean the three incorrect answers
    incorrect_answers = []

    for answer in item["incorrect_answers"]:
        incorrect_answers.append(html.unescape(answer))

    # Combine the incorrect answers with the correct answer
    all_answers = incorrect_answers + [correct_answer]

    # Shuffle the answers so the correct answer is not always in the same position
    random.shuffle(all_answers)

    # Find the position of the correct answer after shuffling
    correct_index = all_answers.index(correct_answer)

    # Convert the position into A, B, C, or D
    correct_letter = LETTERS[correct_index]

    # Create one question dictionary in our game format
    question = {
        "question": question_text,
        "A": all_answers[0],
        "B": all_answers[1],
        "C": all_answers[2],
        "D": all_answers[3],
        "correct": correct_letter,
        "difficulty": game_level,

        "source_difficulty": item["difficulty"],
        "category": html.unescape(item["category"])
    }

    return question


# -----------------------------
# CREATE THE FULL DATASET
# -----------------------------

def create_dataset():
   
    # Get the OpenTDB token to reduce duplicate questions
    token = get_token()

    questions_by_level = {}

    for level in range(1, NUMBER_OF_LEVELS + 1):
        questions_by_level[level] = []

    # This set stores question texts we already used
    # It helps us avoid duplicate questions
    seen_questions = set()

    # We repeat API calls until we have enough questions
    # or until we reach MAX_ROUNDS
    for round_number in range(1, MAX_ROUNDS + 1):

        # Count how many questions we currently have
        total_questions = sum(
            len(questions_by_level[level])
            for level in questions_by_level
        )

        # Stop if we already have enough questions
        if total_questions >= TOTAL_QUESTIONS_NEEDED:
            break

        print(f"Round {round_number}: current total = {total_questions}")

        # This counts how many new questions we add in this round
        new_questions_this_round = 0

        # Make API calls for easy, medium, and hard questions
        for opentdb_difficulty in ["easy", "medium", "hard"]:

            data = download_questions(opentdb_difficulty, token)

            # OpenTDB response_code 0 means the request worked
            # Other codes mean there are no questions or another issue happened
            if data["response_code"] != 0:
                print(f"No more questions available for {opentdb_difficulty}.")
                continue

            # Go through every question returned by the API
            for item in data["results"]:

                # Clean the question text before checking duplicates
                question_text = html.unescape(item["question"])

                # Skip this question if we already have it
                if question_text in seen_questions:
                    continue

                # Choose one of our 15 game levels for this question
                game_level = choose_game_level(opentdb_difficulty, questions_by_level)

                # If there is no available level, skip the question
                if game_level is None:
                    continue

                # Convert the question into our group's format
                question = convert_question(item, game_level)

                # Add the question to the correct level
                questions_by_level[game_level].append(question)

                # Mark this question as already used
                seen_questions.add(question_text)

                # Increase the counter of new questions
                new_questions_this_round += 1

            # Wait 5 seconds before the next API call
            # This avoids sending too many requests too quickly
            time.sleep(5)

        # If we did not get any new questions in this round, stop the loop
        if new_questions_this_round == 0:
            print("No new questions were found. Stopping.")
            break

        # Check if every level already has 50 questions
        all_levels_full = all(
            len(questions_by_level[level]) >= QUESTIONS_PER_LEVEL
            for level in questions_by_level
        )

        # If all levels are full, stop
        if all_levels_full:
            break

    # Convert the questions_by_level dictionary into one final list
    final_questions = []

    for level in range(1, NUMBER_OF_LEVELS + 1):
        final_questions.extend(questions_by_level[level])

    return final_questions, questions_by_level


# -----------------------------
# SAVE DATASET TO JSON FILE
# -----------------------------

# Create the dataset
questions, questions_by_level = create_dataset()

# Save the final list of dictionaries into questions.json
with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(questions, file, indent=4, ensure_ascii=False)


# -----------------------------
# PRINT SUMMARY
# -----------------------------

print("Dataset created successfully!")
print(f"Total questions saved: {len(questions)}")

# Print how many questions we have for each level
for level in range(1, NUMBER_OF_LEVELS + 1):
    print(f"Level {level}: {len(questions_by_level[level])} questions")