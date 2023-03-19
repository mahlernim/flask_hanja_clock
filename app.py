from flask import Flask, render_template
import pandas as pd
import random
import datetime
from urllib import parse

app = Flask(__name__)

@app.route('/<user_hanja>')
@app.route('/')
def index(user_hanja=""):
    # Load hanja500.csv
    df = pd.read_csv('hanja500.csv')
    words_df = pd.read_csv('hanjawords500.csv')

    # Select a random hanja_row
    if not user_hanja:
        hanja_row = df.sample().iloc[0]
    else:
        if user_hanja in df['hanja'].values:
            hanja_row = df[df['hanja']==user_hanja].iloc[0]
        else:
            hanja_row = df.sample().iloc[0]

    # Get the current time in 24h format and seconds to wait until reload
    now = datetime.datetime.now()
    dow = '月火水木金土日'
    date_str = now.strftime('%Y年 %m月 %d日 ') + dow[now.weekday()] + "曜日"
    time_str = datetime.datetime.now().strftime('%H:%M')
    time_until_next_minute = 60 - now.second + 1
    
    # Get the values from the row
    hanja = hanja_row['hanja']
    huneum = hanja_row['huneum']
    strokes = hanja_row['strokes']
    radical = hanja_row['radical']
    read_level = hanja_row['read_level']
    write_level = hanja_row['write_level']
    
    # Get words
    matching_words = []
    for idx, row in words_df[words_df['hanja']==hanja].iterrows():
        word = row['kor'] + "("
        for letter in row['han']:
            if letter == hanja:
                word += letter
            elif letter in df['hanja'].values:
                # link letters that exist in the DB
                word += f"<a href='/{parse.quote(letter)}'>{letter}</a>"
            else:
                word += letter
        word += ")"
        matching_words.append({"word":word, "meaning":row['meaning']})

    # Render the template with the values
    return render_template("index.html", date=date_str, time=time_str, hanja=hanja, huneum=huneum, strokes=strokes, radical=radical,
        read_level=read_level, write_level=write_level, reload_interval=time_until_next_minute, matching_words=matching_words)

if __name__ == '__main__':
    app.run(debug=True)
