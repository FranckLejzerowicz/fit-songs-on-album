#!/usr/bin/env python

import itertools
import argparse

__author__ = "Franck Lejzerowicz"
__copyright__ = "Copyright 2017, The Deep-Sea Microbiome Project"
__credits__ = ["Yoann Dufresne", "Jan Pawlowski"]
__license__ = "GPL V3"
__version__ = "1.0"
__maintainer__ = "Franck Lejzerowicz"
__email__ = "franck.lejzerowicz@unige.ch"

def fit_songs_on_album_():
    parser=argparse.ArgumentParser()
    parser.add_argument('-songs', nargs = '*', required = True, help="Songs names in arbitrary order (',,,'-separated, yes three comas in order to allow song names written with more than one word... but you can choose another separator with -sep).")
    parser.add_argument('-vinyl', nargs = '*', default = 0, help="Vinyl format to try: [1] 33 RPM / 12' (42 min), [2] 33 RPM / 10' (26 min), [3] 33 RPM / 7' (14 min), [4] 45 RPM / 12' (30 min), [5] 45 RPM / 10' (20 min) - (default: 1 2 3 4 5)")
    parser.add_argument('-durations', nargs = '*', required = True, help="Songs durations in 'minutes:seconds' (e.g. ) or in 'minutes' (e.g. 4.89 2.99).")
    parser.add_argument('-min', nargs = '?', type = int, default = 0, help="Minimum number of songs to release on the album (if missing and -max missing: all songs.")
    parser.add_argument('-max', nargs = '?', type = int, default = 0, help="Maximum number of songs to release on the album (if missing (i) and -min given: from min to all songs, (ii) and -min missing: just the max number.")
    parser.add_argument('-out', nargs = 1, required = True, help="Output file (add a '+' at the end of file name to have one file per vinyl format: if no possibily for a format -> no file).")
    parser.add_argument('-waste', nargs = '?', type = int, default = 0, help="Maximum allowed duration in seconds of no music on the total vinyl format duration, i.e. not per face (default: any duration)")
    parser.add_argument('-must', nargs = '*', default = [], help="The song(s) that must be released in the vinyl")
    parser.add_argument('-sep', nargs = '?', default = ',,,', help="Separator for the song names (default = ',,,')")
    parse=parser.parse_args()
    args=vars(parse)

    out = args['out'][0]
    mini = args['min']
    maxi = args['max']
    timeLeft = args['waste']
    mustHave = args['must']
    sep = args['sep']
    names = [x.strip() for x in ' '.join(args['songs']).split(sep)]
    print names
    durations = args['durations']
    vinyls = args['vinyl']
    D = {1: ["33 RPM / 12'", 42], 2: ["33 RPM / 10'", 26], 3: ["33 RPM / 7'", 14], 4: ["45 RPM / 12'", 30], 5: ["45 RPM / 10'", 20]}
    d = {}
    if vinyls:
        for i in vinyls:
            if i.isdigit() and D.has_key(int(i)):
                d[D[int(i)][0]] = D[int(i)][1]
            else:
                print 'Wrong vinyl type entries...\nExiting :('
                return -1
    else:
        for i in D:
            d[D[int(i)][0]] = D[int(i)][1]

    dOrd = sorted(d, key=lambda x: (int(x[:2]), int(x[-3:-1])))

    songs = get_songs_durations(names, durations)
    if songs:
        print
        print 'Songs to search for %s' % out
        for i in sorted(songs):
            print '- %s [%s]' % (i, dec_to_sec(songs[i]))
        if mustHave:
            for must in mustHave:
                if must not in songs.keys():
                    print "%s not in the list of songs\nI'm stopping here!" % must
                    return -1
        if mini:
            if maxi:
                N = range(mini, (maxi+1))
            else:
                N = range(mini, len(songs)+1)
        else:
            if maxi:
                N = [maxi]
            else:
                N = [len(songs)]
        print
        print 'Looking in these kinds of vinyl formats:'
        for i in dOrd:
            print '  -', i, '[%s minutes - %s/side]' % (d[i], d[i]/2)
        choice = raw_input('Continue? <y/n>')
        if choice or choice.lower().startswith('n'):
            return -1
        outputs, possib = make_choices(dOrd, d, songs, N, timeLeft, mustHave, out)

        print
        print '-------'
        print 'Outputs'
        print '-------'
        for output in outputs:
            if output == out:
                filou = out
                thresh = (4 * len(dOrd))+(4 * len(N) * len(dOrd))
            else:
                filou = '%s_%s' % (output.replace("'", "").replace(' ', '_').replace('_/_','-'), out[:-1])
                thresh = 4 + (4 * len(N))
            print '-',filou,'->',
            if len(outputs[output]) > thresh:
                if possib[output]==1:
                    print possib[output], 'possibility'
                else:
                    print possib[output], 'possibilities'
                o=open(filou, 'w')
                for line in outputs[output]:
                    o.write(line)
                o.close()
            else:
                print '0 possibility'


