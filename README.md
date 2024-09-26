# AI Powered Authentication System

This project implements a Conversational AI Authentication System with two distinct modules:

1. **Password Strength Evaluation**: Evaluates the strength of user passwords based on a trained model.
2. **Text-Based Conversational Authentication**: Authenticates users based on dynamically generated questions from a descriptive input.

## Features

### 1. Password Strength Evaluation (Module 1)
- Uses a `RandomForestClassifier` and `TF-IDF Vectorizer` to predict the strength of a password.
- The system evaluates password strength based on factors like length, uppercase/lowercase letters, numbers, special characters, etc.

### 2. Text-Based Conversational Authentication (Module 2)
- Takes a descriptive input from the user (e.g., details about the user’s background), instead of security questions.
- Generates questions dynamically from the input using an AI model (`GenerativeModel`).
- Validates the answers provided by the user for authentication.
- This is extensible to scrapping data from user activity and then posing questions.

## Installation

Clone the repository:
   ```bash
   git clone https://github.com/your-repo/conversational-ai-authentication.git
