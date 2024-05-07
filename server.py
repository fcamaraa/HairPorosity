from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management
app.secret_key = 'very_secret_key'


items = [
    {
        'id': "1",
        'title': "Low Porosity",
        'image': "https://i.pinimg.com/736x/d8/3b/2f/d83b2f4e84cf442068bc68c2a03fd71b.jpg",
        'description': """
        Low Porosity hair has trouble maintaining moisture. When washing hair, be sure to use warm water to open up the cuticles, 
        pro tip: use heat in the form of plastic cap/steamer/deep conditioning cap when deep conditioning for best results. 
        Hydrating products including humectants, penetrating ingredients, and light oils are what you should look out for.
        Lighter products are best to use as they are easier to absorb and will avoid the potential for build up.
        """,
        'video': "https://www.youtube.com/embed/-hJLlHs-LYA?si=VSGSQ2mkRn5F_wrR"
    },
    {
        'id': "2",
        'title': "Medium Porosity",
        'image': "https://i.pinimg.com/originals/bc/45/d8/bc45d81f758651766cb532133376e641.png",
        'description': """
        Medium Porosity hair does not have trouble accepting moisture nor an issue with moisture leaving too quickly. Sulfate free 
        shampoos are best to maintain hair health. The use of hydrating conditioners and styling products like leave in conditioners 
        and curl creams are best to use.
        It is recommended to deep condition with a protein treatment once a month and deep condition with moisture one to three times a month.
        """,
        'video': "https://www.youtube.com/embed/eU39cgyXfLE?si=OlhQBjKNMM8alBfd"
    },
   {
        'id': "3",
        'title': "High Porosity",
        'image': "https://i.pinimg.com/originals/de/df/c3/dedfc305524b76dd8594a0e85b3479c2.png",
        'description': """
        High porosity hair has issue with moisture leaving it too quickly. It is able to easily and immediately accept moisture but this 
        does not last. To combat this it is best to use conditioners with ingredients like shea butter, coconut oil to provide intense hydration. 
        As hydration is key for high porosity hair, protein treatments, which cause the hair to strengthen, may cause a sensitivity issue to some. 
        Along with this since moisture leaves quickly, it is important to keep high porosity hair well hydrated, regularly seal in moisture to prevent dryness.
        """,
        'video': "https://www.youtube.com/embed/BrdBcfgg4Cs?si=4rvMzY1fDwi3tclH"
    },
]

