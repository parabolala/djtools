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
import subprocess

from djtools.djay import models

XML_FIXTURES_DIR = os.path.join(
    os.path.dirname(__file__), '../fixtures', 'djay')


def get_fixture_from_xml(name):
    fname = os.path.join(XML_FIXTURES_DIR, name)
    with open(fname, 'rb') as f:
        fixture_xml = f.read()

    p = subprocess.Popen(
        'plutil -convert binary1 - -o -'.split(),
        stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, _ = p.communicate(fixture_xml)
    bplist_bytes = stdout
    return bplist_bytes


# The models below match the fixtures XML data.
EXPECTED_TITLE = models.ADCMediaItemTitleID(
    title='Title',
    artist='Artist',
    uuid='71f9ccc746630c592ceeed39cbc837b2',
    internalID='71f9ccc746630c592ceeed39cbc837b2',
    stringRepresentation='String Representation',
    duration=15.5,
)

EXPECTED_CUEPOINT = models.ADCCuePoint(
    comment="foo",
    number=3,
    time=15.1,
)

EXPECTED_USER_DATA = models.ADCMediaItemUserData(
    cuePoints=[
        models.ADCCuePoint(comment=None, number=1, time=3.2826459407806396),
        models.ADCCuePoint(comment=None, number=2, time=114.29496765136719),
        models.ADCCuePoint(comment=None, number=3, time=114.83682250976562)
    ],
    startPoint=models.ADCCuePoint(comment=None, number=0,
                                  time=112.90266418457031),
    uuid='71f9ccc746630c592ceeed39cbc837b2',
    playCount=7,
    # TODO: Populate the fields in fixture.
    linkedUserDataUUIDs=None,
    loopRegions=None,
    manualFirstDownBeatIndices=None,
    manualGridStartPoints=None,
    tagUUIDs=None,
    # endPoint=None,
    # energy=0,
    highEQ=0.0,
    midEQ=0.0,
    lowEQ=0.0,
    manualBPM=0.0,
    manualBeatTime=0.0,
    # manualKeySignatureIndex=0,
    # rating=0,
    userChangedCloudKeys=None,
)

EXPECTED_ANALYZED_DATA = models.ADCMediaItemAnalyzedData(
    bpm=109.99951171875,
    keySignatureIndex=21,
    uuid='71f9ccc746630c592ceeed39cbc837b2',
)

EXPECTED_MEDIA_ITEM_LOCATION = models.ADCMediaItemLocation(
    sourceURIs={
        models.NSURL(
            NSrelative='file:///Volumes/Foo/Contents/Bar/Baz/quux.mp3',
            NSbase=None,
        ),
        models.NSURL(
            NSrelative='com.apple.iTunes:7531193491163805027',
            NSbase=None,
        )
    },
    type=0,
    urlBookmarkData=models.NSMutableData(b'a b64-encoded string'),
    uuid='71f9ccc746630c592ceeed39cbc837b2'
)
