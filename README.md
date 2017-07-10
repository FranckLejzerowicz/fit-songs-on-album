# fit-songs-on-album
Give you songs durations and get possibilities for how they fit on a vinyl album (33 or 45 rmp; 7, 10 or 12')

## Usage
```
usage: plan_album.py [-h] -songs [SONGS [SONGS ...]]
                     [-vinyl [VINYL [VINYL ...]]] -durations
                     [DURATIONS [DURATIONS ...]] [-min [MIN]] [-max [MAX]]
                     -out OUT [-waste [WASTE]] [-must [MUST [MUST ...]]]
                     [-sep [SEP]]

```

### Optional arguments

  -h, --help            show help message and exit
  -songs [SONGS [SONGS ...]]
                        Songs names in arbitrary order (',,,'-separated, yes
                        three comas in order to allow song names written with
                        more than one word... but you can choose another
                        separator with -sep).
  -vinyl [VINYL [VINYL ...]]
                        Vinyl format to try: [1] 33 RPM / 12' (42 min), [2] 33
                        RPM / 10' (26 min), [3] 33 RPM / 7' (14 min), [4] 45
                        RPM / 12' (30 min), [5] 45 RPM / 10' (20 min) -
                        (default: 1 2 3 4 5)
  -durations [DURATIONS [DURATIONS ...]]
                        Songs durations in 'minutes:seconds' (e.g. ) or in
                        'minutes' (e.g. 4.89 2.99).
  -min [MIN]            Minimum number of songs to release on the album (if
                        missing and -max missing: all songs.
  -max [MAX]            Maximum number of songs to release on the album (if
                        missing (i) and -min given: from min to all songs,
                        (ii) and -min missing: just the max number.
  -out OUT              Output file (add a '+' at the end of file name to have
                        one file per vinyl format: if no possibily for a
                        format -> no file).
  -waste [WASTE]        Maximum allowed duration in seconds of no music on the
                        total vinyl format duration, i.e. not per face
                        (default: any duration)
  -must [MUST [MUST ...]]
                        The song(s) that must be released in the vinyl
  -sep [SEP]            Separator for the song names (default = ',,,')
  ```

#### Requirements
Python2.7
