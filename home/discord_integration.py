import requests

# https://discord.com/api/v9/channels/918848924033380405/messages -> mine
# https://discord.com/api/v9/channels/806880311769563170/messages ->V6

#authorization: NzYwNTEwOTg2NTQ4ODA1NjQy.YK5FNw.fMYRaL228PKlLwF_T9A9Am4fTp4 ->mine
#authorization : NzYwNTEwOTg2NTQ4ODA1NjQy.YK5FNw.fMYRaL228PKlLwF_T9A9Am4fTp4 ->v6

payload={
    'content': "FirstTrial"
}

header={
        "authorization": "NzYwNTEwOTg2NTQ4ODA1NjQy.YK5FNw.fMYRaL228PKlLwF_T9A9Am4fTp4 "
}
r=requests.post("https://discord.com/api/v9/channels/806880311769563170/messages",data=payload,headers=header)