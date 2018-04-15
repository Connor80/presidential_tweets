from flask import Flask, render_template
import datetime
import tweepy

app = Flask(__name__)

app.config.from_object('config')
auth = tweepy.OAuthHandler(app.config['CONSUMERKEY'], app.config['CONSUMERSECRET'])
auth.set_access_token(app.config['ACCESSTOKENKEY'], app.config['ACCESSTOKENSECRET'])
tweepy = tweepy.API(auth)

inauguration44 = datetime.date(2009, 1, 20)
inauguration45 = datetime.date(2017, 1, 20)
today = datetime.date.today()
diff = today - inauguration45
day = diff.days
date = inauguration44 + datetime.timedelta(days=day)

@app.route('/')
def index():
    today = str(datetime.date.today())
    username44 = '@BarackObama'
    username45 = '@realDonaldTrump'
    return render_template('layout.html', day=day, date=date, today=today,
        obamatweets=get_obama_tweets(username44), trumptweets=get_trump_tweets(username45))

def get_obama_tweets(username44):
    obamatweets = tweepy.user_timeline(username44)
    return [{'tweet': t.text, 'created_at': t.created_at.replace().strftime('%Y-%m-%d'),
              'username': username44,
              'headshot_url': t.user.profile_image_url}
           for t in obamatweets]

def get_trump_tweets(username45):
    trumptweets = tweepy.user_timeline(username45)
    return [{'tweet': t.text, 'created_at': t.created_at.replace().strftime('%Y-%m-%d'),
              'username': username45,
              'headshot_url': t.user.profile_image_url}
           for t in trumptweets]
