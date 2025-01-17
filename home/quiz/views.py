from django.shortcuts import render
from .forms import QuizForm
from .models import Quiz, Question, Option
import requests

def home(request):
    if request.method == 'POST':
        form = QuizForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            question_count = form.cleaned_data['question_count']
            difficulty = form.cleaned_data['difficulty']

            # Send the data to the external API (for quiz generation)
            url = "https://bharatsain.pythonanywhere.com/api/generate-quiz/"
            files = {"file": uploaded_file}
            data = {"question_count": question_count, "difficulty": difficulty}
            response = requests.post(url, files=files, data=data)

            if response.status_code == 200:
                quiz_data = response.json()

                # Save quiz metadata to the database
                quiz = Quiz.objects.create(
                    difficulty=quiz_data['metadata']['difficulty'],
                    total_questions=quiz_data['metadata']['total_questions']
                )

                # Save questions and options to the database
                for question_data in quiz_data['questions']:
                    # Create a question
                    question = Question.objects.create(
                        quiz=quiz,  # Link the question to the quiz
                        question_text=question_data['question'],
                        correct_answer=question_data['answer']
                    )

                    # Create options for the question
                    for option_text in question_data['options']:
                        Option.objects.create(
                            question=question,  # Link the option to the question
                            option_text=option_text
                        )

                # Return the quiz result page
                return render(request, "quiz.html", {"quiz_data": quiz_data})

            else:
                # Handle failure response
                return render(request, "home.html", {"form": form, "error": "Failed to generate quiz."})
    else:
        form = QuizForm()

    return render(request, "home.html", {"form": form})