def get_songs_durations(names, durations):
    songs = {}
    if len(names) != len(durations):
        print 'Not the same number of songs and durations...\nBye bye'
        return 0
    for idx, i in enumerate(names):
        songs[i] = make_duration(durations[idx])
    return songs

def make_duration(duration):
    if ':' in duration:
        m = duration.split(':')[0]
        s = duration.split(':')[1]
        if m.isdigit() and s.isdigit():
            duration = ((int(m)*60)+int(s))/60.
    elif '.' in duration:
        m = duration.split('.')[0]
        s = duration.split('.')[1]
        if m.isdigit() and s.isdigit():
            duration = float(duration)
    else:
        duration = int(duration)
    return duration


def dec_to_sec(tim):
    if '.' in str(tim):
        m = str(tim).split('.')[0]
        dec = str(tim).split('.')[1]
        sec = 60 * float('0.%s' % dec)
        if sec<10:
            m_s = '%s:0%s' % (m, int(round(sec, 0)))
        else:
            m_s = '%s:%s' % (m, int(round(sec, 0)))
    else:
        return tim
    return m_s

def make_choices(dOrd, d, songs, N, timeLeft, mustHave, out):
    toWrite = {}
    possib = {}
    if out[-1] != '+':
        toWrite[out] = []
        possib[out] = 0
        key = out
    for i in dOrd:
        vinylDuration = d[i]
        halfDuration = vinylDuration / 2
        if out[-1] == '+':
            key = i
            toWrite[key] = []
            possib[key] = 0
        toWrite[key].append('********************\n')
        toWrite[key].append('FORMAT: %s\n' % i)
        toWrite[key].append('Total duration = %s\n' % vinylDuration)
        toWrite[key].append('********************\n')
        print
        print '********************'
        print 'FORMAT:', i
        print 'Total duration =', vinylDuration
        print '********************'
        for nombreChansons in N:
            C = 0
            toWrite[key].append('\n==========\n')
            toWrite[key].append('%s songs\n' % nombreChansons)
            toWrite[key].append('==========\n\n')
            print
            print '=========='
            print '%s songs' % nombreChansons
            print '=========='
            print
            c = 0
            ctrl = {}
            for listChansons in itertools.combinations(songs.keys(), nombreChansons):
                listDuration = sum([songs[x] for x in listChansons])
                if listDuration <= vinylDuration:
                    diff = vinylDuration - listDuration
                    secLeft = round(diff*60, 2)
                    if timeLeft and secLeft > timeLeft:
                        continue
                    curSongs = sorted(listChansons)
                    all_less_than_face_duration = []
                    for r in range(1, len(listChansons)):
                        for new_listChansons in itertools.combinations(listChansons, r):
                            new_listDuration = sum([songs[x] for x in new_listChansons])
                            if new_listDuration <= halfDuration:
                                all_less_than_face_duration.append(new_listChansons)
                        for faces in itertools.combinations(all_less_than_face_duration, 2):
                            allSongs = []
                            for faceSongs in faces:
                                for currSong in faceSongs:
                                    allSongs.append(currSong)
                            if sorted(allSongs)==curSongs:
                                A= '_'.join(faces[0])
                                B= '_'.join(faces[1])
                                AB = '+'.join(sorted([A,B]))
                                if ctrl.has_key(AB):
                                    continue
                                else:
                                    ctrl[AB] = 1
                                for fdx, face in enumerate(faces):
                                    faceSum = sum([songs[x] for x in face])
                                if faceSum > halfDuration:
                                    continue
                                if mustHave:
                                    if sorted(list(set(allSongs)&set(mustHave))) != sorted(mustHave):
                                        continue
                                C+=1
                                c+=1
                                possib[key]+=1
                                toWrite[key].append('#%s\n' % c)
                                print '#%s' % c
                                for fdx, face in enumerate(faces):
                                    faceSum = sum([songs[x] for x in face])
                                    if fdx == 0:
                                        toWrite[key].append('- Side A [Total=%s, No music=%s]\n' % (dec_to_sec(faceSum), dec_to_sec(halfDuration-faceSum)))
                                        print '- Side A [Total=%s, No music=%s]:' % (dec_to_sec(faceSum), dec_to_sec(halfDuration-faceSum))
                                    else:
                                        toWrite[key].append('- Side B [Total=%s, No music=%s]\n' % (dec_to_sec(faceSum), dec_to_sec(halfDuration-faceSum)))
                                        print '- Side B [Total=%s, No music=%s]:' % (dec_to_sec(faceSum), dec_to_sec(halfDuration-faceSum))
                                    for x in face:
                                        toWrite[key].append('\t%s [%s]\n' % (x, dec_to_sec(songs[x])))
                                        print '   *', x, '[%s]' % dec_to_sec(songs[x])
                                    print '---------------------------------'
            if C == 0:
                toWrite[key].append('Not possible!!!\n')
    return toWrite, possib

fit_songs_on_album_()
