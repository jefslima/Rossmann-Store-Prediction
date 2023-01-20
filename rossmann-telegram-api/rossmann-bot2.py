import pandas as pd
import json
import requests
import os
import seaborn as sns
import telegram
import matplotlib.ticker as mticker
from flask import Flask, request, Response


#constants
TOKEN ='5452388971:AAG-fo1jfiVmpTAx7J_JtSE8tfhOjway5gQ'

#info about the bot
#https://api.telegram.org/bot5452388971:AAG-fo1jfiVmpTAx7J_JtSE8tfhOjway5gQ/getMe

#get updates
#https://api.telegram.org/bot5452388971:AAG-fo1jfiVmpTAx7J_JtSE8tfhOjway5gQ/getUpdates

#get sendMessage
#https://api.telegram.org/bot5452388971:AAG-fo1jfiVmpTAx7J_JtSE8tfhOjway5gQ/sendMessage?chat_id=309116313&text=Hi Jef

#SetWebHook (Set url from API from Telegram)
#https://api.telegram.org/bot5452388971:AAG-fo1jfiVmpTAx7J_JtSE8tfhOjway5gQ/setWebhook?url=https://rossmann-telegram-api-2.onrender.com

#Delete SetWebHook
#https://api.telegram.org/bot5452388971:AAG-fo1jfiVmpTAx7J_JtSE8tfhOjway5gQ/deleteWebhook

def  send_message(chat_id, text, _bot, parse='HTML'):
    _bot.send_message(chat_id, text, parse_mode=parse)


    return None

def load_dataset(store_id=None, full=False):
    # loading test dataset
    df_test_raw = pd.read_csv('test.csv')
    df_store_raw = pd.read_csv('store.csv')

    # merge test dataset with Store
    df_test = pd.merge(df_test_raw, df_store_raw, how='left', on='Store')

    if not full:
        # choose store for prediction
        df_test = df_test[df_test['Store'].isin(store_id)]

    if not df_test.empty:
        # remove closed days
        df_test = df_test[df_test['Open'] != 0]
        df_test = df_test[~df_test['Open'].isnull()]
        df_test = df_test.drop('Id', axis=1)

        # convert DataFrame to JSON
        data = json.dumps(df_test.to_dict(orient='records'))

    else:
        data = 'error'

    return data



def predict( data ):
    # API Call
    url = 'https://render-rossmann-store-api.onrender.com/rossmann/predict'
    header = {'Content-type': 'application/json' }
    data = data

    r = requests.post( url, data=data, headers=header )
    print( 'Status Code {}'.format( r.status_code ) )

    d1 = pd.DataFrame( r.json(), columns=r.json()[0].keys() )

    return d1

def get_help(greeting=True):
    msg_help_g = ''
    if greeting:

        linkedin_link = 'https://www.linkedin.com/in/jefersonslima/'
        github_link = 'https://github.com/jefslima'

        msg_help_g  = '''Hello!
Welcome to Rossmann Stores Sales Prediction!
A project developed by <a href="{}">Jeferson Lima</a>.
For full info, go to the <a href="{}">project github</a>.
Through this telegram bot you will access sales preditions of Rossmann Stores.
'''.format(linkedin_link, github_link)

    msg_help = msg_help_g + '''<b><u>Here are you options</u></b>
<b><i>start</i></b> : project info
<b><i>help</i></b> : available commands
<b><i>n</i></b> : prediction for a single store, where n is the id of a store
<b><i>n,n,n,n</i></b> : predictions for a list of stores, where n is the id of a store.
Stay hungry stay foolish!
   '''

    return msg_help

bot = telegram.Bot(token=TOKEN)

def parse_message(message):
    chat_id = message['message']['chat']['id']
    store_id = message['message']['text']

    command = store_id.replace('/', '')
    command = store_id.replace(' ', '')

    return chat_id, command


# API initialize
app = Flask( __name__ )

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        message = request.get_json()

        chat_id, command = parse_message(message)

        try:
            command = command.lower()
        except ValueError:
            command = command

        try:
            command = int(command)
        except ValueError:
            command = command

        if type(command) != int:
            command = command.split(',') if command.find(',') >= 0 else command
        print('Comando: {}'.format(command))

        # filtered prediction
        if (type(command) == list) | (type(command) == int):
            # reshape if there is only one store_id and convert list from string to int
            if type(command) == list:

                store_id = [int(x) for x in command]

            else:

                store_id = [command,]

            send_message(chat_id, 'Loading. Please wait...', bot)

            # loading data
            data = load_dataset(store_id)

            if data != 'error':

                # prediction
                d1 = predict(data)

                # calculation
                d2 = d1[['store', 'prediction']].groupby('store').sum().reset_index()

                for i in range(len(d2)):

                # send message
                    msg = 'Store Number {} will sell R${:,.2f} in the next 6 weeks'.format(
                        d2.loc[i, 'store'],
                        d2.loc[i, 'prediction']
                    )
                    send_message(chat_id, msg, bot)
                    return Response( 'Ok', status=200 )
            else:
                send_message(chat_id, 'Store ID do not exist', bot)
                return Response( 'Ok', status=200 )

        # start
        elif (command == 'start'):

            msg_help = get_help()
            send_message(chat_id, msg_help, bot)

        # help
        elif (command == 'help'):

            msg_help = get_help(False)
            send_message(chat_id, msg_help, bot)
            return Response( 'Ok', status=200 )

        else:

            msg_help = get_help(greeting = False)
            send_message(chat_id, 'This is an invalid command!', bot)
            send_message(chat_id, msg_help, bot)
            return Response( 'Ok', status=200 )

        send_message(chat_id, 'Done!', bot)
        return Response('Ok', status=200)

    else:
           return '<h1> Rossmann Telegram BOT</h1>'

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port=port)
