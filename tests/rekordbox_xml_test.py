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
import xml.etree.ElementTree as ET

from djtools import rekordbox
from djtools.rekordbox import models

FIXTURES_DIR = os.path.join(
        os.path.dirname(__file__), 'fixtures', 'rekordbox')


def get_fixture_path(fixture_name):
    return os.path.join(FIXTURES_DIR, fixture_name)

def get_fixture_root(fixture_name):
    tree = ET.parse(get_fixture_path(fixture_name))
    return tree.getroot()


class TestParseXML(unittest.TestCase):
  def test_parse_cue_point(self):
    expected = [
        models.CuePoint(Num=0, Start=1.444, Red=230, Blue=40, Green=40),
        models.CuePoint(Num=1, Start=12.098, Red=40, Blue=20, Green=226),
        models.CuePoint(Num=2, Start=172.113, Red=230, Blue=40, Green=40),
        models.CuePoint(Num=3, Start=182.814, Red=40, Blue=20, Green=226),
    ]

    root = get_fixture_root('cuepoint.xml')
    actual = [models.CuePoint.parse(cp) for cp in root.findall('POSITION_MARK')]
    self.assertEqual(actual, expected)

  def test_parse_xml(self):
    expected = [
        models.Track(
            TrackID=5, Name="Foo", Artist="Bar", Album="",
            TotalTime=214, Location="file://localhost/foobarbaz.mp3",
            CuePoints=[
                models.CuePoint(Num=0, Start=1.444, Red=230, Blue=40, Green=40),
                models.CuePoint(Num=1, Start=12.098, Red=40, Blue=20, Green=226),
                models.CuePoint(Num=2, Start=172.113, Red=230, Blue=40, Green=40),
                models.CuePoint(Num=3, Start=182.814, Red=40, Blue=20, Green=226),
            ],
        ),
    ]

    actual = rekordbox.parse_xml_file(get_fixture_path('rekordbox.xml'))
    self.assertEqual(actual, expected)



if __name__ == '__main__':
    unittest.main()
