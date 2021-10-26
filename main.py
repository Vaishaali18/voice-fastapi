from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from fastapi import FastAPI, Query, Path,Request, Form
'''from ner_model import check_name_entity_recognition, POS,check_name_entity_recognition_pdf'''
from pdf_mail import sendpdf
import json 
import en_core_med7_trf
from datetime import datetime
from app import *

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:8000/data",
    "http://localhost:3000/prescribe"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)	



class Payload(BaseModel):
    data: str = ""

class Details(BaseModel):
    email : str
    dirpath : str
    pateintID : str


@app.get('/')
def demo():
    return {"message":"working"}

@app.post('/pdf')
async def createPdf(payload: Payload):
    '''pred = await check_name_entity_recognition_pdf(payload.data)'''
    med7 = en_core_med7_trf.load()
    doc = med7(payload.data)
    pred = [[ent.text, ent.label_] for ent in doc.ents]
    text = payload.data
    text.lower()
    sentences = text.split("next")
    print(sentences)
    data = []
    line = 0 
    entities = {"DRUG" : "NA" , "DURATION" : "NA" , "STRENGTH" : "NA" , "ROUTE" : "NA" , "FORM" : "NA" , "DOSAGE" : "NA" , "FREQUENCY" : "NA"}
    for pre in range(len(pred)):   
        if(pred[pre][0] in sentences[line]):
            entities[pred[pre][1]] = pred[pre][0]
        else:
            data.append(entities)
            entities = {"DRUG" : "NA" , "DURATION" : "NA" , "STRENGTH" : "NA" , "ROUTE" : "NA" , "FORM" : "NA" , "DOSAGE" : "NA" , "FREQUENCY" : "NA"}
            entities[pred[pre][1]] = pred[pre][0]
            line += 1
    data.append(entities)
    print(data)
    return data
    # data= {"item" : out }
    # data=json.dumps(data)
    # data = data.encode("utf-8")
  
    # return data;
    
    '''sent=payload.data;
    wordsList=sent.split();
    predsList = [j for sub in pred for j in sub]
    print(predsList )
    words=[]
    preds=[]

    for i in range(len(predsList)):
        if(predsList[i]!="O"):
            preds.append(predsList[i])
            words.append(wordsList[i])      
    start=0
    inputs=[]
    predictions=[]
    for current in range(len(words)):
        if(preds[current][0]=="B"):
            predictions.append(preds[current])
            inputs.append(" ".join(words[start:current]))
            start=current

    inputs.append(" ".join(words[start:]))
    inputs=inputs[1:]
    tempCounts={"I-PER":0,"B-PER":0,"I-MISC":0,"B-MISC":0,"I-LOC":0,"B-LOC":0,"B-ORG":0,"I-ORG":0}
    for i in predictions:
        tempCounts[i]+=1
        totalDrug=max(tempCounts.values())
    data=[]
    for i in range(totalDrug):
        data.append({"I-PER":"NA","B-PER":"NA","I-MISC":"NA","B-MISC":"NA","I-LOC":"NA","B-LOC":"NA","B-ORG":"NA","I-ORG":"NA"})
    counts={"I-PER":0,"B-PER":0,"I-MISC":0,"B-MISC":0,"I-LOC":0,"B-LOC":0,"B-ORG":0,"I-ORG":0}
    for i in range(len(predictions)):
        temp=counts[predictions[i]]
        data[temp][predictions[i]]=inputs[i]
        counts[predictions[i]]+=1
    # data= {"item" : data}
    # data=json.dumps(data)
    # data = data.encode("utf-8")
    print("data((")
    print(data)
    return data'''


@app.post('/data')
async def main(payload: Payload):
    print(payload)
    '''out = await check_name_entity_recognition(payload.data)'''
    med7 = en_core_med7_trf.load()
    doc = med7(payload.data)
    final_dict = []
    for ent in doc.ents:
        dict1={'data': ent.text,'label': ent.label_}
        final_dict.append(dict1)
    data= {"item" : final_dict }
    data=json.dumps(data)
    data = data.encode("utf-8")
    print(payload)
    return data;

@app.post('/sendpdf')
async def send(details : Details):
    print(details)
    print("hi")
    sender_email_address = "vaishaali18@gmail.com"
    receiver_email_address = details.email
    sender_email_password = "kklv7000"
    subject_of_email = "Prescription"
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    body_of_email = "Below is your prescription for visiting the hospital in : "+ dt_string
    filename = "Prescription" + details.pateintID      
    location_of_file = details.dirpath
    k = sendpdf(sender_email_address, 
            receiver_email_address,
            sender_email_password,
            subject_of_email,
            body_of_email,
            filename,
            location_of_file)
  
    k.email_send()  
    return "success"


"""
class User(BaseModel):
    Input: str

@app.post('/data')#,response_class=HTMLResponse)
async def main(text: User):
    out = await check_name_entity_recognition(text.Input)
    return out;

"""
