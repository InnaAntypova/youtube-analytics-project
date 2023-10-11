import os
from googleapiclient.discovery import build
import json

""" Класс для Video из Youtube"""


class Video:
    def __init__(self, video_id):
        """Экземпляр инициализируется id видео. Остальные данные берем из API."""
        self.__video_id = video_id

        self.request = Video.get_service().videos().list(
            part='snippet,statistics,contentDetails,topicDetails',
            id=self.__video_id
        ).execute()

        self.video_title = self.request['items'][0]['snippet']['title']
        self.view_count = self.request['items'][0]['statistics']['viewCount']
        self.like_count = self.request['items'][0]['statistics']['likeCount']
        self.video_url = f"https://www.youtube.com/watch?v={self.__video_id}"

    @property
    def video_id(self):
        """ Делаем video_id приватным"""
        return self.__video_id

    def __str__(self):
        """ Возвращает информацию о названии видео. """
        return f"{self.video_title}"

    def print_info(self):
        """ Выводит информацию о видео"""
        print(json.dumps(self.request, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """ Возвращает объект для работы с YouTube API"""
        api_key: str = os.getenv('YOUTUBE_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


""" Дочерний класс от класса Video для работы с видео и плейлистом"""


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        """Экземпляр инициализируется id видео и id плейлиста. Остальные данные берем из API."""
        super().__init__(video_id)
        self.playlist_id = playlist_id

        self.request = PLVideo.get_service().videos().list(
            part='snippet,statistics,contentDetails,topicDetails',
            id=self.video_id
        ).execute()

        self.video_title = self.request['items'][0]['snippet']['title']
        self.view_count = self.request['items'][0]['statistics']['viewCount']
        self.like_count = self.request['items'][0]['statistics']['likeCount']
        self.video_url = f"https://www.youtube.com/watch?v={self.video_id}"
