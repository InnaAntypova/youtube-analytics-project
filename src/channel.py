import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        self.request = Channel.youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id="UC_x5XG1OV2P6uZZ5FSM9Ttw"
        ).execute()

        self.title = self.request['items'][0]['snippet']['title']
        self.video_count = self.request['items'][0]['statistics']['videoCount']
        self.url = self.request['items'][0]['snippet']['thumbnails']['default']['url']
        self.description = self.request['items'][0]['snippet']['description']
        self.subscriber_count = self.request['items'][0]['statistics']['subscriberCount']
        self.view_count = self.request['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.request, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """ Возвращает объект для работы с YouTube API"""
        return cls.youtube

    def to_json(self, channel_name: str):
        """ Сохраняет в файл значения атрибутов экземпляра `Channel` """
        to_json = {'channel_id': self.__channel_id,
                   'title': self.title,
                   'description': self.description,
                   'url': self.url,
                   'video_count': self.video_count,
                   'subscriber_count': self.subscriber_count,
                   'view_count': self.view_count
                   }

        with open(channel_name, 'w') as f:
            f.write(json.dumps(to_json, indent=2, ensure_ascii=False))