quiz_questions = [
    {
        'id': 1,
        'type': 'drag-drop',
        'question': 'Match the labels to the correct cup:',
        'answers': {
            'image1': 'low',
            'image2': 'medium',
            'image3': 'high'
        },
        'correct_feedback': "Correct! You’ve correctly matched items.",
        'incorrect_feedback': "Incorrect, reference <a href='/learn'>porosity test page</a> to understand the difference in test results."
    },
    {
        'id': 2,
        'type': 'mcq',
        'question': 'Which Hair Porosity is best suited to use humectants, lighter oils, and penetrating ingredients?',
        'options': ['Low Porosity', 'Medium Porosity', 'High Porosity'],
        'answer': 'Low Porosity',
        'correct_feedback': "Correct! As low porosity hair is buildup prone it is best to use lighter products.",
        'incorrect_feedback': "Incorrect. As low porosity hair is buildup prone it is best to use lighter products, reference <a href='/view/1'>low porosity page</a> for more insight."
    },
    {
        'id': 3,
        'type': 'mcq',
        'question': 'Which Hair Porosity is best suited to use hydrating conditioners and curl creams?',
        'options': ['Low Porosity', 'Medium Porosity', 'High Porosity'],
        'answer': 'Medium Porosity',
        'correct_feedback': "Correct! Medium porosity hair flourishes on hydration, provided by both items.",
        'incorrect_feedback': "Incorrect, medium porosity hair flourishes on hydration, provided by both conditioners and curl creams, reference <a href='/view/2'>medium porosity page</a> for more insight."
    },
    {
        'id': 4,
        'type': 'mcq',
        'question': 'Which Hair Porosity is best suited to use conditioners with ingredients like shea butter, coconut oil to provide intense hydration?',
        'options': ['Low Porosity', 'Medium Porosity', 'High Porosity'],
        'answer': 'High Porosity',
        'correct_feedback': "Correct! High porosity hair has trouble maintaining moisture, these heavier ingredients will be sure to seal in moisture.",
        'incorrect_feedback': "Incorrect, High porosity hair has trouble maintaining moisture, these heavier ingredients will be sure to seal in moisture, reference <a href='/view/3'>high porosity page</a> for more insight."
    },
    {
        'id': 5,
        'type': 'mcq',
        'question': 'What items do you need for the porosity test?',
        'options': [
            'Bowl/cup of water and strands of hair as is',
            'Bowl/cup of water and clean strands of hair',
            'Bowl/cup of water and a clump of hair as is'
        ],
        'answer': 'Bowl/cup of water and clean strands of hair',
        'correct_feedback': "Correct! A bowl/cup of water and clean hair strands are needed to conduct the porosity test.",
        'incorrect_feedback': "Incorrect, A bowl/cup of water and clean hair strands are needed to conduct the porosity test, reference <a href='/learn'>  porosity test page </a> for more insight."
    },
    {
        'id': 6,
        'type': 'mcq',
        'question': 'Which Hair Porosity type is typically more sensitive to protein treatments?',
        'options': ['Low Porosity', 'Medium Porosity', 'High Porosity'],
        'answer': 'High Porosity',
        'correct_feedback': "Correct! As hydration is key for high porosity hair, protein treatments, which cause the hair to strengthen, may cause a sensitivity issue to some.",
        'incorrect_feedback': "Incorrect, As hydration is key for high porosity hair, protein treatments, which cause the hair to strengthen, may cause a sensitivity issue to some, reference <a href='/view/3'>high porosity page</a> for more insight."
    },
    {
        'id': 7,
        'type': 'mcq',
        'question': 'Which practice is best for managing low porosity hair?',
        'options': [
            'Using heat to open hair cuticles during conditioning',
            'Applying heavy butters and oils frequently',
            'Using protein treatments regularly'
        ],
        'answer': 'Using heat to open hair cuticles during conditioning',
        'correct_feedback': "Correct! Heat is a great tool to use when moisturizing low porosity hair as it opens the hair cuticle.",
        'incorrect_feedback': "Incorrect, Heat is a great tool to use when moisturizing low porosity hair as it opens the hair cuticle, reference <a href='/view/1'>low porosity page</a> for more insight."
    }
]

app.jinja_env.filters['round'] = round

@app.route('/quiz')
def start_quiz():
    session['current_index'] = 0  # Start from the first question
    session['score'] = 0          # Reset score
    session['feedbacks'] = []     # Reset feedbacks
    current_index = session['current_index']
    total_questions = len(quiz_questions)  # Assuming 'quiz_questions' is your list of all questions

    # Ensure that the current index is within the bounds of the quiz_questions list
    if current_index < total_questions:
        question = quiz_questions[current_index]  # Retrieve the current question based on the index
    else:
        return redirect(url_for('quiz_results'))  # Redirect to results page or a completion page

    return render_template('quizQuestionsTemplate.html', current_index=current_index, total_questions=total_questions, question=question)


