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
# pylint: disable=unused-import
from typing import Dict, Iterable  # noqa: F401
# pylint: enable=unused-import
import xml.etree.ElementTree as ET

import dataclasses

DEFAULT_PATH = os.getenv('HOME', '') + "/Documents/rekordbox.xml"


@dataclasses.dataclass
class Track:
    TrackID: int
    Name: str
    Artist: str
    Album: str
    TotalTime: int
    Location: str
    CuePoints: list = dataclasses.field(default_factory=list)

    @classmethod
    def parse(cls, track: ET.Element):
        field_values = {}  # type: Dict[str, object]
        for field in dataclasses.fields(cls):
            field_value = track.get(field.name)
            if field_value is not None:
                field_value = field.type(field_value)
            field_values[field.name] = field_value

        cps = []
        for mark in track.findall('POSITION_MARK'):
            cps.append(CuePoint.parse(mark))
        field_values['CuePoints'] = cps
        return cls(**field_values)  # type: ignore


@dataclasses.dataclass
class CuePoint:
    Name: str = ""
    Type: int = 0
    Start: float = 0
    Num: int = 0
    Red: int = 255
    Green: int = 255
    Blue: int = 255

    @classmethod
    def parse(cls, position_mark: ET.Element):
        field_values = {}
        for field in dataclasses.fields(cls):
            field_value = position_mark.get(field.name)
            if field_value is not None:
                field_value = field.type(field_value)
            field_values[field.name] = field_value
        return cls(**field_values)  # type: ignore


def parse_dj_collection(dj_collection: ET.Element) -> Iterable[Track]:
    collection = []
    tracks = dj_collection.find('COLLECTION')
    if tracks:
        for track in tracks:
            collection.append(Track.parse(track))
    return collection


def parse_xml_file(file_path: str = DEFAULT_PATH) -> Iterable[Track]:
    tree = ET.parse(file_path)
    root = tree.getroot()
    return parse_dj_collection(root)
