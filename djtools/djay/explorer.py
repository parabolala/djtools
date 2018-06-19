# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import sqlite3
from typing import Tuple, List
from bpylist import archiver

from . import models


DEFAULT_MEDIALIBRARY_DB_FILE = ('/Users/yvaravva/Music/djay Pro 2/'
                                'djay Media Library.djayMediaLibrary/'
                                'MediaLibrary.db')


Row = Tuple[str, str, str, bytes, bytes]


class Error(Exception):
    pass

class BadDataFormatError(Error):
    pass

def is_supported_version(version_string):
    return version_string == '2.0.6'


class Explorer:
    _fname: bytes = None
    _query: str = "select rowid, collection, key, data, metadata from database2;"
    _data: List[Row] = None

    ROWID_COL, COLLECTION_COL, KEY_COL, DATA_COL, METADATA_COL = range(5)

    def __init__(self, medialibrary_db_fname: bytes=DEFAULT_MEDIALIBRARY_DB_FILE):
        self._fname = medialibrary_db_fname

    def load(self):
        models.register()
        if not os.path.exists(self._fname):
            raise Error(f"Media Library file not found: {self._fname}")
        data = []
        with sqlite3.connect(self._fname) as conn:
            for row in conn.execute(self._query):
                data.append(row)
        self._data = data
        self.verify_version()

    @property
    def data(self) -> List[Row]:
        if self._data is None:
            self.load()
        return self._data

    def get_rows(self, key: str=None, collection: str=None) -> List[Row]:
        results = []
        for row in self.data:
            if key is None or row[self.KEY_COL] == key:
                if collection is None or row[self.COLLECTION_COL] == collection:
                    results.append(row)
        return results

    def verify_version(self):
        products_rows = self.get_rows(
                collection='products',
                key='com.algoriddim.direct.djay-pro-2-mac-Mac',
        )
        if not products_rows:
            raise BadDataFormatError(
                    "Didn't find database row for collection=products. "
                    "Unsupported djay version?")
        products_row = products_rows[0]

        try:
            product = archiver.unarchive(products_row[-2])
        except Exception:
            raise

        if not is_supported_version(product.version):
            raise BadDataFormatError('Unsupported djay Pro 2 version: ' +
                                     product.version)

    def get_track_ids(self) -> List[str]:
        return [row[self.KEY_COL] for row in self.get_rows(collection='mediaItemTitleIDs')]

    def load_track(self, track_id: str):
        rows = self.get_rows(key=track_id)
        collection_to_field = {
            'mediaItemUserData': 'user_data',
            'mediaItemTitleIDs': 'title',
            'mediaItemAnalyzedData': 'analysis',
            'localMediaItemLocations': 'local_location',
            'globalMediaItemLocations': 'global_location',
            'mediaItems': 'media_item',
        }
        field_values = {}
        for row in rows:
            field_values[collection_to_field[row[self.COLLECTION_COL]]] = archiver.unarchive(row[self.DATA_COL])
        track = models.DjayTrack(**field_values)
        return track

    def find_track(self, track_id: str=None, artist: str=None, title: str=None, duration: float=None) -> models.DjayTrack:
        if all([track_id is None, artist is None, title is None, duration is None]):
            raise Error("At least one of track_id, artist, title are required")

        results = []
        for row in self.get_rows(collection='mediaItemTitleIDs'):
            if track_id is not None and row[self.KEY_COL] != track_id:
                continue
            title_obj = archiver.unarchive(row[self.DATA_COL])

            if artist is not None and title_obj.artist != artist:
                continue
            if title is not None and title_obj.title != title:
                continue
            if duration is not None and abs(title_obj.duration - duration) > .01:
                continue

            results.append(self.load_track(row[self.KEY_COL]))

        if not results:
            raise Error(f"Track not found for id={track_id} artist={artist} title={title} duration={duration}")

        if len(results) > 1:
            raise Error(f"More than one track matched: {results}")
        return results[0]

    def save_track(self, track: models.DjayTrack):
        self.validate_track(track)

        uuid = track.title.uuid
        rows = []
        rows.append(('mediaItemUserData', uuid, archiver.archive(track.user_data)))
        rows.append(('mediaItemTitleIDs', uuid, archiver.archive(track.title)))
        #rows.append(('localMediaItemLocations', uuid, archiver.archive(track.local_location)))
        if track.analysis is not None:
            rows.append(('mediaItemAnalyzedData', uuid,
                         archiver.archive(track.analysis)))

        query = 'UPDATE database2 set data=? WHERE collection=? AND key=?'
        with sqlite3.connect(self._fname) as conn:
            for row in rows:
                conn.execute(query, (row[2], row[0], row[1]))
        self.load()

    def validate_track(self, track):
        for field_name in ['analysis', 'local_location', 'global_location']:
            if getattr(track, field_name, None) is not None:
                if (track.title.uuid != getattr(track, field_name).uuid):
                    raise Error('Malformed track: title UUID (%s) doesn\'t '
                                'match %s UUID (%s)' % (
                                    track.title.uuid, field_name,
                                    getattr(track, field_name).uuid))
    def get_all_tracks(self):
        return [self.load_track(t_id) for t_id in self.get_track_ids()]
