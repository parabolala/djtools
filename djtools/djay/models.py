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
from typing import Optional, Set
import dataclasses

from bpylist import archiver
from bpylist.archive_types import DataclassArchiver


class Error(Exception):
    pass


@dataclasses.dataclass
class ADCMediaItemTitleID(DataclassArchiver):
    title: str = ""
    artist: str = ""
    stringRepresentation: str = ""
    internalID: str = ""
    duration: float = 0
    uuid: str = ""


@dataclasses.dataclass
class ADCCuePoint(DataclassArchiver):
    comment: Optional[str] = None
    number: int = 0
    time: float = 0

    @staticmethod
    def encode_archive(obj, archive):
        if not obj.comment:
            obj.comment = '{m}:{s:02d}'.format(
                m=int(obj.time) // 60,
                s=int(obj.time) % 60)
        return DataclassArchiver.encode_archive(obj, archive)


@dataclasses.dataclass
class ADCMediaItemUserData(DataclassArchiver):
    cuePoints: list = dataclasses.field(default_factory=list)
    endPoint: Optional[ADCCuePoint] = None
    energy: float = 0  # ?
    highEQ: float = 0
    midEQ: float = 0
    lowEQ: float = 0
    linkedUserDataUUIDs: list = dataclasses.field(default_factory=list)
    loopRegions: list = dataclasses.field(default_factory=list)
    manualBPM: float = 0
    manualBeatTime: float = 0
    manualFirstDownBeatIndices: list = dataclasses.field(default_factory=list)
    manualGridStartPoints: list = dataclasses.field(default_factory=list)
    manualKeySignatureIndex: int = 0
    playCount: int = 0
    rating: int = 0
    startPoint: Optional[ADCCuePoint] = None
    tagUUIDs: list = dataclasses.field(default_factory=list)
    uuid: str = ""
    userChangedCloudKeys: Set[str] = dataclasses.field(default_factory=set)


@dataclasses.dataclass
class ADCMediaItemAnalyzedData(DataclassArchiver):
    bpm: float = 0
    keySignatureIndex: int = 0
    uuid: str = ""


@dataclasses.dataclass(frozen=True)
class NSURL(DataclassArchiver):
    NSrelative: str = ""
    NSbase: str = ""


@dataclasses.dataclass
class ADCMediaItemLocation(DataclassArchiver):
    sourceURIs: Set[NSURL] = dataclasses.field(default_factory=set)
    type: int = 0
    urlBookmarkData: bytes = b""
    uuid: str = ""


@dataclasses.dataclass(frozen=True)
class NSMutableData(DataclassArchiver):
    NSdata: Optional[bytes] = None

    def __repr__(self):
        return "NSMutableData(%s bytes)" % (
            'null' if self.NSdata is None else len(self.NSdata))


@dataclasses.dataclass
class ADCProduct(DataclassArchiver):
    useCount: int = 0
    uuid: str = ""
    firstUseDate: float = 0
    lastUseDate: float = 0
    deviceOSVersion: str = ""
    deviceType: str = ""
    version: str = ""
    productID: str = ""


@dataclasses.dataclass
class ADCMediaItem(DataclassArchiver):
    addedDate: float
    albumArtistUUIDs: str
    albumDiscCount: int
    albumDiscNumber: int
    albumTrackCount: int
    albumTrackNumber: int
    albumType: int
    albumUUID: str
    bitRate: int
    bpm: float
    channelCount: int
    comments: str
    composer: str
    contentType: str
    drmProtected: bool
    duration: float
    explicitContent: bool
    grouping: str
    keySignatureIndex: int
    labelUUID: str
    lyrics: str
    modifiedDate: float
    originSourceID: str
    purchasedDate: float
    releaseDate: float
    sampleRate: int
    title: str
    titleID: str
    uuid: str
    year: int
    artistUUIDs: Set[str] = dataclasses.field(default_factory=set)
    genreUUIDs: Set[str] = dataclasses.field(default_factory=set)


class NSOrderedSetArchiver:
    "Delegate for packing/unpacking NS(Mutable)Array objects"

    @staticmethod
    def decode_archive(archive):
        res = []
        i = 0
        while True:
            obj = archive.decode('NS.object.%d' % i)
            if obj:
                res.append(obj)
            else:
                break
            i += 1
        return res


@dataclasses.dataclass
class DjayTrack:
    title: ADCMediaItemTitleID
    user_data: Optional[ADCMediaItemUserData] = None
    local_location: Optional[ADCMediaItemLocation] = None
    global_location: Optional[ADCMediaItemLocation] = None
    analysis: Optional[ADCMediaItemAnalyzedData] = None
    media_item: Optional[ADCMediaItem] = None


def register():
    for dataclass in [
            ADCCuePoint,
            ADCMediaItem,
            ADCMediaItemAnalyzedData,
            ADCMediaItemLocation,
            ADCMediaItemTitleID,
            ADCMediaItemUserData,
            NSMutableData,
            NSURL,
            ADCProduct,
    ]:
        archiver.update_class_map(
            {dataclass.__name__: dataclass}
        )
    archiver.update_class_map({
        'NSOrderedSet': NSOrderedSetArchiver,
    })
