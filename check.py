import pandas as pd
import numpy as np
import math

def oyunbitir(id):
    df = pd.read_csv('aktiv_oyunlar.csv')
    idx = df.index[df['chat_id'] == id].tolist()
    try:
        df = df.drop(idx[0])
    except:
        pass
    df.to_csv('aktiv_oyunlar.csv', index=False)

def add_aktiv(id):
    df = pd.read_csv('aktiv_oyunlar.csv')
    idx = df.index[df['chat_id'] == id].tolist()
    try:
        df = df.drop(idx[0])
    except:
        pass
    dict = {
        'chat_id': [id],
        'sualkec': [0],
        'aktiv' : [1],
        'cavab': [0],
        'sual_nomresi':[0],
        'fasile': [0],
        'fasile_vaxt':[0]
    }
    add = pd.DataFrame(dict)
    df = pd.concat([df, add], ignore_index=True)
    df.to_csv('aktiv_oyunlar.csv', index=False)

def quiz_aktivlik(id):
    df = pd.read_csv('aktiv_oyunlar.csv')
    try:
        st=int(df.loc[df['chat_id']==id]['aktiv'])
    except:
        return 2
    if(st==1):
        return 1
    else:
        return 0

def sual_aktivlik(id):
    df = pd.read_csv('aktiv_oyunlar.csv')
    st=int(df.loc[df['chat_id']==id]['sualkec'])
    if (st ==1):
        return 1
    else:
        return 0

def sualkec(id,status):
    df = pd.read_csv('aktiv_oyunlar.csv')
    try:
        idx = df.index[df['chat_id'] == id].tolist()
        df.loc[idx[0],'sualkec']=status
        df.to_csv('aktiv_oyunlar.csv', index=False)
    except:
        pass

def dayan(id):
    df = pd.read_csv('aktiv_oyunlar.csv')
    try:
        idx = df.index[df['chat_id'] == id].tolist()
        df.loc[idx[0], 'aktiv'] = 0
        df.loc[idx[0], 'sualkec'] = 1
        df.loc[idx[0], 'fasile'] = 0
        df.to_csv('aktiv_oyunlar.csv', index=False)
    except:
        pass

def cavab_add(id,cavab,sual_nomre):
    df = pd.read_csv('aktiv_oyunlar.csv')
    idx = df.index[df['chat_id'] == id].tolist()
    df.loc[idx[0], 'cavab'] = cavab
    df.loc[idx[0], 'sual_nomresi'] = sual_nomre
    df.to_csv('aktiv_oyunlar.csv', index=False)

def cavab_yoxla(id,versiya):
    df = pd.read_csv('aktiv_oyunlar.csv')
    try:
        idx = df.index[df['chat_id'] == id].tolist()
        if  versiya.lower() == (df.loc[idx[0], 'cavab'].lower()):
            idx = df.index[df['chat_id'] == id].tolist()
            df.loc[idx[0], 'sualkec'] = 1
            df.to_csv('aktiv_oyunlar.csv', index=False)
            return 1
        else:
            # print('duz deyil')
            return 0
    except:
        pass

def fasile_yoxla(id):
    df = pd.read_csv('aktiv_oyunlar.csv')
    try:
        st=int(df.loc[df['chat_id']==id]['fasile'])
    except:
        return 0
    if(st==1):
        return 1
    else:
        return 0

def fasile_ver(id,vaxt=30):
    df = pd.read_csv('aktiv_oyunlar.csv')
    idx = df.index[df['chat_id'] == id].tolist()
    df.loc[idx[0], 'fasile'] = 1
    df.loc[idx[0], 'sualkec'] = 1
    df.loc[idx[0], 'fasile_vaxt'] += vaxt
    df.to_csv('aktiv_oyunlar.csv', index=False)

def fasile_geri_sayim(id):
    df = pd.read_csv('aktiv_oyunlar.csv')
    idx = df.index[df['chat_id'] == id].tolist()
    if(df.loc[idx[0], 'fasile_vaxt'] == 0):
        df.loc[idx[0], 'fasile'] = 0
    df.loc[idx[0], 'fasile_vaxt'] -= 1
    # print(df.loc[idx[0], 'fasile_vaxt'],"chat_id: "+str(id))
    df.to_csv('aktiv_oyunlar.csv', index=False)

def fasile_vaxti(id):
    df = pd.read_csv('aktiv_oyunlar.csv')
    try:
        st=int(df.loc[df['chat_id']==id]['fasile_vaxt'])
        return st
    except:
        pass

def davam(id):
    df = pd.read_csv('aktiv_oyunlar.csv')
    idx = df.index[df['chat_id'] == id].tolist()
    df.loc[idx[0], 'fasile'] = 0
    df.loc[idx[0], 'fasile_vaxt'] = 0
    df.loc[idx[0], 'sualkec'] = 0
    df.to_csv('aktiv_oyunlar.csv', index=False)

def sikayet_sual_nomresi(id):
    df = pd.read_csv('aktiv_oyunlar.csv')
    idx = df.index[df['chat_id'] == id].tolist()
    nomre=int(df.loc[idx[0], 'sual_nomresi'])+2
    df = pd.read_csv('data/sikayet_olunmus_suallar.csv')
    idx = df.index[df['sual_nomresi'] == nomre].tolist()
    if(len(idx)==0):
        dict = {
        'sual_nomresi': [nomre],
        'sikayet_sayi': [1],
        'sikayet_olunan_chatlar' : [f'#{id}']
        }
        add = pd.DataFrame(dict)
        df = pd.concat([df, add], ignore_index=True)
        df.to_csv('data/sikayet_olunmus_suallar.csv', index=False)
    else:
        df.loc[idx[0], 'sikayet_sayi'] += 1
        if(str(id) in df.loc[idx[0], 'sikayet_olunan_chatlar'] ):
            pass
        else:
            df.loc[idx[0], 'sikayet_olunan_chatlar']+= f'#{id}'
        df.to_csv('data/sikayet_olunmus_suallar.csv', index=False)
    

