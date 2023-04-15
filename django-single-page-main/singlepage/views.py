from django.shortcuts import render, redirect
from django.http import HttpResponse
from nltk import word_tokenize
import random
import logging

def process_line(movie_line):

    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", "would"]

    #value_line = "'''Dumbledore''': should have known would here...Professor McGonagall."
    
    value_line = []

    demo_line = movie_line.lower()
    demo_words = word_tokenize(demo_line)


    for word in demo_words:
        if word not in stopwords and word.isalnum():
            value_line.append(word)


    length = len(value_line)
    
    if length < 1:
        return []
    
    chosen_word_place = random.randint(0, length-1)
    chosen_word = value_line[chosen_word_place]

    presented_line = demo_line.replace(chosen_word, "________")

    
    return [presented_line, chosen_word, length]


def gen_possible_lines():
    movie_script = open("harry_potter_1.txt", "r")

    count = 0
    possible_lines = []

    for movie_line in movie_script:
        quiz_line = process_line(movie_line)
        count += 1
        if quiz_line != []:
            possible_lines.append(quiz_line)
    #     print(movie_line)
    #     print(quiz_line)

    #TODO: LOOP THROUGH
    #TODO: choose chunks
    slice_of_lines = random.randint(0, count-100)
    possible_lines = possible_lines[slice_of_lines:len(possible_lines)]
    return possible_lines



# def index(request):
#     request.session.flush()
#     request.session.cycle_key()
#     # Any additional code you want to run after resetting the session
#     return HttpResponse("Session reset successfully.")

def refresh_session(request):
    request.session.flush()
    return redirect('index')


def index(request):
    
    if 'possible_lines' not in request.session:
        possible_lines = gen_possible_lines()
        request.session['possible_lines'] = possible_lines
        
    if 'previous_ans' not in request.session or request.session['previous_ans'] is None:
        request.session['previous_ans'] = []
        previous_ans = []

    if 'question' in request.session and 'previous_ans' in request.session:
        question = request.session['question']
        answer = request.session['answer']
        previous_ans = request.session['previous_ans']
        previous_ans.append(question.replace('________', f'<b>{answer}</b>') + '<br>')

    score = request.session.get('score', {'correct': 0, 'incorrect': 0})

    guess = request.POST.get('guess')
    request.session['guess'] = guess
    if guess is not None and 'answer' in request.session:
        answer = request.session['answer']
        if guess.lower() == answer.lower():
            score['correct'] += 1
        else:
            score['incorrect'] += 1
        
        request.session['score'] = score

    question, answer, _ = request.session['possible_lines'].pop(0)
    request.session['answer'] = answer
    request.session['question'] = question
    

    context = {
        'answer': answer,
        'previous_ans': previous_ans,
        'question': question,
        'guess': guess,
        'score': score,
    }
    return render(request, 'singlepage/index.html', context)






# question = "none"
# answer = "none"
# previous_ans = []
# guess = "None"
# count_wrong = 0
# count_right = 0
# possible_lines = gen_possible_lines()


# def index(request):

#     global question
#     global answer
#     global guess
#     global previous_ans

#     # if the user submits a guess
#     if request.method == 'POST':
#         guess = request.POST.get('guess')

#         if guess == answer:
 
#             # previous_ans.append(question.replace('________', f'<b>{answer}</b>') + '<br>')
#             request.session['previous_ans'] = previous_ans
    
#     previous_ans.append(question.replace('________', f'<b>{answer}</b>') + '<br>')

#     question, answer, _ = possible_lines.pop(0)


#     context = {
#         'question': question,
#         'answer': answer,
#         'previous_ans': previous_ans,
#         'guess': guess,
#     }
#     return render(request, 'singlepage/index.html', context)


