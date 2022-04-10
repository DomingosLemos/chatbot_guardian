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
statusBot = {"status":"", "url":"", "param_name":"", "param_value":"", "param_type":""} # "" = normal; "wait_param" = aguarga input para API
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

def getEntity(api_param_type, msg, entity_name, list_of_entities):
    #api_param_type: 
    #   proper noun (nome próprio: João, Lisboa, CCB)
    #   verb (verbo: estar, ficar)
    #   pronoun (pronome: eu, eles, aqueles, minha, meu, sua)
    #   adverb (advérbios: amanhã, agora, sempre, ali, assim)
    #   adjective (adjetivo: bonito, agradável )
    #   pontuation (pontuação: ?, !)
    # caso o valor seja "entity" estamos a trabalhar com uma entidade e neste caso é necessário saber qual que é dado pelo argumento api_param_name

    if (api_param_type == 'entity'):
        #tem que trabalhar a desambiguação de entidade
        for doc in list_of_entities:
            if doc['name'] == entity_name:
                #encontrada a entidade
                list_of_entities_values = doc['values']
                for entity_value in list_of_entities_values:
                    #para os possíveis valores da entidade
                    for entity_synonym in list_of_entities_values[entity_value]:
                        #tem em conta a lista de sinónimos (o valor tem que constar na lista de sinonimos) 
                        if entity_synonym in msg:
                            if debug:
                                print('function: getEntity(1) | api_param_type: ', api_param_type, ' | entity_name: ', entity_name, ' | entity_value: ', entity_value, ' | resultado: encontrado um sinónimo para a entidade') 
                            return entity_value

    else:
        doc = nlp(msg)
        if debug:
            print('function: getEntity(2) | doc: ', doc, ' | resultado: procurar se existe o tipo de entidade na frase')
        for token in doc:
            if debug:
                print('function: getEntity(3) | api_param_type: ', api_param_type, ' | tag: ', token.tag_, ' | explain: ', spacy.explain(token.tag_), ' | entidade: ', token.text) 

            if (spacy.explain(token.tag_) == api_param_type):
                if debug:
                    print('function: getEntity(4) | api_param_type: ', api_param_type, ' | entidade encontrada: ', token.text, ' | resultado: encontrado o tipo de entidade na frase')
                return token.text
    
    if debug:
        print('function: getEntity(5) | api_param_type: ', api_param_type, ' | entity_name: ', entity_name, ' | msg: ', msg, ' | resultado: entidade não encontrada') 
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
        print ('function: getResponse(0) | statusBot: ', statusBot)
        print ('function: getResponse(0) | ints: ', ints)
    if (len(ints)==0 and statusBot['status'] == ""):
        result = "Não  entendi. Pode reformular a pergunta?"
    elif (statusBot['status'] == "wait_param"):
        #recebi resposta para a minha API (falta de entidade)
        if (statusBot['param_name'] != ""):
            #se for uma desambiguação é necessário obter o valor master, caso contrário é a própria mensagem da resposta do user que é passada à API
            if (statusBot['param_type'] == 'entity'):
                list_of_entities = intents_json['entities']
                element = str(getEntity(statusBot['param_type'], msg, statusBot['param_name'], list_of_entities))
            else:
                element = msg
            if debug:
                print ('function: getResponse(1) | element: ', element, ' | statusBot: ', statusBot, ' | resultado: elemento encontrado e passado à API')
            response = callAPI(statusBot['url'], statusBot['param_name'], element)
        else:
            response = callAPI(statusBot['url'])
        result =  response 
        if debug:
            print ('function: getResponse(2) | Recolha da entidade em falta | resposta: ', response, ' | resultado: resposta da API' )

        statusBot = {"status":"", "url":"", "param_name":"", "param_value":"", "param_type":""} # limpa tudo
    else:
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        list_of_entities = intents_json['entities']
        for i in list_of_intents:
            # encontrou a intent desejada
            if(i['tag']== tag):
                # verifica se existe uma API que trata da intent             
                if(i['api_action'] != ""):
                    response=""
                    if (i['api_param_type'] != ""):
                        element = str(getEntity(i['api_param_type'], msg, i['api_param_name'], list_of_entities))

                        #verifica se existe o elemento procurado
                        if (element == ""):
                            response = random.choice(i['api_responses_missing_param'])
                            statusBot = {"status": "wait_param", "url": i['api_action'], "param_name": i['api_param_name'], "param_value": element, "param_type": i['api_param_type']}
                            if debug:
                                print ('function: getResponse(3) | resposta API: ', response + ' | intent: ' + ints[0]['intent'] + ' | probability: ' + ints[0]['probability'] + ' | threshould: ' + ints[0]['threshould'], ' | resultado: entidade não encontrada. Prompt enviado para identificar entidade')
                        else:
                            response = callAPI(i['api_action'], i['api_param_name'], element)
                            statusBot = {"status": "", "url": i['api_action'], "param_name": i['api_param_name'], "param_value": element, "param_type": i['api_param_type']}
                            if debug:
                                print ('function: getResponse(4) | resposta API: ', response + ' | intent: ' + ints[0]['intent'] + ' | probability: ' + ints[0]['probability'] + ' | threshould: ' + ints[0]['threshould'], ' | resultado: chamada API com identificação imediata da entidade')
                    else:
                        response = callAPI(i['api_action'])
                        if debug:
                            print ('function: getResponse(5) | resposta API: ', response + ' | intent: ' + ints[0]['intent'] + ' | probability: ' + ints[0]['probability'] + ' | threshould: ' + ints[0]['threshould'], ' | resultado: chamada API sem necessidade de identificação da entidade')

                    result = response

                else:
                    result = random.choice(i['responses'])
                    if debug:
                        print ('function: getResponse(6) | resposta: ', random.choice(i['responses']) + ' | intent: ' + ints[0]['intent'] + ' | probability: ' + ints[0]['probability'] + ' | threshould: ' + ints[0]['threshould'], ' | resultado: devolve uma das respostas aliatórias')
                break 
            else:
                result = "Não entendi. Pode reformular a pergunta?"
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    if debug:
        print('-------------------------------------------------------------------')
        print('function: chatbot_response | msg: ', msg)
    res = getResponse(ints, intents, msg)
    if debug:
        print('function: chatbot_response | resposta: ', res)
        print('-------------------------------------------------------------------')
    return res
