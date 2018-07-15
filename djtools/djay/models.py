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
from typing import Set
import dataclasses

from bpylist import archiver


class Error(Exception):
    pass

def verify_dataclass_has_fields(dataclass, plist_obj):
    dataclass_fields = dataclasses.fields(dataclass)

    skip_fields = {'$class'}

    fields_to_verify = plist_obj.keys() - skip_fields
    fields_with_no_dots = {(f if not f.startswith('NS.') else 'NS' + f[3:])
        for f in fields_to_verify}
    unmapped_fields = fields_with_no_dots - {f.name for f in dataclass_fields}
    if unmapped_fields:
        raise Error(
            f"Unmapped fields: {unmapped_fields} for class {dataclass}")


class DataclassArchiver:
    def encode_archive(self, archive):
        for field in dataclasses.fields(type(self)):
            archive_field_name = field.name
            if archive_field_name[:2] == 'NS':
              archive_field_name = 'NS.' + archive_field_name[2:]
            archive.encode(archive_field_name, getattr(self, field.name))

    @classmethod
    def decode_archive(cls, archive):
        verify_dataclass_has_fields(cls, archive._object)
        field_values = {}
        for field in dataclasses.fields(cls):
            archive_field_name = field.name
            if archive_field_name[:2] == 'NS':
              archive_field_name = 'NS.' + archive_field_name[2:]
            value = archive.decode(archive_field_name)
            if isinstance(value, bytearray):
              value = bytes(value)
            field_values[field.name] = value
        return cls(**field_values)

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
    comment: str = None
    number: int = 0
    time: float = 0


@dataclasses.dataclass
class ADCMediaItemUserData(DataclassArchiver):
    cuePoints: list = dataclasses.field(default_factory=list)
    endPoint: ADCCuePoint = None
    energy: float = 0 # ?
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
    startPoint: ADCCuePoint = None
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
    urlBookmarkData: bytes = ""
    uuid: str = ""


@dataclasses.dataclass(frozen=True)
class NSMutableData(DataclassArchiver):
    NSdata: bytes = None

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
    global_location: ADCMediaItemLocation
    user_data: ADCMediaItemUserData = None
    local_location: ADCMediaItemLocation = None
    global_location: ADCMediaItemLocation = None
    analysis: ADCMediaItemAnalyzedData = None
    media_item: ADCMediaItem = None


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
                {dataclass.__name__: dataclass }
        )
    archiver.update_class_map({
        'NSOrderedSet': NSOrderedSetArchiver,
    })
