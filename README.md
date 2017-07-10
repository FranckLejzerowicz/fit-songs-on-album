# plan_album
Give you songs durations and get possibilities for how they fit on a vinyl album (33 or 45 rmp; 7, 10 or 12')

This script would help loose music bands without the help of a major label and thus house that would like to decide for themselves how to fit their songs on a vinyl of a given time space in order to release an LP or EP. Hope that helps!

## Usage
```
usage: plan_album.py [-h] -songs [SONGS [SONGS ...]]
                     [-vinyl [VINYL [VINYL ...]]] -durations
                     [DURATIONS [DURATIONS ...]] [-min [MIN]] [-max [MAX]]
                     -out OUT [-waste [WASTE]] [-must [MUST [MUST ...]]]
                     [-sep [SEP]]
```


### Optional arguments
```
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

#### Example

Let's say my band is called **Deftones** and I want to release an album of 9 songs that I will call **Around the fur** :)
The songs and their durations are the following:
- My Own Summer Shove It [3:35] ---> as parentheses are not allowed I changed the original name "My Own Summer (Shove It)"
- Lhabia [4:11]
- Mascara [3:45]
- Around the Fur [3:31]
- Rickets [2:42]
- Be Quiet and Drive Far Away [5:08] ---> as parentheses are not allowed I changed the original name "Be Quiet and Drive (Far Away)"
- Lotion [3:57]
- Dai the Flu [4:36]
- Headup [6:13]

If I do this command:
```
python2.7 plan_album.py -songs My Own Summer Shove It,,, Lhabia,,, Mascara,,, Around the Fur,,, Rickets,,, Be Quiet and Drive Far Away,,, Lotion,,,Dai the Flu,,, Headup -durations 3:35 4:11 3:45 3:31 2:42 5:08 3:57 4:36 6:13 -out Around_the_fur.txt+
```
It will map the songs to their durations in the input orders (options ```-songs``` and ```-durations```) and ask you to confirm you want to search for these vinyl album formats (according to what has been entered to ```-vinyl```):
 - 33 RPM / 7' [14 minutes - 7/side]
 - 33 RPM / 10' [26 minutes - 13/side]
 - 33 RPM / 12' [42 minutes - 21/side]
 - 45 RPM / 10' [20 minutes - 10/side]
 - 45 RPM / 12' [30 minutes - 15/side]

The ```-out``` option is compulsory and the output file name could logically be the albun name (here Around_the_fur.txt+). You noticed the ```+``` at the end of the file name: this specifies the script to ouptut one file per vinyl format (because there could be a lot of combinations). The algorithm is brute force - no fancy heuristic to solve this problem :)

The result here is that the Deftones songs only fit on a 33 RPM / 12' vinyl, and I bet it does!

#### Requirements
Python2.7
