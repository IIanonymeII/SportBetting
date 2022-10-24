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
#import json

def Betclic_data(sport="tennis",type ="win",now="",live=False):

    if type not in ["win","lose"]:
        print("type variable in Betclic_data not good, normally choose \"win\" or \"lose\"")
    elif type == "win":
        type_num = 0
    else:
        type_num = 1

    if sport not in ["tennis"]:
        print("Sport variable in Betclic_data not good, normally choose \"tennis\"")

    if live:
        name_live="Live"
    else:
        name_live="Future"

    data = parse_competition("Tout le "+sport, sport,live, "betclic")#, "winamax","unibet")
    # print(data["betclic"])
    # # print(type(json_object))

    # with open('data.json', 'wb') as fp:
    #     pickle.dump(json_object, fp)

    # with open('data.json', 'rb') as fp:
    #     data = pickle.load(fp)

    betclic = []
    try:
        df = pd.read_csv("CSV/"+name_live+"__"+sport+"_betclic_"+type+".csv")
        index_change = []
        betclic = [0] *len(df)
        for i in data["betclic"]:
            if ((i in str(df.Match)) and ( str(data["betclic"][i]["date"] in df.Date ))):
                # print(i,str(data["betclic"][i]["date"]))
                ind = df[(df.Match == i) & (df.Date == str(data["betclic"][i]["date"]))]
                if int(ind.index.size) >0:
                    index_change.append([ind.index.values[0],(ind["Match"].to_string(index=False))])
            else:
                betclic = betclic+[data["betclic"][i]["odds"]["betclic"][type_num]]
                # print([data["betclic"][i]["date"],i]+[0]*(len(df)-2))
                
                df.loc[len(df.index)] = [len(df.index),data["betclic"][i]["date"],i]+[0]*(len(df.columns)-3)

        
        for i in index_change:
            try :
                betclic[i[0]] = (data["betclic"][i[1]]["odds"]["betclic"][type_num])
            except:
                pass
        #now = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        df[now] = betclic
        try:
            del df['Unnamed: 0']
        except:
            pass
        df['Date'] = pd.to_datetime(df['Date'], format=('%d-%m-%Y_%H:%M:%S'))
        df = df.sort_values(by='Date')
        df.to_csv("CSV/"+name_live+"__"+sport+"_betclic_"+type+".csv")

    except:
        print("INISIALISATION FILE ==>"+"CSV/"+name_live+"__"+sport+"_betclic_"+type+".csv")
        for i in data["betclic"]:
            # print(data[i],"\n\n")
            try :
                betclic.append([data["betclic"][i]["date"],i,data["betclic"][i]["odds"]["betclic"][type_num]])
            except:
                betclic.append([data["betclic"][i]["date"],i,0])


        #now = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        # print(type(date_now))
        df = pd.DataFrame(data=betclic,columns = ["Date","Match",now])
        try:
            del df["Unnamed: 0"]
        except:
            pass
        df['Date'] = pd.to_datetime(df['Date'], format=('%d-%m-%Y_%H:%M:%S'))
        df = df.sort_values(by='Date')


        df.to_csv("CSV/"+name_live+"__"+sport+"_betclic_"+type+".csv")
        # print(df)




def pause(tps):
    for i in np.arange(0,tps,0.1):
        if keyboard.is_pressed('q'):
            print("\nyou pressed q, so exiting...")
            sys.exit(0)
        time.sleep(0.1)




if __name__ == "__main__":
    i = 0
    while True:
        
        now = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        if i%60==0:
            Betclic_data(sport = "tennis", type = "win",now=now,live=False)
            Betclic_data(sport = "tennis", type = "lose",now=now,live=False)
        Betclic_data(sport = "tennis", type = "win",now=now,live=True)
        Betclic_data(sport = "tennis", type = "lose",now=now,live=True)
        print("\033[96m {} secondes execute\033[00m".format(i*10))
        pause(10)
        i=i+1

    
