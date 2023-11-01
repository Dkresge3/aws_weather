from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendation = None
    additional_promt = None
    if request.method == 'POST':
        temp = float(request.form['temperature'])
        recommendation = get_clothing_recommendation(temp)
        additional_promt = request.form.get('text')
    return render_template('index.html', recommendation=recommendation)

def get_clothing_recommendation(temp):
    if temp < 0:
        return "Wear a heavy winter coat, gloves, hat, and scarf!"
    elif temp < 10:
        return "Wear a winter coat and a hat!"
    elif temp < 20:
        return "Wear a light jacket or sweater!"
    else:
        return "It's warm! Just a T-shirt will do."

if __name__ == "__main__":
    app.run(debug=True)
