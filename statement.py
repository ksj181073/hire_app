from vessel_info import Company
from datetime import datetime
import json
import copy

class HireStatement:
    def __init__(self, hire_date=datetime.now(), location="", on_hire="on", charterer="", project="", mgo=0.0, lo=0, fw=0.0) -> None:
        self.on_hire = on_hire
        self.date = hire_date
        self.location = location
        self.charterer = Company(name=charterer)
        self.project = project
        self.mgo = mgo
        self.lo = lo
        self.fw = fw
    
    def toJSON(self):
        hire_cc = copy.deepcopy(self)
        hire_cc.date = self.DateToInt()
        
        return json.dumps(hire_cc, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)
    
    def fromJSON(self, json_string=""):
        self.__dict__ = json.loads(json_string)
        self.IntToDate(self.date)

        self.charterer = Company(name=self.__dict__['charterer']['name'])
    
    def DateToInt(self):
        return self.date.strftime("%Y%m%d%H%M")
    
    def IntToDate(self, dateString="200001010101"):
        self.date = datetime(year=int(dateString[:4]), month=int(dateString[4:6]), day=int(dateString[6:8]), hour=int(dateString[8:10]), minute=int(dateString[10:12]))
