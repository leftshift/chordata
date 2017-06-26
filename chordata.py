#!/usr/bin/env python
# coding=utf-8

import argparse

from utils import (render, build_diff_dict, with_same_pattern, get_instrument,
                   get_chords, INSTRUMENT_CHOICES, FLATS_TO_SHARPS)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A dummy chordbook')
    parser.add_argument('chords', nargs='+')
    parser.add_argument('-i', '--instrument', dest='instrument',
                        choices=INSTRUMENT_CHOICES.keys(), default='mando',
                        help='instrument/tuning to show')
    parser.add_argument('-s', '--same-shapes', dest='same_shapes',
                        action='store_true', help='show chords w/ same shape')
    parser.add_argument('-a', '--all', dest='with_inversions',
                        action='store_true', help='show all chord inversions')
    parser.add_argument('-f', '--max-fingers', dest='max_fingers',
                        type=int, help='how many figers maximum you want to use')
    args = parser.parse_args()

    PADD = 10
    STRINGS, CHORDS = get_instrument(args.instrument)
    by_diff = build_diff_dict(CHORDS)

    for one in args.chords:
        matches = get_chords(STRINGS, CHORDS, one, args.max_fingers,
                             args.with_inversions, args.same_shapes)
        prev = ""

        for name, pattern in matches:
            name = '[ ' + name + ' ]'
            if name != prev:
                print('\n', name.center(40, '='))

            print(render(pattern, STRINGS))

            if args.same_shapes:
                shapes = with_same_pattern(pattern, by_diff)
                if shapes:
                    print('\n', ' ' * PADD, 'w/ same shape:\n')
                for sname, spattern in shapes:
                    sname = '[ ' + sname + ' ]'
                    print(' ' * PADD, sname.center(30, '~'))
                    print(render(spattern, STRINGS, PADD))
                    print('\n')

            prev = name
            print('\n')
