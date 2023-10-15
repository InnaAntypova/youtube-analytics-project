import os
import isodate
from googleapiclient.discovery import build
import json
import datetime

""" Класс для Video из Youtube"""


class PlayList:
    def __init__(self, playlist_id: str) -> None:
        """Экземпляр инициализируется id плейлиста. Остальные данные берем из API."""
        self.__playlist_id = playlist_id
        self.url = f"https://www.youtube.com/playlist?list={self.__playlist_id}"

        # Получаем playlist по его id
        self.playlist = PlayList.get_service().playlists().list(id=self.__playlist_id, part='snippet', ).execute()

        self.title = self.playlist['items'][0]['snippet']['title']

        # Получаем список видео из playlist
        self.playlist_videos = PlayList.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                                           part='snippet,contentDetails',
                                                                           maxResults=50,
                                                                           ).execute()

        # Получаем все id видеороликов из playlist
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        # Получаем информацию о видеороликах по списку собранных video_id
        self.video_response = PlayList.get_service().videos().list(part='contentDetails,statistics',
                                                                   id=','.join(self.video_ids)
                                                                   ).execute()

    @property
    def playlist_id(self):
        """ Делаем video_id приватным"""
        return self.__playlist_id

    def print_info(self):
        """ Выводит информацию для разработчика"""
        print(json.dumps(self.playlist, indent=2, ensure_ascii=False))
        print("")
        print("")
        print(json.dumps(self.playlist_videos, indent=2, ensure_ascii=False))
        print("")
        print("")
        print(json.dumps(self.video_response, indent=2, ensure_ascii=False))

    @property
    def total_duration(self) -> datetime:
        """ Метод возвращает суммарную длительность видео"""
        durations = datetime.timedelta()
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            durations += isodate.parse_duration(iso_8601_duration)

        return durations

    def __str__(self) -> str:
        """ Возвращает информацию об экземпляре класса"""
        return f"{self.__playlist_id}\n{self.title}\n{self.url}"

    def show_best_video(self) -> str:
        """ Метод возвращает видео с наибольшим кол-вом лайков"""
        count_likes = 0
        best_video_id = ""
        for video in self.video_response['items']:
            like_count = int(video['statistics']['likeCount'])
            if like_count > count_likes:
                best_video_id = video['id']

        return f"https://youtu.be/{best_video_id}"

    @classmethod
    def get_service(cls):
        """ Возвращает объект для работы с YouTube API"""
        api_key: str = os.getenv('YOUTUBE_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube
