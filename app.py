from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask(__name__)
# Configure the database (using SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testcases.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Set a secret key for security (replace with a long random string in production)
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize the database
db = SQLAlchemy(app)

# Define the Test Case model
class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')

    def __repr__(self):
        return f'<TestCase {self.title}>'

# --- Routes for CRUD Operations ---

# Create the database tables
@app.before_request
def create_tables():
    db.create_all()

# Retrieve all test cases (Home Page)
@app.route('/')
def index():
    test_cases = TestCase.query.all()
    return render_template('index.html', test_cases=test_cases)

# Create a new test case
@app.route('/add', methods=['GET', 'POST'])
def add_test_case():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_test_case = TestCase(title=title, description=description)
        try:
            db.session.add(new_test_case)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue adding your test case'
    else:
        return render_template('add.html')

# Update a test case
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_test_case(id):
    test_case = TestCase.query.get_or_404(id)
    if request.method == 'POST':
        test_case.title = request.form['title']
        test_case.description = request.form['description']
        test_case.status = request.form['status']
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue updating the test case'
    else:
        return render_template('edit.html', test_case=test_case)

# Delete a test case
@app.route('/delete/<int:id>')
def delete_test_case(id):
    test_case = TestCase.query.get_or_404(id)
    try:
        db.session.delete(test_case)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'There was a problem deleting that test case'

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
