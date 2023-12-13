from fastapi import FastAPI,Body
from pydantic import BaseModel
import uvicorn
from fuzzywuzzy import fuzz
import sqlite3
from base_db import*
import datetime

app = FastAPI()


class Request_Item(BaseModel):
    tree_id: str
    question: str

def from_database(tree_id, question):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    core_data=core_tab(question)
    if core_data:
        return core_data
    elif core_data==False:
        query = "SELECT question FROM user WHERE tree_id=?"
        cursor.execute(query,(tree_id,))
        questions = cursor.fetchall()
        for i in questions:
            match_rate=fuzz.ratio(i[0],question)
            if match_rate>85:
                #print(match_rate)
                quy="SELECT answer FROM user WHERE tree_id=? AND question=?"
                cursor.execute(quy,(tree_id,i[0],))
                answer=cursor.fetchone()
                #print(answer[0])
                conn.close()
                return answer[0]
                
                
def time_teller(question):
    if "time" in question:
        timE=datetime.datetime.now()
        return timE.strftime('time is %H:%M and date is %B-%D')
    
def player_vid(question):
    if "play" in question:
        return "playing"  
@app.get("/")
async def read_root():
    return {"Hello": "World"} 
@app.post("/process")
async def process(RawData :Request_Item=Body(...)):
    print(RawData.tree_id)
    print(RawData.question)
    processedData = from_database(tree_id = RawData.tree_id,question=RawData.question)
    if processedData:
        sendData = {
        "Response":f"{processedData}"
        }
        return sendData
    processedData = time_teller(RawData.question)
    if processedData:
        print(processedData)
        sendData = {
        "Response":f"{processedData}"
        }
        return sendData
    


if __name__ == "__main__":
    uvicorn.run(app)
