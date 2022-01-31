from django.test import tag
from googleapiclient.discovery import build
import os
import re
from datetime import timedelta

try:
    hour_pattern=re.compile(r'(\d+)H')
    minute_pattern=re.compile(r'(\d+)+M')
    second_pattern=re.compile(r'(\d+)+S')
    def convertSeconds(time):
        hour=hour_pattern.search(time)
        minute=minute_pattern.search(time)
        second=second_pattern.search(time)
        hour= int(hour.group(1)) if hour else 0
        minute=int(minute.group(1)) if minute else 0
        second=int(second.group(1)) if second else 0
        return  int(timedelta(hours=hour,
        minutes=minute,
        seconds=second).total_seconds())
    api_key=os.environ.get('youtube_api_key')
    #create an api specific service object
    youtube=build('youtube','v3',developerKey=api_key)
    playlistId=input("Enter a Playlist Id: ")
    nextPageToken=None
    duration=0
    while True:
            pl_request=youtube.playlistItems().list(part='contentDetails',playlistId=playlistId,pageToken=nextPageToken,maxResults=50)
            pl_response=pl_request.execute()
            pl_info=pl_response['items']
            videoId=[]
            for item in pl_info:
                videoId.append(item['contentDetails']['videoId'])
            vd_request=youtube.videos().list(part='contentDetails',id=','.join(videoId))
            vd_response=vd_request.execute()
            vd_info=vd_response['items']
            for item in vd_info:
                duration+=convertSeconds(item['contentDetails']['duration'])
            nextPageToken=pl_response.get('nextPageToken')
            if not nextPageToken:
                break
    minute,second=divmod(duration,60)
    hour,minute=divmod(minute,60)  
    print(f"Duration: {hour}:{minute}:{second}")
except Exception as e:
    print('Your Request Can not be successed')
    
    