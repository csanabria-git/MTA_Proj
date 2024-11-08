import os
from datetime import datetime
from flask import Flask, render_template, request
import sys
from subprocess import Popen, PIPE
import requests
import json
from dateutil.parser import parse
from datetime import datetime
from datetime import timedelta
from flask import Flask
import time

############################################################# Dicts################################################################################################
#Since I would need to run the same 6 commands for 36st station trains and they remain constsnat this line is to put all the commands into a dict
CommandDict={1:"underground stops N --api-key Yes7tAol8sKfqd1cGfF26W1C2nWTFiZ1mM8Z5uG8 | grep R01S",
             2:"underground stops W --api-key Yes7tAol8sKfqd1cGfF26W1C2nWTFiZ1mM8Z5uG8 | grep R01S",
             }
#This dict takes all the text from the commands and actually runs them in terminal and this is what sends back the train station ID + all the times i.e R36N 12:17 12:26 12:37 12:43 12:52 12:58 13:08 13:17 13:23 13:32
TrainTimesDict = {1:os.popen("underground stops N --api-key Yes7tAol8sKfqd1cGfF26W1C2nWTFiZ1mM8Z5uG8 | grep R36N").read(),
                  2:os.popen("underground stops N --api-key Yes7tAol8sKfqd1cGfF26W1C2nWTFiZ1mM8Z5uG8 | grep R36S").read(),      
                   }
MasterDict = {1:[],2:[],3:[],4:[],5:[],6:[]}
NTrainDict = {1:[],2:[]}
WTrainDict = {1:[],2:[]}

############################################################# Functions################################################################################################
def ParseTrainAndDestination(CommandDict,TrainTimesDict):
    #parse Train and destination from CLI command that calls from the MTA API
    currenttime = datetime.now()
    if "stops N" in CommandDict:
        train = 'N'
        destination = "CONEY ISLAND-STILLWELL"
    if "stops W" in CommandDict:
        train = 'W'
        destination = "WHITEHALL"
    #Put train times output into a variable of type string then remove spaces so its easier to parse
    TrainTimes=TrainTimesDict
    TrainTimes=TrainTimes.replace(" ", "")

    # Parse arrival1 and 2 from TrainTimes string
    arrival1=TrainTimes[4:9]
    arrival2=TrainTimes[9:14]
    arrival1 = parse(arrival1)
    arrival2 = parse(arrival2)
    arrival1 = int(timedelta.total_seconds(arrival1-currenttime) /60)
    arrival2 = int(timedelta.total_seconds(arrival2-currenttime) /60)

    TrainDict={"Train":train,
               "Dst":destination,
               "Train1":arrival1,
               "Train2":arrival2
               }
    return TrainDict

#app = Flask(__name__)
#@app.route('/')
#def my_route():
#    return render_template('index.html', NTrains=NTrainDict, WTrains=WTrainDict)



