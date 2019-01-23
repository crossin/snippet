# coding: utf-8
import itchat
import tkinter.messagebox
import winsound
# import os
# import pygame

def alarm():
    # Windows嗡鸣声
    winsound.Beep(1000, 3000)
#     # Mac语音
#     os.system('say "有人发红包了，赶紧去抢啊！红红火火恍恍惚惚哈哈哈哈"')
#     # 播放MP3
#     pygame.mixer.init()
#     track = pygame.mixer.music.load('alarm.mp3')
#     pygame.mixer.music.play()
    tkinter.messagebox.showinfo('重要提醒','有人发红包了！') 


@itchat.msg_register('Note', isGroupChat=True)
def get_note(msg):
    if '红包' in msg['Text']:
        print('note:',msg['Text'])
        alarm()

@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def _(msg):
    print('text:',msg['Text'])

itchat.auto_login(hotReload=True)
itchat.run()
itchat.logout()

