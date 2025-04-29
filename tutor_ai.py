# -*- coding: utf-8 -*-
print("Running tutor AI")
bot_name = 'tutor_ai'
import os
import sys
try:
    mother_folder = sys.argv[1] ## 線上主機中的檔案位置
except:
    mother_folder = r"F:\Downloads\2025Work\bots" ## 線上主機中的檔案位置，線上，到客戶資料夾為止，EX:客戶資料夾名稱= test1

sys.path.append(f"{mother_folder}/{bot_name}")  ## 指到自己的Folder
import setting_config

line_channel_id = setting_config.line_channel_id
line_channel_secret = setting_config.line_channel_secret
line_token = setting_config.line_token

host_ip = setting_config.host_ip
port_ip = setting_config.port_ip

'''
code
'''
import requests
import re
import time
import random
from random import randint
import pandas as pd

from datetime import datetime
import io
import json

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (PostbackEvent, MessageEvent, TextMessage, 
                            TextSendMessage, StickerSendMessage, LocationSendMessage, ImageSendMessage, VideoSendMessage, 
                            TemplateSendMessage, FlexSendMessage, 
                            ButtonsTemplate, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn, 
                            QuickReply, QuickReplyButton, ConfirmTemplate,
                            MessageAction, MessageTemplateAction, URIAction, PostbackTemplateAction,
                            ImagemapSendMessage, BaseSize, URIImagemapAction, MessageImagemapAction, ImagemapArea, Video, ExternalLink,
                            RichMenuSwitchAction, RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, RichMenuAlias)

line_bot_api = LineBotApi(line_token)
handler = WebhookHandler(line_channel_secret)

## Vocab
with open(f'{mother_folder}/{bot_name}/Models/vocabulary.txt', 'r') as f:
    vocabulary = json.loads(f.read())
    
## Grammar
with open(f'{mother_folder}/{bot_name}/Models/grammar.txt', 'r') as f:
    grammar = json.loads(f.read())

from newspaper import Article
import nltk
nltk.download('punkt')

from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key='122eea9e4cd747f389858069a8d06742')

'''
Rich Menu
'''
initial_height=246
fix_height=360
rich_url_news = 'https://imgur.com/z1ljilj.png#'
rich_url_rand ='https://imgur.com/1Le5fIQ.png#'
function_8 = ['選難度', '查看文章', '單字解釋', '練習題', '查單字', '產生文章', '文法解釋', '幫我翻譯']
mode = ['chat', 'search', 'gen_article']

[line_bot_api.delete_rich_menu(i.rich_menu_id) for i in line_bot_api.get_rich_menu_list()]
[line_bot_api.delete_rich_menu_alias(i.rich_menu_alias_id) for i in line_bot_api.get_rich_menu_alias_list().aliases]

## Menu left-a
areas_a= [RichMenuArea(bounds= RichMenuBounds(x= 1251, y= 0, width= 1250, height= initial_height),
                       action= RichMenuSwitchAction(label= 'Switch_to_b', rich_menu_alias_id= 'richmenu-alias-b', data= "richmenu-changed-to-b")),
          RichMenuArea(bounds= RichMenuBounds(x= 0, y= initial_height , width= 1250, height= fix_height),
                       action= PostbackTemplateAction(label= function_8[0], data= function_8[0])),
          RichMenuArea(bounds= RichMenuBounds(x= 0, y= initial_height+fix_height, width= 1250, height= fix_height),
                       action= PostbackTemplateAction(label= function_8[1], data= function_8[1])),
          RichMenuArea(bounds= RichMenuBounds(x= 0, y= initial_height+fix_height*2, width= 1250, height= fix_height),
                       action= PostbackTemplateAction(label= function_8[2], data= function_8[2])),
          RichMenuArea(bounds= RichMenuBounds(x= 0, y= initial_height+fix_height*3, width= 1250, height= fix_height),
                       action= PostbackTemplateAction(label= function_8[3], data= function_8[3])),
          RichMenuArea(bounds= RichMenuBounds(x= 1250, y= initial_height, width= 1250, height= fix_height),
                       action= PostbackTemplateAction(label= function_8[4], data= function_8[4])),
          RichMenuArea(bounds= RichMenuBounds(x= 1250, y= initial_height+fix_height, width= 1250, height= fix_height),
                       action= PostbackTemplateAction(label= function_8[5], data= function_8[5])),
          RichMenuArea(bounds= RichMenuBounds(x= 1250, y= initial_height+fix_height*2, width= 1250, height= fix_height),
                       action= PostbackTemplateAction(label= function_8[6], data= function_8[6])),
          RichMenuArea(bounds= RichMenuBounds(x= 1250, y= initial_height+fix_height*3, width= 1250, height= fix_height),
                       action= PostbackTemplateAction(label= function_8[7], data= function_8[7]))]

