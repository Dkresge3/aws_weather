from flask import Flask, request, render_template_string
from getClothes import getClothes
from getData import get_current_weather

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        location = request.form.get('location')
        clothes = printme(location)

        return render_template_string('''
            <h1 style="width: 100%; text-align: center;">Weather Wear</h1>
            <form method="post">
                Location: <input type="text" name="location" placeholder="{{ location_value }}">
                <input type="submit" value="Submit">
            </form>
            <p>You are currently looking at {{ location_value }}</p> <br/>
            <p>{{ clothes_value }}</p>
            Location received and printed to console!
        ''', location_value=location, clothes_value=clothes) 

    return render_template_string('''
        <h1 style="width: 100%; text-align: center;">Weather Wear</h1>
        <form method="post">
            Location: <input type="text" name="location">
            <input type="submit" value="Submit">
        </form>
    ''')

def printme(location):
    print(f"Location is: {location}")
    getMsg=get_current_weather(location)
    print(getMsg)
    getResults=getClothes(getMsg)
    print(getResults)
    location=getResults
    return getResults


if __name__ == '__main__':
    app.run(debug=True, port=8501)
