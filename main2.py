from this import d
import sportsbetting
from sportsbetting.user_functions import *

import pickle
import pandas as pd
from datetime import datetime
import time
import sys
import keyboard
import numpy as np
import glob


def download_csv(data,sport,live,now):
    list_file =  glob.glob("CSV/*")
    # print(data)
    for i in data["betclic"]:
        file = [j for j in list_file if (sport+"__"+str(i).replace(" - ","__").replace(" ","_").replace("/","__") +"__"+data["betclic"][i]["date"].strftime("%Y_%m_%d_%H_%M")) in j]
        if len(file) != 0:
            # print("INISIALISATION FILE ==> "+"\"CSV/"+sport+"__"+str(i).replace(" - ","__").replace(" ","_").replace("/","__") +"__"+data["betclic"][i]["date"].strftime("%Y_%m_%d_%H_%M")+".csv\"")
            Update_csv(i,data,sport,live,now)
        else:
            # print("pas de file!!!!!!!!!!!!!!!!!!!!")
            created_new_csv(i,now,live,data,sport)
       
def Update_csv(i,data,sport,live,now):
    df = pd.read_csv("CSV/"+sport+"__"+str(i).replace(" - ","__").replace(" ","_").replace("/","__") +"__"+data["betclic"][i]["date"].strftime("%Y_%m_%d_%H_%M")+".csv")
    new_row = {'Date':now,'Live':live,'Win':data["betclic"][i]["odds"]["betclic"][0],'Lose':data["betclic"][i]["odds"]["betclic"][1]}
    new_df = pd.DataFrame(new_row, index=[0])
    # print(type(new_df),type(df))
    df = pd.concat([df,new_df], ignore_index=True)
    del df["Unnamed: 0"]
    df.to_csv("CSV/"+sport+"__"+str(i).replace(" - ","__").replace(" ","_").replace("/","__") +"__"+data["betclic"][i]["date"].strftime("%Y_%m_%d_%H_%M")+".csv")

def created_new_csv(i,now,live,data,sport):
    betclic = []
    try :
        betclic.append([now, live,data["betclic"][i]["odds"]["betclic"][0],data["betclic"][i]["odds"]["betclic"][1]])
    except:
        betclic.append([now,live,0,0])
    
    df = pd.DataFrame(data=betclic,columns = ["Date","Live","Win","Lose"])
    print("INISIALISATION FILE ==> "+"\"CSV/"+sport+"__"+str(i).replace(" - ","__").replace(" ","_").replace("/","__") +"__"+data["betclic"][i]["date"].strftime("%Y_%m_%d_%H_%M")+".csv\"",end="  ")
    try:
        try:
            del df["Unnamed: 0"]
        except:
            pass
        df.to_csv("CSV/"+sport+"__"+str(i).replace(" - ","__").replace(" ","_").replace("/","__") +"__"+data["betclic"][i]["date"].strftime("%Y_%m_%d_%H_%M")+".csv")
        print("\033[92m {}V \x1b[0m".format(" "*(125-len("INISIALISATION FILE ==> "+"\"CSV/"+sport+"__"+str(i).replace(" - ","__").replace(" ","_").replace("/","__") +"__"+data["betclic"][i]["date"].strftime("%Y_%m_%d_%H_%M")+".csv\""))))
    except:
        print("\033[91m {}X \x1b[0m".format(" "*(125-len("INISIALISATION FILE ==> "+"\"CSV/"+sport+"__"+str(i).replace(" - ","__").replace(" ","_").replace("/","__") +"__"+data["betclic"][i]["date"].strftime("%Y_%m_%d_%H_%M")+".csv\""))))
        sys.exit(0)

def Betclic_data(sport="tennis",now=""):  
    if sport not in ["tennis"]:
        print("Sport variable in Betclic_data not good, normally choose \"tennis\"")
    for live in [True,False]:
        data = parse_competition("Tout le "+sport, sport,live, "betclic")#, "winamax","unibet")
        download_csv(data,sport,live,now)

def pause(tps):
    for i in np.arange(0,tps,0.1):
        if keyboard.is_pressed('q'):
            print("\nyou pressed q, so exiting...")
            sys.exit(0)
        time.sleep(0.1)


if __name__ == "__main__":
    i=0
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            Betclic_data(sport = "tennis",now=now) 
            print("\u001b[33;1m {} secondes execute\033[00m".format(i*10))
        except:     
            print("\033[91mERROR \x1b[0m")
        pause(10)
        i=i+1