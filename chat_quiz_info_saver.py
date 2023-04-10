import pandas as pd

def zaman_ayar(chat_id,zaman):
    df=pd.read_csv('chat_quiz_info.csv')
    idx=df.index[df['chat_id']==chat_id].tolist()
    if(len(idx)!=0):
        df=df.drop(idx[0])
    dict={
        'chat_id':[chat_id],
        'sual_vaxti':[zaman]
    }
    add=pd.DataFrame(dict)
    df=pd.concat([df, add], ignore_index = True)
    df.to_csv('chat_quiz_info.csv',index=False)







def say_ayar(chat_id, say):
    df = pd.read_csv('chat_quiz_info.csv')
    idx = df.index[df['chat_id'] == chat_id].tolist()[0]
    df.loc[idx,'sual_sayi']=say
    df.to_csv('chat_quiz_info.csv', index=False)


def info(chat_id):
    df = pd.read_csv('chat_quiz_info.csv')
    idx = df.index[df['chat_id'] == chat_id].tolist()[0]
    return df['sual_sayi'][idx],df['sual_vaxti'][idx]

