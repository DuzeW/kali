from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from deep_translator import GoogleTranslator
from crew import TravelingCrew

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def home():
    return render_template('survey.html')


@app.route('/submit_survey', methods=['POST'])
def submit_survey():
    data = request.json
    city = data.get("city")
    preferred_language = data.get("preferred_language")

    # Tłumaczenie nazwy miasta na angielski
    translator = GoogleTranslator(source='pl', target='en')
    translated_city = translator.translate(city)

    inputs = {
        "city": translated_city,
        "preferred_language": preferred_language,
        "budget": data.get("budget"),
        "preferred_transportation": data.get("preferred_transportation"),
        "point_of_interest": data.get("point_of_interest"),
        "preferred_accommodation": data.get("preferred_accommodation"),
        "departure_date": data.get("departure_date")
    }

    response = TravelingCrew().crew().kickoff(inputs=inputs)

    print("Response object:", response)
    print("Response dict:", response.__dict__)

    # Konwersja CrewOutput na słownik na podstawie dostępnych atrybutów
    response_dict = {
        "weather": response.raw.split('\n\n')[0],
        "attractions": response.raw.split('\n\n')[1],
        "accommodation": response.raw.split('\n\n')[2],
        "transport": response.raw.split('\n\n')[3]
    }

    return jsonify(response_dict)


if __name__ == '__main__':
    app.run(debug=True)