# Route to display the current question
# Constants
POINTS_PER_CORRECT_ANSWER = 100 / 7  # Approximately 14.29 points per correct answer
@app.route('/show_question', methods=['GET', 'POST'])
def show_question():
    if 'current_index' not in session:
        session['current_index'] = 0
        session['score'] = 0
        session['feedbacks'] = []
        session['answered'] = False
        session['dropzone_states'] = {'image1': '', 'image2': '', 'image3': ''}  # Ensure it's initialized

    current_index = session['current_index']
    if current_index >= len(quiz_questions):
        return redirect(url_for('quiz_results'))

    question = quiz_questions[current_index]
    feedback = ''
    alert_flag = False
    correct_flags = {}

    # Retrieve dropzone states from the session or initialize
    dropzone_states = session.get('dropzone_states', {'image1': '', 'image2': '', 'image3': ''})

    if request.method == 'POST':
        if question['type'] == 'drag-drop':
            # Extracting form data for each dropzone
            dropzone1_filled = request.form.get('image1', '').strip()
            dropzone2_filled = request.form.get('image2', '').strip()
            dropzone3_filled = request.form.get('image3', '').strip()
            
            # Storing the states in the session for persistence across requests
            session['dropzone_states']['image1'] = dropzone1_filled
            session['dropzone_states']['image2'] = dropzone2_filled
            session['dropzone_states']['image3'] = dropzone3_filled

            # Set correct flags based on answers
            correct_flags = {
                'correct_image1': dropzone1_filled == question['answers']['image1'],
                'correct_image2': dropzone2_filled == question['answers']['image2'],
                'correct_image3': dropzone3_filled == question['answers']['image3']
            }

            # Verify all answers are filled and correct
            if all([dropzone1_filled, dropzone2_filled, dropzone3_filled]):
                answers_correct = all(correct_flags.values())
                feedback = question['correct_feedback'] if answers_correct else question['incorrect_feedback']
                session['answered'] = True
                if answers_correct:
                    session['score'] += POINTS_PER_CORRECT_ANSWER
            else:
                alert_flag = True
                feedback = 'Please complete all parts of the question.'
                session['answered'] = False

        elif question['type'] == 'mcq':
            user_answer = request.form.get('answer', '').strip()
            correct_answer = question.get('answer', '')
            if user_answer == correct_answer:
                feedback = question['correct_feedback']
                session['score'] += POINTS_PER_CORRECT_ANSWER
                session['answered'] = True
            else:
                feedback = question['incorrect_feedback']
                session['answered'] = True

        session['feedbacks'].append({'question': question['question'], 'feedback': feedback})

    # Always pass necessary data to the template
    return render_template('quizQuestionsTemplate.html', question=question, feedback=feedback,
                           score=session['score'], current_index=current_index,
                           total_questions=len(quiz_questions), alert_flag=alert_flag,
                           answered=session['answered'], dropzone_states=dropzone_states, **correct_flags)



@app.route('/next_question', methods=['POST'])
def next_question():
    # Only allow moving to the next question if the current question has been answered
    if 'answered' in session and session['answered']:
        # Reset the 'answered' flag for the next question
        session['answered'] = False
        
        # Check if there's a next question and increment the index
        if 'current_index' in session and session['current_index'] < len(quiz_questions) - 1:
            session['current_index'] += 1
        # Redirect to the quiz result page if there are no more questions
        elif session['current_index'] >= len(quiz_questions) - 1:
            return redirect(url_for('quiz_results'))

    # Redirect back to the current question if it hasn't been answered yet
    return redirect(url_for('show_question'))



@app.route('/quiz_results', methods=['GET', 'POST'])
def quiz_results():
    score = round(session.get('score', 0)) 
    feedbacks = session.get('feedbacks', []) 

    
    return render_template('quiz_results.html', score=score, feedbacks=feedbacks)

def get_item_by_id(id):
   
    return next((item for item in items if item['id'] == str(id)), None)

def total_items_count():
    return len(items)


@app.route('/')
def home():
    print("Items being sent to template:", items) 
    return render_template('main.html', items=items)


@app.route('/learn')
def learn():
    return render_template('porosityTest.html', item=items)

@app.route('/quizStart')
def quizStart():
    return render_template('quizStart.html')

@app.route('/view/<int:id>')
def view(id):
    item = get_item_by_id(id)
    if not item:
        return "Item not found", 404 

   
    prev_id = id - 1 if id > 1 else None
    next_id = id + 1 if id < len(items) else None

    return render_template('porosityContent.html', item=item, prev_id=prev_id, next_id=next_id)

@app.route('/moreInformation')
def moreInformation():
    return render_template('moreInformation.html')

@app.route('/leaveaComment')
def leaveaComment():
    return render_template('leaveaComment.html')

@app.route('/quizQuestions')
def quizQuestions():
    return render_template('quizQuestions.html')


@app.route('/reset-quiz')
def reset_quiz():
    
    session['current_index'] = 0
    session['score'] = 0
    
    return redirect(url_for('start_quiz', qid=1))


@app.route('/reset-score', methods=['POST'])
def reset_score():
    session.pop('score', None)
    return jsonify({'score': 0})




if __name__ == '__main__':
    app.run(debug=True)