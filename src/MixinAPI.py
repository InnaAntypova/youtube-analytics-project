import os
from googleapiclient.discovery import build


class MixinAPI:
    api_key: str = os.getenv('YOUTUBE_API_KEY')

    @classmethod
    def get_service(cls):
        """ Возвращает объект для работы с YouTube API"""
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube

