import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        self.request = Channel.get_service().channels().list(
            part="snippet,contentDetails,statistics",
            id=self.__channel_id
        ).execute()

        self.title = self.request['items'][0]['snippet']['title']
        self.video_count = self.request['items'][0]['statistics']['videoCount']
        self.url = f"https://www.youtube.com/watch?v={self.__channel_id}"
        self.description = self.request['items'][0]['snippet']['description']
        self.subscriber_count = self.request['items'][0]['statistics']['subscriberCount']
        self.view_count = self.request['items'][0]['statistics']['viewCount']

    def __str__(self):
        """ Возвращает информацию об экземпляре класса по шаблону '<Название канала> (<Ссылка на канал>)' """
        return f"'{self.title} ({self.url})'"

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.request, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """ Возвращает объект для работы с YouTube API"""
        api_key: str = os.getenv('YOUTUBE_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

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

    def __add__(self, other) -> int:
        """ Метод складывает данные двух каналов по кол-ву подписчиков"""
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other) -> int:
        """ Метод вычитает данные двух каналов по кол-ву подписчиков"""
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other) -> bool:
        """ Метод сравнивает ('больше') данные двух каналов по кол-ву подписчиков"""
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other) -> bool:
        """ Метод сравнивает ('больше' или 'равно') данные двух каналов по кол-ву подписчиков"""
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other) -> bool:
        """ Метод сравнивает ('меньше') данные двух каналов по кол-ву подписчиков"""
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other) -> bool:
        """ Метод сравнивает ('меньше' или 'равно') данные двух каналов по кол-ву подписчиков"""
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other) -> bool:
        """ Метод сравнивает ('равны' или 'не равны') данные двух каналов по кол-ву подписчиков"""
        return int(self.subscriber_count) == int(other.subscriber_count)

