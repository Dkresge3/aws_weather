from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendation = None
    additional_prompt = None
    location = request.form.get('location', 'Enter a city or zipcode')
    if request.method == 'POST':
        # Assuming temp is fetched based on the location (this logic needs to be implemented)
        temp = get_temperature_for_location(location)
        recommendation = get_clothing_recommendation(temp)
        additional_prompt = request.form.get('text')
    return render_template('index.html', recommendation=recommendation, location=location, additional_prompt=additional_prompt)

def get_temperature_for_location(location):
    # Implement your logic to get temperature based on location
    # For demonstration, returning a dummy value
    return 25  # example temperature value

def get_clothing_recommendation(temp):
    # Implement your logic to give clothing recommendation based on temperature
    if temp <= 0:
        return "Wear a heavy coat"
    elif 0 < temp <= 10:
        return "Wear a jacket"
    elif 10 < temp <= 20:
        return "Wear a sweater"
    else:
        return "Wear light clothes"

if __name__ == "__main__":
    app.run(debug=True)