rich_menu_to_a_create = RichMenu(size= RichMenuSize(width= 2500, height= 1686), selected= True, name= 'RichMenuA', 
                                 chat_bar_text= '現在是新聞模式!', areas= areas_a)
rich_menu_a_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_a_create)
    
line_bot_api.set_rich_menu_image(rich_menu_a_id, 'image/png', io.BytesIO(requests.get(rich_url_news, stream=True).content))

## Menu right-b
areas_b= [RichMenuArea(bounds= RichMenuBounds(x= 0, y= 0, width= 1250, height= initial_height),
                       action= RichMenuSwitchAction(label= 'Switch_to_a', rich_menu_alias_id= 'richmenu-alias-a', data= "richmenu-changed-to-a")),
          RichMenuArea(bounds= RichMenuBounds(x= 0, y= initial_height , width= 1250, height= fix_height),
                       action= PostbackTemplateAction(label= function_8[0], data= function_8[0])),
          RichMenuArea(bounds= RichMenuBounds(x= 0, y= initial_height+fix_height, width= 1250, height= fix_height),
                       action= PostbackTemplateAction(label= function_8[1], data= function_8[1])),
          RichMenuArea(bounds= RichMenuBounds(x= 0, y= initial_height+fix_height*2, width= 1250, height= fix_height),
                       action= PostbackTemplateAction(label= function_8[2], data= function_8[2])),
          RichMenuArea(bounds= RichMenuBounds(x= 0, y= initial_height+fix_height*3, width= 1250, height= fix_height),
                       action= PostbackTemplateAction(label= function_8[3], data= function_8[3])),
          RichMenuArea(bounds= RichMenuBounds(x= 1250, y= initial_height, width= 1250, height= fix_height),
                       action= PostbackTemplateAction(label= function_8[4], data= function_8[4])),
          RichMenuArea(bounds= RichMenuBounds(x= 1250, y= initial_height+fix_height, width= 1250, height= fix_height),
                       action= PostbackTemplateAction(label= function_8[5], data= function_8[5])),
          RichMenuArea(bounds= RichMenuBounds(x= 1250, y= initial_height+fix_height*2, width= 1250, height= fix_height),
                       action= PostbackTemplateAction(label= function_8[6], data= function_8[6])),
          RichMenuArea(bounds= RichMenuBounds(x= 1250, y= initial_height+fix_height*3, width= 1250, height= fix_height),
                       action= PostbackTemplateAction(label= function_8[7], data= function_8[7]))]

rich_menu_to_b_create = RichMenu(size= RichMenuSize(width= 2500, height= 1686), selected= True, name= 'RichMenuB',
                                 chat_bar_text= '現在是隨機模式!', areas= areas_b)
rich_menu_b_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_b_create)
    
line_bot_api.set_rich_menu_image(rich_menu_b_id, 'image/png', io.BytesIO(requests.get(rich_url_rand, stream=True).content))


line_bot_api.set_default_rich_menu(rich_menu_a_id)
alias_a = RichMenuAlias(rich_menu_alias_id='richmenu-alias-a', rich_menu_id=rich_menu_a_id)
line_bot_api.create_rich_menu_alias(alias_a)

alias_b = RichMenuAlias(rich_menu_alias_id='richmenu-alias-b', rich_menu_id=rich_menu_b_id)
line_bot_api.create_rich_menu_alias(alias_b)

print('success')


'''
Chat Function
'''
buttons = []
buttons.append(TemplateSendMessage(alt_text='Buttons template', 
                                   template=ButtonsTemplate(title='請先選難度', text='Elementary, Junior, Senior, University',
                                                            actions=[MessageTemplateAction(label='Elementary', text='Elementary-school'),
                                                                     MessageTemplateAction(label='Junior', text= 'Junior-high'),
                                                                     MessageTemplateAction(label='Senior', text='Senior-high'),
                                                                     MessageTemplateAction(label='University', text='University')])))

'''
ChatGPT
'''
from openai import OpenAI
tutor_key = setting_config.tutor_key
translate_key = setting_config.translate_key
gpt_mode = "gpt-3.5-turbo-1106"

from opencc import OpenCC
stp = OpenCC('s2twp')

def rewrite_articles(openai_key, instruct, difficulty, article, limit, text_n=3000):
    global response, command , gpt_model   
    rewrite_command = {
        'article': f"rewrite the article to a {difficulty} level paragraph which less than {limit} words",
        'vocab': f"pick {limit} vocabulaires used in the paragraph, then give the meanings and short example sentence for the {limit} vocabularies",
        'grammar': f"shortly explain {limit} grammar used in the paragraph",
        'exercise': f"give {limit} single exercises with answer and short explanation for {difficulty} students"}
    command = f"You are a {difficulty} English tutor, you will {rewrite_command[instruct]}."
    response = OpenAI(api_key=openai_key).chat.completions.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": command},
            {"role": "user", "content": article},
            ],
        max_tokens=text_n,
        top_p=0.8,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0,
        temperature=0.6,
    )
    return stp.convert(response.choices[0].message.content)

