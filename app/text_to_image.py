from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from google_images_search import GoogleImagesSearch
import re
import speech_recognition as sr
import json
from secrets import GOOGLE_CLOUD_SPEECH_CREDENTIALS, developer_key, custom_search_cx
import io

def tts():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source, phrase_time_limit=4)
        print('file format', type(audio))

    # recognize speech using Google Cloud Speech
    try:
        response = r.recognize_google_cloud(audio, credentials_json=json.dumps(GOOGLE_CLOUD_SPEECH_CREDENTIALS))
        print('Response ', response)
        return response
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))

def blob_to_text(blob):
    try:
        r = sr.Recognizer()
        open("backend.wav",'wb').write(blob)
        file_obj = io.BytesIO()  # create file-object
        file_obj.write(blob) # write in file-object
        file_obj.seek(0) # move to beginning so it will read from beginning

        mic = sr.AudioFile('backend.wav') # use file-object
        with mic as source:
            audio = r.record(source)

        result = r.recognize_google(audio_data=audio, language="en-US")
        return result
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))

def get_urls(searches):
    gis = GoogleImagesSearch(developer_key, custom_search_cx, validate_images=False)
    # define search params:
    search_params = {'num': 1, 'safe': 'off'}
    urls = []

    for search in searches:
        search_params['q'] = search
        gis.search(search_params)
        [urls.append(result.url) for result in gis.results()]
    return urls

def purge(string):  
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(string) 
    return [w for w in word_tokens if w not in stop_words and w.isalnum()] 

def text_to_image():
    string = tts()
    purged_string = purge(string)
    urls = get_urls(purged_string)

    return urls

def blob_to_image(audio):
    string = blob_to_text(audio)
    purged_string = purge(string)
    urls = get_urls(purged_string)

    return urls

if __name__ == "__main__":
    urls = text_to_image()
    print(urls)