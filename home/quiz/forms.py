from django import forms

class QuizForm(forms.Form):
    file = forms.FileField(label="Upload PDF", required=False)  # This handles the file upload for PDF
    question_count = forms.IntegerField(label="Number of Questions", min_value=1, required=True)  # Number of questions to generate
    difficulty_choices = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    difficulty = forms.ChoiceField(label="Difficulty Level", choices=difficulty_choices, required=True)  # Difficulty level selection
