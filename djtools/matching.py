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
from typing import Iterable, Optional

from djtools.djay import models as djaymodels
from djtools.rekordbox import models as rbmodels


def duration_matches(dj_t: djaymodels.DjayTrack, rb_t: rbmodels.Track) -> bool:
    return abs(dj_t.title.duration - rb_t.TotalTime) < 1


def title_matches(dj_t: djaymodels.DjayTrack, rb_t: rbmodels.Track) -> bool:
    if dj_t.title.title != rb_t.Name:
        return False
    if dj_t.title.artist != rb_t.Artist:
        return False
    if abs(dj_t.title.duration - rb_t.TotalTime) > 1:
        return False
    return True


def find_matching_track(
        dj_t: djaymodels.DjayTrack,
        rb_ts: Iterable[rbmodels.Track]) -> Optional[rbmodels.Track]:
    candidates = list(filter(lambda rb_t: duration_matches(dj_t, rb_t), rb_ts))
    if not candidates:
        return None

    if len(candidates) == 1:
        return candidates[0]

    candidates = list(filter(lambda rb_t: title_matches(dj_t, rb_t),
                             candidates))
    if candidates:
        return candidates[0]
    return None
