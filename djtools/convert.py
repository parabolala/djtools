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
import copy

from djtools.djay import models as djaymodels
from djtools.rekordbox import models as rbmodels


def transfer_cue_points(rb_t: rbmodels.Track,
                        dj_t: djaymodels.DjayTrack) -> djaymodels.DjayTrack:
    result = copy.deepcopy(dj_t)
    if result.user_data is None:
        result.user_data = djaymodels.ADCMediaItemUserData()
    result.user_data.cuePoints = []
    for i, cp in enumerate(rb_t.CuePoints):
        result.user_data.cuePoints.append(djaymodels.ADCCuePoint(
            comment=cp.Name,
            number=i + 1,
            time=cp.Start,
        ))
    return result
