from flask import Flask, render_template
import datetime
import pytz
import sys
import tweepy

app = Flask(__name__)

app.config.from_object('config')
auth = tweepy.OAuthHandler(app.config['CONSUMERKEY'], app.config['CONSUMERSECRET'])
auth.set_access_token(app.config['ACCESSTOKENKEY'], app.config['ACCESSTOKENSECRET'])
tweepy = tweepy.API(auth)

start = datetime.date(2017, 1, 20)
today = datetime.date.today()
diff = today - start
day = diff.days

@app.route('/')
def index():
    today = str(datetime.date.today())
    username44 = '@BarackObama'
    username45 = '@realDonaldTrump'
    return render_template('layout.html', day=day, obamatweets=get_obama_tweets(username44),
        trumptweets=get_trump_tweets(username45), today=today)

def get_obama_tweets(username44):
    obamatweets = tweepy.user_timeline(username44)
    start = datetime.date(2009, 1, 20)
    date = start + datetime.timedelta(days=day)
    return [{'tweet': t.text, 'created_at': t.created_at, 'username': username44,
              'headshot_url': t.user.profile_image_url}
           for t in obamatweets]

def get_trump_tweets(username45):
    trumptweets = tweepy.user_timeline(username45)
    return [{'tweet': t.text, 'created_at': t.created_at.replace().strftime('%Y-%m-%d'), 'username': username45,
              'headshot_url': t.user.profile_image_url}
           for t in trumptweets]
