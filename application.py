from flask import Flask, render_template, url_for, jsonify, request
import translate, sentiment, synthesize

application = Flask(__name__)
application.config['JSON_AS_ASCII'] = False


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/translate-text', methods=['POST'])
def translate_text():
    # I am using the request object to call the get.json() to be able to store the data posted in the
    # http request as a JSON Object
    data = request.get_json()
    print(data)
    # Creating a variable to store the value of 'text' from the JSON object stored in the data variable.
    text_input = data['text']
    # Creating a variable to store the value of 'to' from the JSON object stored in the data variable.
    translation_output = data['to']
    # I am calling the get_translation function in translate.py which is then going to call the
    # Cognitive service api with the parameters and storing the response in response variable.
    response = translate.get_translation(text_input, translation_output)
    # We are returning the data we get as JSON to display on our website
    return jsonify(response)


@application.route('/sentiment-analysis', methods=['POST'])
def sentiment_analysis():
    data = request.get_json()
    print(data)
    input_text = data['inputText']
    input_lang = data['inputLanguage']
    response = sentiment.get_sentiment(input_text, input_lang)
    return jsonify(response)


@application.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    print(data)
    text_input = data['text']
    voice_font = data['voice']
    tts = synthesize.TextToSpeech(text_input, voice_font)
    tts.get_token()
    audio_response = tts.save_audio()
    return audio_response


if __name__ == "__main__":
    application.run(debug=True)
