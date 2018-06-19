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
import unittest
import sqlite3
import tempfile


from djtools.djay import models, explorer, Explorer

from .common import dj_tests


INSERT_QUERY = (
        'INSERT INTO database2(rowid, collection, key, data, metadata)'
        ' VALUES (?,?,?,?,?)'
)

def get_fixture_schema():
    fname = os.path.join(dj_tests.XML_FIXTURES_DIR, 'schema.sql')
    with open(fname, 'r', encoding='utf-8') as f:
        return f.read()


def data_fixture_row(collection, key, data_xml):
    data = dj_tests.get_fixture_from_xml(data_xml)
    ExplorerTest.rowid += 1
    return (ExplorerTest.rowid-1, collection, key, data, None)

class ExplorerTest(unittest.TestCase):
    rowid = 1

    def setUp(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            self.db_fname = f.name
        schema_sql = get_fixture_schema()

        self.db = sqlite3.connect(self.db_fname)
        with self.db:
            self.db.execute(schema_sql)
            for row in [
                    data_fixture_row('products',
                                     'com.algoriddim.direct.djay-pro-2-mac-Mac',
                                     'product.xml'),
            ]:
                self.db.execute(INSERT_QUERY, row)
        self.e = Explorer(self.db_fname)

    def tearDown(self):
        os.unlink(self.db_fname)

    def test_load(self):
        self.assertTrue(self.e.data)

    def test_load_bad_version(self):
        with self.db:
            self.db.execute('delete from database2 where collection="products"')
            for row in [data_fixture_row(
                    'products', 'com.algoriddim.direct.djay-pro-2-mac-Mac',
                    'product_bad_version.xml'),
            ]:
                self.db.execute(INSERT_QUERY, row)
        with self.assertRaises(explorer.BadDataFormatError):
            Explorer(self.db_fname).data

    def test_get_track_ids(self):
        expected_track_ids = ['foo', 'bar', 'baz']
        with self.db:
            for row in [data_fixture_row('mediaItemTitleIDs', track_id, '/dev/null')
                    for track_id in expected_track_ids]:
                self.db.execute(INSERT_QUERY, row)
                self.rowid += 1

        self.e.load()
        self.assertEqual(expected_track_ids, self.e.get_track_ids())

    def _populate_track(self):
        track_id = dj_tests.EXPECTED_TITLE.uuid
        with self.db:
            for table, data in [
                    ('mediaItemUserData', 'userdata.plist.xml'),
                    ('mediaItemTitleIDs', 'adctitle.plist.xml'),
                    ('mediaItemAnalyzedData', 'analyzed_data.plist.xml'),
                    ('localMediaItemLocations', 'location.plist.xml'),
                ]:
                row = data_fixture_row(table, track_id, data)
                self.db.execute(INSERT_QUERY, row)
        self.e.load()
        return models.DjayTrack(
            title=dj_tests.EXPECTED_TITLE,
            user_data=dj_tests.EXPECTED_USER_DATA,
            analysis=dj_tests.EXPECTED_ANALYZED_DATA,
            local_location=dj_tests.EXPECTED_MEDIA_ITEM_LOCATION,
        )

    def test_load_track(self):
        expected_track = self._populate_track()
        track_id = expected_track.title.uuid

        self.assertEqual(self.e.load_track(track_id), expected_track)

    def test_find_track(self):
        expected_track = self._populate_track()
        track_id = expected_track.title.uuid

        self.assertEqual(self.e.find_track(track_id=track_id), expected_track)
        self.assertEqual(self.e.find_track(artist=expected_track.title.artist),
                         expected_track)
        self.assertEqual(self.e.find_track(title=expected_track.title.title),
                         expected_track)
        self.assertEqual(
                self.e.find_track(duration=expected_track.title.duration),
                expected_track)

        with self.assertRaises(explorer.Error):
            self.e.find_track(duration=5)

    def test_save_track(self):
        expected_track = self._populate_track()
        track_id = expected_track.title.uuid

        old_duration = expected_track.title.duration

        self.assertEqual(self.e.find_track(track_id=track_id).title.duration,
                         old_duration)

        expected_track.title.duration += 5
        self.e.save_track(expected_track)

        self.assertEqual(self.e.find_track(track_id=track_id).title.duration,
                         old_duration + 5)

    def test_get_all_tracks(self):
        expected_track = self._populate_track()

        all_tracks = self.e.get_all_tracks()
        self.assertEqual(len(all_tracks), 1)
        self.assertEqual(all_tracks[0], expected_track)


if __name__ == '__main__':
    unittest.main()
