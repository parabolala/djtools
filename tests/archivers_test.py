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
import unittest

from bpylist import archiver

from djtools.djay import models

from .common import dj_tests


class TestArchivers(unittest.TestCase):
    def setUp(self):
        models.register()

    def test_verify_dataclass_has_fields(self):
        with self.assertRaises(models.Error):
            bplist = dj_tests.get_fixture_from_xml('cuepoint_extra_field.plist.xml')
            archiver.unarchive(bplist)

    def test_title_unarchive(self):
        bplist = dj_tests.get_fixture_from_xml('adctitle.plist.xml')
        expected = dj_tests.EXPECTED_TITLE
        actual = archiver.unarchive(bplist)
        self.assertEqual(actual, expected)

    def test_title_e2e(self):
        expected = models.ADCMediaItemTitleID(
            title='title',
            artist='artist',
            uuid='UuId',
            internalID='UuId',
            stringRepresentation='String Repr',
            duration=15.3,
        )
        actual = archiver.unarchive(archiver.archive(expected))
        self.assertEqual(actual, expected)

    def test_cuepoint_unarchive(self):
        bplist = dj_tests.get_fixture_from_xml('cuepoint.plist.xml')
        expected = dj_tests.EXPECTED_CUEPOINT
        actual = archiver.unarchive(bplist)
        self.assertEqual(actual, expected)

    def test_cuepoint_e2e(self):
        expected = models.ADCCuePoint(
            comment="bar",
            number=2,
            time=15.2,
        )
        actual = archiver.unarchive(archiver.archive(expected))
        self.assertEqual(actual, expected)

    def test_userdata_unarchive(self):
        bplist = dj_tests.get_fixture_from_xml('userdata.plist.xml')
        expected = dj_tests.EXPECTED_USER_DATA
        actual = archiver.unarchive(bplist)
        self.assertEqual(actual, expected, f'\n{actual} != \n{expected}')

    def test_userdata_e2e(self):
        expected = models.ADCMediaItemUserData(
            cuePoints=[
                models.ADCCuePoint(comment=None, number=1,
                                   time=3.2826459407806396),
                models.ADCCuePoint(comment=None, number=2,
                                   time=114.29496765136719),
                models.ADCCuePoint(comment=None, number=3,
                                   time=114.83682250976562)
            ],
            startPoint=models.ADCCuePoint(comment=None, number=0,
                                   time=112.90266418457031),
            uuid='71f9ccc746630c592ceeed39cbc837b2',
            playCount=7,
            energy=15,
            highEQ=10.30,
            midEQ=2.0,
            lowEQ=3.0,
            manualBPM=117.33,
            manualBeatTime=1.01,
            manualKeySignatureIndex=7,
            rating=3,
            # TODO: Populate the fields.
            linkedUserDataUUIDs=None,
            loopRegions=None,
            manualFirstDownBeatIndices=None,
            manualGridStartPoints=None,
            tagUUIDs=None,
            endPoint=None,
        )
        actual = archiver.unarchive(archiver.archive(expected))
        self.assertEqual(actual, expected)

    def test_analyzed_data_unarchive(self):
        bplist = dj_tests.get_fixture_from_xml('analyzed_data.plist.xml')
        expected = dj_tests.EXPECTED_ANALYZED_DATA
        actual = archiver.unarchive(bplist)
        self.assertEqual(actual, expected)

    def test_analyzed_data_e2e(self):
        expected = models.ADCMediaItemAnalyzedData(
                bpm=1,
                keySignatureIndex=10,
                uuid="foo",
        )
        actual = archiver.unarchive(archiver.archive(expected))
        self.assertEqual(actual, expected)

    def test_location_unarchive(self):
        bplist = dj_tests.get_fixture_from_xml('location.plist.xml')
        expected = dj_tests.EXPECTED_MEDIA_ITEM_LOCATION
        actual = archiver.unarchive(bplist)
        self.assertEqual(actual, expected)

    def test_location_e2e(self):
        expected = models.ADCMediaItemLocation(
            sourceURIs={
                models.NSURL(
                    NSrelative='file:///tmp/foo.wav',
                    NSbase=None
                ),
                models.NSURL(
                    NSrelative='com.apple.iTunes:123456',
                    NSbase=None
                )
            },
            type=3,
            urlBookmarkData=models.NSMutableData(
                NSdata=b'not a b64-encoded string'
            ),
            uuid='71f9'
        )
        actual = archiver.unarchive(archiver.archive(expected))
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
