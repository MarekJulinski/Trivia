import requests
from tkinter import *
import random
import html

def create_screen():
    screen = Tk()
    screen.title('TRIVIA QUIZ')
    screen.config(padx=50, pady=50, height=1000)
    
    return screen
    
def get_questions():
    response = requests.get('https://opentdb.com/api.php?amount=10')

    data = response.json()['results']
    
    return data

def multiple(question):
    global frame
    global answers
    
    frame = Frame(master=screen, pady=25)
    
    buttons = []
    
    answers = {}
    
    answer = question['correct_answer']
    
    answer = html.unescape(answer)
    
    correct_answer = Button(master=frame, text=answer, command=correct, width=28, font=['New Roman Times', 20, 'italic'], pady=10)
    
    buttons.append(correct_answer)
    
    
    for incorrect in question['incorrect_answers']:
        
        incorrect = html.unescape(incorrect)
        
        incorrect_answer = Button(master=frame, text=incorrect, command=fail, width=28, font=['New Roman Times', 20, 'italic'], pady=10)
        buttons.append(incorrect_answer)
    
    answers = {'correct' : buttons[0], 'incorrect' : buttons[1 : len(buttons)]}
    
    random.shuffle(buttons)
    
    for button in buttons:
        button.pack()
        
    frame.pack()

def bool_question(question):
    global frame
    global answers
    
    frame = Frame(master=screen, width=400, pady=20)
    answers = {}
    
    if question['correct_answer'] == 'True':
        true = Button(master=frame, text='T', command=correct, font=['New Roman Times', 25, 'italic'], pady=5, padx=50, width=4)
        
        true.pack(side=LEFT)
        
        false = Button(master=frame, text='F', command=fail, font=['New Roman Times', 25, 'italic'], pady=5, padx=50, width=4)
        
        false.pack(side=RIGHT)
        
        answers['correct'] = true
        
        answers['incorrect'] = false
    else:
        true = Button(master=frame, text='T', command=fail, font=['New Roman Times', 25, 'italic'], pady=5, padx=50, width=4)
        
        true.pack(side=LEFT)
        
        false = Button(master=frame, text='F', command=correct, font=['New Roman Times', 25, 'italic'], pady=5, padx=50, width=4)
        
        false.pack(side=RIGHT)
        
        answers['correct'] = false
        
        answers['incorrect'] = true
    
    frame.pack()
   
def correct():
    global score_num
    global canvas
    global screen
    global answers
    
    answers['correct'].configure(highlightbackground = 'green')
    
    if type(answers['incorrect']) == list:
        for button in answers['incorrect']:
            button.configure(highlightbackground = 'red')
    else:
        answers['incorrect'].config(highlightbackground = 'red')
        
    canvas.itemconfig(box, fill = 'green')
    
    score_num += 1
    
    score_text.set(f'Score: {score_num}')
    
    screen.after(3000, correct_part_two)
    
def correct_part_two():
    global question_num
    global canvas
    global frame
    
    canvas.itemconfig(box, fill = 'white')
    
    frame.destroy()
    
    if question_num < 9:
        question_num += 1
        display_question(question_num)
    else:
        end_screen()
    
def fail():
    global canvas
    global screen
    global answers
    
    answers['correct'].configure(highlightbackground = 'green')
    
    if type(answers['incorrect']) == list:
        for button in answers['incorrect']:
            button.configure(highlightbackground = 'red')
    else:
        answers['incorrect'].config(highlightbackground = 'red')
    
    
    canvas.itemconfig(box, fill = 'red')
    
    screen.after(3000, fail_part_two)
        
def fail_part_two():
    global question_num
    global canvas
    global frame
    
    canvas.itemconfig(box, fill = 'white')
    
    frame.destroy()
    
    if question_num < 9:
        question_num += 1
        display_question(question_num)
    else:
        end_screen()
    
def display_question(n):
    question = questions[n]['question']
    question = html.unescape(question)
    
    if questions[n]['type'] == 'multiple':
        canvas.itemconfig(quest, text = question)
        multiple(questions[n])
    if questions[n]['type'] == 'boolean':
        canvas.itemconfig(quest, text = question)
        bool_question(questions[n])
        
def end_screen():
    global frame
    global canvas
    global score_num
    global score
    
    score.destroy()
    frame.destroy()
    canvas.destroy()
    
    label = Label(master=screen, text=f'FINAL SCORE: {score_num}', font=('New Roman Times', 40, 'bold'), pady=20)
    label.pack()
    
    button = Button(master=screen, text='EXIT', font=('New Roman Times', 20, 'italic'), command=screen.quit, pady=20)
    button.pack()

if __name__ == '__main__':
    screen = create_screen()
    
    score_text = StringVar()
    score_num = 0
    score_text.set((f'Score: {score_num}'))
    score = Label(screen, textvariable=score_text, font=('New Roman Time', 25, 'bold'), width=30, justify='right')
    score.pack()
    
    canvas = Canvas(screen, width=400, height=400)
    box = canvas.create_rectangle(0, 0, 2000, 2000, fill = 'white')
    canvas.pack()
    question_text = StringVar()
    quest = canvas.create_text(200, 200, font=('New Roman Times', 25, 'italic'), fill='black', text=question_text, width=390, justify='center')
    
    questions = get_questions()
    
    question_num = 0
    
    display_question(question_num)
    
    screen.mainloop()