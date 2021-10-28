from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from fastapi import FastAPI, Query, Path,Request, Form
from pdf_mail import sendpdf
import json 
import en_core_med7_trf
from datetime import datetime
import spacy


app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
 

@app.post('/data')
async def classify(payload: Payload):
    print(payload)
    med7 = en_core_med7_trf.load()
    print("hello")
    doc = med7(payload.data)
    final_dict = []
    print("got")
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



