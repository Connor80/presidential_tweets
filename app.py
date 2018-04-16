from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
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
date44 = date.strftime('%-m/%d/%Y')

@app.route('/')
def index():
    today = str(datetime.date.today())
    username45 = '@realDonaldTrump'
    return render_template('layout.html', day=day, date=date44, today=today,
        trumptweets=get_trump_tweets(username45), text=get_obama_tweets())

def get_obama_tweets():
    option = webdriver.ChromeOptions()
    option.add_argument(" — incognito")
    path = app.config['PATH']
    browser = webdriver.Chrome(executable_path=path, chrome_options=option)
    browser.get("http://obamawhitehouse.gov.archivesocial.com")
    browser.set_page_load_timeout(60)

    #tab over to advanced search, click the drop down, and select custom
    tab = browser.find_element_by_xpath("//*[@id='notebook']/div[2]/ul/li[2]/a").click()
    date_drop_down = browser.find_element_by_xpath("//*[@id='dijit_form_Select_0']/tbody/tr/td[2]/input").click()
    custom = browser.find_element_by_xpath("//*[@id='dijit_MenuItem_6_text']").click()

    #clear default dates, enter search date, and change search to 'from'
    date_from = browser.find_element_by_xpath("//*[@id='dijit_form_DateTextBox_0']")
    date_to = browser.find_element_by_xpath("//*[@id='dijit_form_DateTextBox_1']")
    button = browser.find_element_by_xpath("//*[@id='advancedForm']/span/input")
    date_from.clear()
    date_from.send_keys(date44)
    date_to.clear()
    date_to.send_keys(date44)
    search_from = browser.find_element_by_xpath("//*[@id='dijit_form_Select_1']/tbody/tr/td[2]/input").click()
    from_drop_down = browser.find_element_by_xpath("//*[@id='dijit_MenuItem_8_text']").click()

    #clear all social media selections, select twitter, and search for tweets from white house
    clear = browser.find_element_by_xpath("//*[@id='contentClearLink']").click()
    twitter_icon = browser.find_element_by_xpath("//*[@id='accountTypes']/div[7]").click()
    twitter_select = browser.find_element_by_xpath("//*[@id='dijit_TooltipDialog_6']/div[1]/div/ul/li").click()
    search_terms = browser.find_element_by_xpath("//*[@id='dijit_form_ValidationTextBox_0']")
    search_terms.send_keys('white')
    search_terms.submit()
    text = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='pi_widget_twitter_TweetWidget_0']/div[1]/div/table/tbody/tr/td[2]/span"))).text

    return text

def get_trump_tweets(username45):
    trumptweets = tweepy.user_timeline(username45)
    return [{'tweet': t.text, 'created_at': t.created_at.replace().strftime('%Y-%m-%d'),
              'username': username45,
              'headshot_url': t.user.profile_image_url}
           for t in trumptweets]
