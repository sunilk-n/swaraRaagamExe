import os


song_collection_name = None
song_info_collection_name = None

work_env = os.getenv("WORK_ENV")
if song_collection_name is None and song_info_collection_name is None:
    if work_env == "development":
        os.environ['SONG_INFO_COLLECTION'] = f"{os.getenv('SONG_INFO_COLLECTION')}-test"
        os.environ['SONG_COLLECTION'] = f"{os.getenv('SONG_COLLECTION')}-test"

    song_collection_name = os.getenv("SONG_COLLECTION")
    song_info_collection_name = os.getenv("SONG_INFO_COLLECTION")
