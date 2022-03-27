import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
import requests
import spacy

intents = json.loads(open('job_intents.json', encoding='utf-8').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
nlp = spacy.load('pt_core_news_md') #modelo da lingua portuguêsa
statusBot = {"status":"", "url":"", "param_name":"", "param_value":""} # "" = normal; "way_param" = aguarga input para API
debug = True

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    #short sentence
    if (len(sentence)< 10):
        ERROR_THRESHOLD = 0.80
    else:
        ERROR_THRESHOLD = 0.25

    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1]), "threshould": str(ERROR_THRESHOLD)})
    return return_list

def getEntity(api_param_type, msg):
    #api_param_type: 
    #   proper noun (nome próprio: João, Lisboa, CCB)
    #   verb (verbo: estar, ficar)
    #   pronoun (pronome: eu, eles, aqueles, minha, meu, sua)
    #   adverb (advérbios: amanhã, agora, sempre, ali, assim)
    #   adjective (adjetivo: bonito, agradável )
    #   pontuation (pontuação: ?, !)

    doc = nlp(msg)
    print("doc: ", doc)
    for token in doc:
        if debug:
            print('function: getEntity | type: ', api_param_type, ' | tag: ', token.tag_, ' | explain: ', spacy.explain(token.tag_), ' | entidade: ', token.text) 

        if (spacy.explain(token.tag_) == api_param_type):
            return token.text
    
    if debug:
        print('function: getEntity | type: ', api_param_type, ' | texto: ', msg, ' | resultado: entidade não encontrada') 
    return ""

def callAPI(url, param_name="", param_value=""):
    if param_name != "":
        param = {param_name:param_value}
        response = requests.get(url, params=param)
    else:
        response = requests.get(url)

    return response.text

def getResponse(ints, intents_json, msg):
    global statusBot

    if debug:
        print ("statusBot: ", statusBot)
        print ("ints: ", ints)
    if (len(ints)==0 and statusBot['status'] == ""):
        result = "Não  entendi. Pode reformular a pergunta?"
    elif (statusBot['status'] == "way_param"):
        #recebi resposta para a minha API (falta de entidade)
        if (statusBot['param_name'] != ""):
            response = callAPI(statusBot['url'], statusBot['param_name'], msg)
        else:
            response = callAPI(statusBot['url'])
        result =  response 
        if debug:
            print ('function: getResponse(0) | Recolha da entidade em falta | resposta: ', response )

        statusBot = {"status":"", "url":"", "param_name":"", "param_value":""} # limpa tudo
    else:
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            # encontrou a intent desejada
            if(i['tag']== tag):
                # verifica se existe uma API que trata da intent             
                if(i['api_action'] != ""):
                    response=""
                    if (i['api_param_type'] != ""):
                        element = str(getEntity(i['api_param_type'], msg))

                        #verifica se existe o elemento procurado
                        if (element == ""):
                            response = random.choice(i['api_responses_missing_param'])
                            statusBot = {"status": "way_param", "url": i['api_action'], "param_name": i['api_param_name'], "param_value": element}
                        else:
                            response = callAPI(i['api_action'], i['api_param_name'], element)
                    else:
                        response = callAPI(i['api_action'])

                    result = response
                    if debug:
                        print ('function: getResponse(1) | resposta API: ', response + ' | intent: ' + ints[0]['intent'] + ' | probability: ' + ints[0]['probability'] + ' | call API | threshould: ' + ints[0]['threshould'])
                else:
                    result = random.choice(i['responses'])
                    if debug:
                        print ('function: getResponse(2) | resposta: ', random.choice(i['responses']) + ' | intent: ' + ints[0]['intent'] + ' | probability: ' + ints[0]['probability'] + ' | threshould: ' + ints[0]['threshould'])
                break 
            else:
                result = "Não entendi. Pode reformular a pergunta?"
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents, msg)
    return res