def create_articles(openai_key, difficulty, vocab_list, grammar, subject, limit, text_n=3000):
    global response, command, gpt_model    
    command = f"You are a {difficulty} English tutor, you will pick 5 vocabularies from {vocab_list}, \
        use it and the grammar-{grammar} to write a {difficulty} level paragraph about {subject} which less than {limit} words."
            
    response = OpenAI(api_key=openai_key).chat.completions.createe(
        model=gpt_model,
        messages=[
            {"role": "system", "content": command},
            {"role": "user", "content": "I am a {difficulty} student, give me an paragraph about {subject} which less than {limit} words."},
            ],
        max_tokens=text_n,
        top_p=0.8,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0,
        temperature=0.5,
    )
    return stp.convert(response.choices[0].message.content)

def translate_articles(openai_key, article, text_n=3000):   
    global response, command, gpt_model
    command = "你是一名英文翻譯，請把內容翻譯成繁體中文"
    response = OpenAI(api_key=openai_key).chat.completions.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": command},
            {"role": "user", "content": article},
            ],
        max_tokens=text_n,
        top_p=0.8,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0,
        temperature=0.5,
    )
    return stp.convert(response.choices[0].message.content)

def search_vocab(openai_key, vocab):   
    global response, command, gpt_model
    command = "你是一個單字英語老師，以繁體中文回答這個單字的意思，並給一個英文例句與翻譯"
    response = OpenAI(api_key=openai_key).chat.completions.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": command},
            {"role": "user", "content": vocab},
            ],
        max_tokens=3000,
        top_p=0.8,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0,
        temperature=0.5,
    )
    return stp.convert(response.choices[0].message.content)

def random_vocab(vocab_list, n=10):
    return random.sample(vocab_list, n)

def article_process(msg):
    global article_in_process, this_article
    all_articles = newsapi.get_everything(q=msg, language='en', sort_by='relevancy')
    this_article = random.choice(all_articles['articles'])
    url = this_article['url']
    source = this_article['source']
    article = Article(url)

    article.download()
    article.parse()
    article.nlp()

    title = article.title
    # text = article.text
    summary = article.summary
    
    return title, summary

def chatbot(openai_key, sentence, text_n=3000):
    global response, gpt_model
    response = OpenAI(api_key=openai_key).chat.completions.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": f"You are a {difficulty} English tutor, chat with the student."},
            {"role": "user", "content": sentence},
            ],
        max_tokens=text_n,
        top_p=0.8,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0,
        temperature=0.5,
    )
    return stp.convert(response.choices[0].message.content)


'''
API
'''
difficulty = 'University'
vocabulary_list={'Elementary-school': vocabulary['1']+vocabulary['2']+vocabulary['3'], 'Junior-high': vocabulary['4']+vocabulary['5'], 
                 'Senior-high': vocabulary['6']+vocabulary['7'], 'University': vocabulary['8']+vocabulary['9']}
grammar_list={'Elementary-school': grammar['a1']['titles'], 'Junior-high': grammar['a2']['titles'], 'Senior-high': grammar['b1']['titles'],
              'University': grammar['b1.5']['titles']+grammar['b2']['titles']}

article_in_process = False
now_article, now_content, now_mode, now_gen_mode = "", "", "chat", "richmenu-changed-to-a"
n=0

