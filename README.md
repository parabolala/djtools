# DJ Tools

The project contains a set of libraries for reading, writing and converting
media library information between different DJ Software applications.

# Features

  * Algoriddim djay Pro 2: read and parse library. Limited writing.
  * Rekordbox: read explorted XML library.

  * Conversion:
    * Convert cue points from Rekordbox XML format to matching tracks in djay Pro 2 library.

# Installing

```
$ pip install Djtools

# Tests
$ pip install Djtools[test]
$ nosetests
```

# Usage

```
>>> # Explore djay Pro 2 database.
>>> from djtools.djay import Explorer
>>> e = Explorer()
>>> track = e.get_all_tracks()[0]
>>> print('{} - {}'.format(track.title.artist, track.title.title))

>>> # Parse rekordbox XML library.
>>> from djtools import rekordbox, matching, convert
>>> rbts = rekordbox.parse_xml_file()
>>> print(rbts[0].Artist, rbts[0].Name)

>>> # Transfer cue points from rekordbox XML library to matching tracks in djay Pro 2.
>>> for dj_t in e.get_all_tracks():
>>>     print('Djay track: ' + dj_t.title.artist + ' - ' + dj_t.title.title)
>>>     match = matching.find_matching_track(dj_t, rbts)
>>>     if match is not None:
>>>         result = convert.transfer_cue_points(match, dj_t)
>>>         if result.user_data and result.user_data.cuePoints:
>>>             print(f"Transferred {len(result.user_data.cuePoints)} cue points.")
>>>         else:
>>>             print("No cue points in RB track")
>>>         e.save_track(result)
>>>     else:
>>>         print("No matching track in RB")
>>>     print('===')
```

# Disclaimer

This is not an officially supported Google product.
