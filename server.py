from flask import Flask, render_template, request, redirect, url_for  # Import redirect and url_for here

app = Flask(__name__)

items = [
    {
        'id': "1",
        'title': "Low Porosity",
        'image': "https://i.ibb.co/zxjMxDM/Screenshot-2024-04-17-at-6-51-09-PM-removebg-preview.png",
        'description': """
        Low Porosity hair has trouble maintaining moisture. When Washing hair be sure to use warm water to open up the cuticles. 
        Hydrating Products Including humectants, penetrating ingredients, and light oils are what you should look out for.
        Lighter products are best to use as they are easier to absorb and will avoid the potential for build up.
        """
    },
    {
        'id': "2",
        'title': "Medium Porosity",
        'image': "https://i.ibb.co/ssjg5z2/Screenshot-2024-04-17-at-6-53-08-PM-removebg-preview.png",
        'description': """
        Medium Porosity hair does not have trouble accepting moisture nor an issue with moisture leaving too quickly. Sulfate free 
        shampoos are best to maintain hair health. The use of hydrating conditioners and styling products like leave in conditioners 
        and curl creams are best to use.
        It is recommended to deep condition with a protein treatment once a month and deep condition with moisture one to three times a month.
        """
    },
    {
        'id': "3",
        'title': "High Porosity",
        'image': "https://i.ibb.co/s1s8ttt/Screenshot-2024-04-17-at-6-54-24-PM-removebg-preview.png",
        'description': """
        High porosity hair has issue with moisture leaving it too quickly. It is able to easily and immediately accept moisture but this 
        does not last. To combat this it is best to use conditioners with ingredients like shea butter, coconut oil to provide intense hydration. 
        As moisture leaves quickly, it is important to keep high porosity hair well hydrated, regularly seal in moisture to prevent dryness.
        """
    },
]


@app.route('/')
def home():
    print("Items being sent to template:", items)  # Debug print to console
    return render_template('main.html', items=items)


@app.route('/learn')
def learn():
    return render_template('porosityTest.html', item=items)

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/view/<id>')
def view(id):
    # Fetch the item with matching id
    item = next((item for item in items if item['id'] == id), None)
    return render_template('porosityContent.html', item=item)

@app.route('/moreInformation')
def moreInformation():
    return render_template('moreInformation.html')

@app.route('/leaveaComment')
def leaveaComment():
    return render_template('leaveaComment.html')

@app.route('/quizQuestions')
def quizQuestions():
    return render_template('quizQuestions.html')
@app.route('/quizQuestion1')
def quizQuestion1():
    return render_template('quizQuestion1.html')

@app.route('/quizQuestion2',  methods=['GET', 'POST'])
def quizQuestion2():
    return render_template('quizQuestion2.html')
    

@app.route('/quizQuestion3',  methods=['GET', 'POST'])
def quizQuestion3():
    # Logic here to handle answer validation or other tasks
    # Redirect to quizQuestion4 or render it directly, depending on your flow
    return render_template('quizQuestion3.html')

@app.route('/quizQuestion4',  methods=['GET', 'POST'])
def quizQuestion4():
    return render_template('quizQuestion4.html')

@app.route('/quizResults',  methods=['GET', 'POST'])
def quizResults():
    return render_template('quizResults.html')


if __name__ == '__main__':
    app.run(debug=True)