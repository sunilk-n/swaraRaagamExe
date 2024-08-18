from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

from services.firestore_service import firestore_db
from models.songInfo import SongInfo as _SongInfo, song_info_collection_name
from google.cloud.firestore_v1 import DocumentReference
from models import song_collection_name


@dataclass
class Song:
    songId: Optional[str] = None
    songFileName: Optional[str] = None
    createdAt: Optional[datetime] = datetime.utcnow()
    editedAt: Optional[datetime] = None
    isPublished: Optional[bool] = False
    likes: Optional[int] = 0
    dislikes: Optional[int] = 0
    songInfo_ref: Optional[DocumentReference] = None
    songInfo: Optional[_SongInfo] = None

    def save(self, song_info_id: str = None):
        if song_info_id:
            self.songInfo_ref = firestore_db.collection(song_info_collection_name).document(song_info_id)
            self.songInfo = self.songInfo_ref.get()
        else:
            raise ValueError("song_info_id is required")
        if not self.songFileName:
            self.songFileName = f"{self.songInfo.data['songName']}_{song_info_id}"
        doc_ref = firestore_db.collection(song_collection_name).document()
        self.songId = doc_ref.id
        doc_ref.set(self.to_dict())

    def delete(self):
        doc_ref = firestore_db.collection(song_collection_name).document(self.songId)
        doc_ref.delete()

    def to_dict(self):
        return {
            "songFileName": self.songFileName,
            "createdAt": self.createdAt,
            "editedAt": self.editedAt,
            "isPublished": self.isPublished,
            "likes": self.likes,
            "dislikes": self.dislikes,
            "songInfo": self.songInfo_ref
        }

    def jsonify(self):
        # songInfo = SongInfo.get_by_id(self.songInfo_ref.id)
        # print(songInfo, self.songInfo_ref.id)
        # print(self.songInfo_ref)
        return {
            "songId": self.songId,
            "songFileName": self.songFileName,
            "createdAt": self.createdAt,
            "editedAt": self.editedAt,
            "isPublished": self.isPublished,
            "likes": self.likes,
            "dislikes": self.dislikes,
            "songInfo": self.songInfo.jsonify()
        }

    @classmethod
    def get_by_id(cls, doc_id: str):
        song = firestore_db.collection(song_collection_name).document(doc_id).get()
        if song.exists:
            song_data = song.to_dict()
            songInfo_doc = song_data['songInfo'].get()
            if songInfo_doc.exists:
                songInfo = SongInfo(songInfo_id=songInfo_doc.id, **songInfo_doc.to_dict())
            else:
                songInfo = None
            song_data['songInfo_ref'] = song_data['songInfo']
            song_data['songInfo'] = songInfo
            return cls(songId=doc_id, **song_data)
        else:
            return None


class SongCollection:
    songs: List[Song] = field(default_factory=list)

    def get_all_songs(self, limit: int = 10):
        self.songs = []
        songs = firestore_db.collection(song_collection_name).limit(limit).stream()
        for song in songs:
            song_data = song.to_dict()
            songInfo_doc = song_data['songInfo'].get()
            if songInfo_doc.exists:
                songInfo = _SongInfo(songInfo_id=songInfo_doc.id, **songInfo_doc.to_dict())
            else:
                songInfo = None
            song_data['songInfo_ref'] = song_data['songInfo']
            song_data['songInfo'] = songInfo
            self.songs.append(Song(**song_data, songId=song.id))

    def jsonify(self):
        return [song.jsonify() for song in self.songs]


@dataclass
class SongLocal:
    songFileName: Optional[str] = None
