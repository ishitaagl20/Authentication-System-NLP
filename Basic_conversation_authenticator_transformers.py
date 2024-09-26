import spacy
import random
from transformers import pipeline

nlp = spacy.load("en_core_web_sm")

generator = pipeline('text-generation', model='distilgpt2')

def get_user_input():
    print("Please describe a memorable occasion in detail (at least 4-5 sentences):")
    return input()

def extract_entities(user_input):
    doc = nlp(user_input)
    entities = {}

    for ent in doc.ents:
        entities[ent.label_.lower()] = ent.text
    
    return entities

def generate_llm_questions_and_validate(entity, value):
    prompt = f"""
    The user has provided the following information:
    {entity}: {value}
    Generate a question based on this information, and provide the answer as well.
    """
    
    response = generator(prompt, max_length=100, num_return_sequences=1)
    
    generated_text = response[0]['generated_text'].strip()
   
    parts = generated_text.split("Answer:", 1)
    question = parts[0].replace("Question:", "").strip()
    answer = parts[1].strip() if len(parts) > 1 else ""
    
    return question, answer

def generate_random_questions(user_data, n=4):
    selected_entities = random.sample(list(user_data.keys()), n)
    questions_and_answers = {}

    for entity in selected_entities:
        value = user_data[entity]
        question, answer = generate_llm_questions_and_validate(entity, value)
        questions_and_answers[entity] = (question, answer)

    return questions_and_answers

def validate_answers(user_answers, correct_answers):
    correct = 0
    total = len(user_answers)

    for entity, user_answer in user_answers.items():
        if user_answer.lower() == correct_answers[entity].lower():
            correct += 1

    return correct, total

def authentication_result(correct, total, threshold=0.75):
    if correct / total >= threshold:
        return "Authentication Successful"
    else:
        return "Authentication Failed"


def conversational_auth():
    user_input = get_user_input()

    user_data = extract_entities(user_input)
    print("\nExtracted entity:value pairs:", user_data)

    if len(user_data) < 4:
        print("Please provide more details. At least 4 different entities are required.")
        return
    
    questions_and_answers = generate_random_questions(user_data)
    print("\nAnswer the following questions:")

    user_answers = {}
    for entity, (question, correct_answer) in questions_and_answers.items():
        print(question)
        answer = input("Your answer: ")
        user_answers[entity] = answer

    correct, total = validate_answers(user_answers, {e: a for e, (q, a) in questions_and_answers.items()})
    print(f"\nCorrect answers: {correct}/{total}")

    result = authentication_result(correct, total)
    print(result)

conversational_auth()


def validate_answer(provided_answer, correct_answers):
    """Validate the provided answer against the stored answers."""
    return provided_answer.strip().lower() in [answer.strip().lower() for answer in correct_answers]

def authenticate_user(user_id, provided_answer):
    """Authenticate the user by generating a question and validating the provided answer."""
    description = get_user_description(user_id)
    if not description:
        return "User not found"
    
    question = generate_question(description)
    print(f"Generated Question: {question}")

    correct_answers = get_user_answers(user_id)
    if not correct_answers:
        return "No answers found for the user"
    
    if validate_answer(provided_answer, correct_answers):
        return "Authentication successful"
    else:
        return "Authentication failed"

