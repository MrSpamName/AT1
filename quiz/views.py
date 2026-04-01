from django.shortcuts import render, redirect
import random

QUESTIONS = [
    {
        "question": "What is the closest star to Earth?",
        "choices": ["The Sun", "Proxima Centauri", "Sirius", "Betelgeuse"],
        "answer": "The Sun"
    },
    {
        "question": "How many planets are in our Solar System?",
        "choices": ["7", "8", "9", "10"],
        "answer": "8"
    },
    {
        "question": "What is the largest planet in our Solar System?",
        "choices": ["Saturn", "Neptune", "Earth", "Jupiter"],
        "answer": "Jupiter"
    },
    {
        "question": "What is a light-year a measure of?",
        "choices": ["Time", "Speed", "Distance", "Brightness"],
        "answer": "Distance"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "choices": ["Venus", "Mars", "Mercury", "Saturn"],
        "answer": "Mars"
    },
    {
        "question": "What force keeps planets in orbit around the Sun?",
        "choices": ["Magnetism", "Friction", "Gravity", "Inertia"],
        "answer": "Gravity"
    },
    {
        "question": "What is the name of our galaxy?",
        "choices": ["Andromeda", "The Milky Way", "Triangulum", "Sombrero"],
        "answer": "The Milky Way"
    },
    {
        "question": "What is the phase of the Moon when it is fully illuminated?",
        "choices": ["New Moon", "Crescent Moon", "Quarter Moon", "Full Moon"],
        "answer": "Full Moon"
    },
    {
        "question": "Which planet has the most moons?",
        "choices": ["Jupiter", "Uranus", "Saturn", "Neptune"],
        "answer": "Saturn"
    },
    {
        "question": "What is the name of NASA's most famous space telescope?",
        "choices": ["Hubble", "Kepler", "Spitzer", "Chandra"],
        "answer": "Hubble"
    },
    {
        "question": "What is the centre of our Solar System?",
        "choices": ["Earth", "The Moon", "The Sun", "Jupiter"],
        "answer": "The Sun"
    },
    {
        "question": "Which planet has rings around it?",
        "choices": ["Mars", "Venus", "Saturn", "Mercury"],
        "answer": "Saturn"
    },
]

def home(request):
    request.session.flush()
    return render(request, 'quiz/home.html')

def quiz(request):
    # Set up a fresh randomised question order
    if 'question_order' not in request.session:
        order = random.sample(range(len(QUESTIONS)), 10)
        request.session['question_order'] = order
        request.session['current'] = 0
        request.session['score'] = 0
        request.session['answers'] = []

    current = request.session['current']
    order = request.session['question_order']

    # All 10 questions answered — go to results
    if current >= 10:
        return redirect('results')

    q_index = order[current]
    question_data = QUESTIONS[q_index]

    selected = None
    correct = None
    answered = False

    if request.method == 'POST':
        selected = request.POST.get('choice')
        correct = question_data['answer']
        answered = True

        if selected == correct:
            request.session['score'] += 1

        answers = request.session['answers']
        answers.append({
            'question': question_data['question'],
            'selected': selected,
            'correct': correct,
            'is_correct': selected == correct,
        })
        request.session['answers'] = answers
        request.session['current'] = current + 1

    return render(request, 'quiz/quiz.html', {
        'question': question_data['question'],
        'choices': question_data['choices'],
        'current': current + 1,
        'total': 10,
        'selected': selected,
        'correct': correct,
        'answered': answered,
    })

def results(request):
    score = request.session.get('score', 0)
    answers = request.session.get('answers', [])
    return render(request, 'quiz/results.html', {
        'score': score,
        'answers': answers,
    })