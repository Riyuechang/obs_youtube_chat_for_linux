import re
import atexit
import requests
import subprocess

import pytchat

from config import config
from tools.log import logger

#提取直播的影片代碼
def get_youtube_live_video_id(youtube_channel_id):
    if not re.search(r"@", youtube_channel_id):
        youtube_channel_id = "@" + youtube_channel_id

    youtube_url = f"https://www.youtube.com/{youtube_channel_id}/live"
    youtube_html = requests.get(youtube_url)

    return youtube_html.status_code, youtube_html.content.decode()

def youtube_html_process(youtube_html_content):
    video_id_search = re.search(r"(?<=https://www\.youtube\.com/watch\?v=)[a-zA-Z0-9]+", youtube_html_content)
    return video_id_search

get_status_code, get_content = get_youtube_live_video_id(config.youtube_channel_id)

if get_status_code == 200:
    video_id_search = youtube_html_process(get_content)

    if video_id_search:
        video_id = video_id_search.group(0)
        logger.info("已連接上YouTube直播")

        try:
            YouTube_chat = pytchat.create(video_id=video_id) #讀取直播

            command = ["python", "web_chat_room/app.py"] #指令和傳遞參數
            web_chat_room = subprocess.Popen(command, stdout=subprocess.PIPE) #呼叫Youtube_Chat.py

            def Execute_at_the_end():
                YouTube_chat.terminate() #停止獲取聊天室
                web_chat_room.terminate() #關閉網頁聊天室

            atexit.register(Execute_at_the_end) #註冊關閉事件


            #讀取聊天室
            while YouTube_chat.is_alive():
                for response in YouTube_chat.get().sync_items(): #等待新訊息
                    author_name = response.author.name
                    message = response.message

                    data = "{" + f"\"author_name\" : {author_name}, \"message\" : {message}" + "}" #輸出成指定格式
                    logger.info(data)

                    web_chat_room_url = f"http://127.0.0.1:3200/send_message?author_name={author_name}&message={message}"
                    web_chat_room_send_message = requests.get(web_chat_room_url)

                    if web_chat_room_send_message.status_code == 200:
                        logger.info(web_chat_room_send_message.content.decode())
                    else:
                        logger.error(f"無法連線到web_chat_room  錯誤:{web_chat_room_send_message.status_code}")
            
            logger.info("YouTube直播結束")
        except:
            logger.error("載入YouTube聊天室時發生錯誤")
    else:
        logger.error("YouTube直播未開啟")
else:
    logger.error("無法連線到YouTube直播")