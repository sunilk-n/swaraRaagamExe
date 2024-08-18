import os
from dataclasses import dataclass
from typing import Optional, List

from services.firestore_service import firestore_db
from models import song_info_collection_name


class SongInfoCollection:
    def __init__(self):
        self.songs = []

    def get_all_songs(self):
        song_info_collection = firestore_db.collection(song_info_collection_name).get()
        for song in song_info_collection:
            songObj = song.to_dict()
            songObj['songId'] = song.id
            self.songs.append(songObj)

    def get_song_data(self, song_id):
        for song in self.songs:
            if song['songId'] == song_id:
                return song

    @staticmethod
    def get_song(song_id):
        song = firestore_db.collection(song_info_collection_name).document(song_id).get()
        song_data = {}
        if song.exists:
            song_data = song.to_dict()
            song_data['songId'] = song.id

        return song_data

    def search_songs(self, search_term):
        self.get_all_songs()
        search_items = []
        for song in self.songs:
            if search_term in song['songName']:
                search_items.append(song)
        return search_items


@dataclass
class SongInfo:
    songName: str
    movieName: Optional[str] = None
    movieYear: Optional[int] = None
    songInfo_id: Optional[str] = None
    actors: Optional[List[str]] = None
    composer: Optional[str] = None
    singers: Optional[List[str]] = None
    tags: Optional[List[str]] = None


    def save(self):
        doc_ref = firestore_db.collection(song_info_collection_name).document()
        self.songInfo_id = doc_ref.id
        doc_ref.set(self.to_dict())

    def to_dict(self):
        return {
            'songName': self.songName,
            'movieName': self.movieName,
            'movieYear': self.movieYear
        }

    def jsonify(self):
        return {
            'songId': self.songInfo_id,
            'songName': self.songName,
            'movieName': self.movieName,
            'movieYear': self.movieYear
        }

    @classmethod
    def get_by_id(cls, songInfo_id: str):
        song = firestore_db.collection(song_info_collection_name).document(songInfo_id).get()
        if song.exists:
            song_data = song.to_dict()
            return cls(**song_data, songInfo_id=song.id)
        else:
            return None
