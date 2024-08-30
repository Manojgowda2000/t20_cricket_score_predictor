from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load the pre-trained model
pipe = pickle.load(open('pipe1.pkl', 'rb'))

# List of teams and cities
teams = [
    'Australia', 'India', 'Bangladesh', 'New Zealand', 'South Africa',
    'England', 'West Indies', 'Afghanistan', 'Pakistan', 'Sri Lanka'
]

cities = [
    'Colombo', 'Mirpur', 'Johannesburg', 'Dubai', 'Auckland', 'Cape Town',
    'London', 'Pallekele', 'Barbados', 'Sydney', 'Melbourne', 'Durban',
    'St Lucia', 'Wellington', 'Lauderhill', 'Hamilton', 'Centurion',
    'Manchester', 'Abu Dhabi', 'Mumbai', 'Nottingham', 'Southampton',
    'Mount Maunganui', 'Chittagong', 'Kolkata', 'Lahore', 'Delhi', 'Nagpur',
    'Chandigarh', 'Adelaide', 'Bangalore', 'St Kitts', 'Cardiff',
    'Christchurch', 'Trinidad'
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve form data
        batting_team = request.form.get('batting_team')
        bowling_team = request.form.get('bowling_team')
        city = request.form.get('city')
        current_score = int(request.form.get('current_score', 0))
        overs = float(request.form.get('overs', 0))
        wickets = int(request.form.get('wickets', 0))
        last_five = int(request.form.get('last_five', 0))

        # Calculate additional inputs
        balls_left = 120 - int(overs * 6)
        wickets_left = 10 - wickets
        crr = current_score / overs if overs > 0 else 0

        # Create a DataFrame for the model
        input_df = pd.DataFrame({
            'batting_team': [batting_team], 
            'bowling_team': [bowling_team],
            'city': [city], 
            'current_score': [current_score],
            'balls_left': [balls_left], 
            'wickets_left': [wickets_left], 
            'crr': [crr], 
            'last_five': [last_five]
        })

        # Predict using the loaded model
        predicted_score = pipe.predict(input_df)[0]

        # Render the result with the input form
        return render_template('index.html', teams=teams, cities=cities, predicted_score=int(predicted_score))

    # Render the form template
    return render_template('index.html', teams=teams, cities=cities)

if __name__ == '__main__':
    app.run(debug=True)