app = Flask(__name__)
# 接收 LINE 的資訊
@app.route("/", methods=['POST'])
def call_back():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    body_check = json.loads(body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def dscbot_chat(event):
    global msg, user_id, difficulty, article_in_process, now_article, now_content, now_mode, mode, now_gen_mode, title, summary, n
    n+=1
    msg = event.message.text
    user_id = event.source.user_id
    reply_token = event.reply_token
    
    ## Algorithm
    if not article_in_process:
        article_in_process = True
        try:
            if now_mode == mode[1]: # now_mode = "search"
                result = search_vocab(tutor_key, msg)
                now_mode = "chat"
                article_in_process = False
                line_bot_api.reply_message(reply_token, TextSendMessage(text=result))
                
            elif now_mode == mode[2]: # now_mode = "gen_article"
                now_mode = "chat"
                try:
                    if now_gen_mode == "richmenu-changed-to-a":
                        title, summary = article_process(msg)
                        now_article = rewrite_articles(tutor_key, 'article', difficulty, summary, 60)
                        now_content = now_article
                        
                        article_in_process = False
                        line_bot_api.reply_message(reply_token, [TextSendMessage(text=title), TextSendMessage(text=now_article)])
                        
                    elif now_gen_mode == "richmenu-changed-to-b":
                        now_article = create_articles(tutor_key, difficulty, random_vocab(vocabulary_list[difficulty], 10), 
                                                      random_vocab(grammar_list[difficulty], 1), msg, 60)
                        now_content = now_article
                        
                        article_in_process = False
                        line_bot_api.reply_message(reply_token, [TextSendMessage(text=now_article)])
                except:
                    article_in_process = False
                    line_bot_api.reply_message(reply_token, TextSendMessage(text="No result"))
            
            else:
                if msg == '難度':
                    article_in_process = False
                    line_bot_api.reply_message(reply_token, buttons)
                elif msg in ['Elementary-school', 'Junior-high', 'Senior-high', 'University']:
                    difficulty=msg
                    article_in_process = False
                    line_bot_api.reply_message(reply_token, TextSendMessage(text=f'The difficulty now is {difficulty}'))
                else:
                    article_in_process = False
                    line_bot_api.reply_message(reply_token, TextSendMessage(text=chatbot(tutor_key, msg)))
        except:
            article_in_process = False
            line_bot_api.reply_message(reply_token, TextSendMessage(text="Please try again"))
    else:
        line_bot_api.reply_message(reply_token, TextSendMessage(text="Still running!"))

@handler.add(PostbackEvent)
def dscbot_call(event):
    global callback, article_in_process, now_article, now_content, now_mode, mode, now_gen_mode, n
    n+=1
    callback = event.postback.data
    user_id = event.source.user_id
    reply_token = event.reply_token
    
    ## Build df
    menu_df = pd.DataFrame(columns=["menu_data", "func", "return", "now_content", "mode"])
    menu_list = [["richmenu-changed-to-a", "text", "新聞模式產生之文章皆由新聞改寫，並會針對不同程度的學生產生相對應難度的文章", 0, now_mode],
                 ["richmenu-changed-to-b", "text", "隨機模式為AI針對學生輸入之關鍵字產生文章，由於為隨機產生，因此文章內容可能不屬實", 0, now_mode],
                 ["選難度", "button", buttons, 0, now_mode], 
                 ["查看文章", "text", now_article, 0, now_mode],
                 ["單字解釋", "text", [rewrite_articles, tutor_key, 'vocab', difficulty, now_article, 5], 1, mode[0]],
                 ["練習題", "text", [rewrite_articles, tutor_key, 'exercise', difficulty, now_article, 2], 1, mode[0]],
                 
                 ["查單字", "text", "Please enter a vocabulary", 0, mode[1]],
                 ["產生文章", "text", "Please enter a keyword", 0, mode[2]], 
                 ["文法解釋", "text", [rewrite_articles, tutor_key, 'grammar', difficulty, now_article, 2], 1, mode[0]],
                 ["幫我翻譯", "text", [translate_articles, translate_key, now_content], 0, now_mode]
                 ]
    for row in menu_list:
        menu_df.loc[len(menu_df)]=row
        
    
    ## Algorithm    
    if not article_in_process:
        article_in_process = True
        try:
            now_row = menu_df.loc[menu_df["menu_data"] == callback]
            ## 選難度
            if now_row['func'].iloc[0]=="button":
                article_in_process = False
                line_bot_api.reply_message(reply_token, now_row['return'].iloc[0])
            elif now_row['func'].iloc[0]=="text":
                now_mode = now_row['mode'].iloc[0]
                
                if callback in ["richmenu-changed-to-a", "richmenu-changed-to-b"]: 
                    now_gen_mode = callback
                    article_in_process = False
                    line_bot_api.reply_message(reply_token, TextSendMessage(text=now_row['return'].iloc[0]))
                    
                elif callback in ["查單字", "產生文章", "查看文章"]:
                    article_in_process = False
                    line_bot_api.reply_message(reply_token, TextSendMessage(text=now_row['return'].iloc[0]))
                else: 
                    ## 單字解釋，練習題，文法解釋 
                    if now_row['now_content'].iloc[0]:
                        f, *args = now_row['return'].iloc[0]
                        now_content = f(*args)
                        article_in_process = False
                        line_bot_api.reply_message(reply_token, TextSendMessage(text=now_content))
                    ## 幫我翻譯
                    else:
                        f, *args = now_row['return'].iloc[0]
                        temp = f(*args)
                        article_in_process = False
                        line_bot_api.reply_message(reply_token, TextSendMessage(text=temp))
        except:
            article_in_process = False
            line_bot_api.reply_message(reply_token, TextSendMessage(text="請先產生文章"))
    else:
        line_bot_api.reply_message(reply_token, TextSendMessage(text="Still running!"))

app.run(port= port_ip)
