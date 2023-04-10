import pandas as pd

def check(user_id):
    df = pd.read_csv('data/userdata.csv')
    idx = df.index[df['user_id'] == user_id].tolist()
    if(idx):
        return 1
    else:
        return 0

def save(user_id,username):
    df = pd.read_csv('data/userdata.csv')
    add = pd.DataFrame({'user_id':[user_id],
                        'username':[username]})
    df = pd.concat([df, add], ignore_index=True)
    df.to_csv('data/userdata.csv', index=False)

def user_data_add(message):
    userid = message.from_user.id
    username=message.from_user.username
    if(check(userid)!=1):
        save(userid,username)