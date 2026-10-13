# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 Simone Felli
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.


"""
autofingers: guess a fingering (1..4 for the left hand fingers) for a chord.

chord_autofingers(['x','2','4','4','3','2']) -> ['x','1','3','4','2','1']

How it works:
    1. make_frets_cluster(): group the strings by fret number
    2. make_frets_clst_barre(): find possible barres, a fret pressed on
       more strings with no lower fret in between ("shadowing")
    3. valid_frets_cluster() / check_fingers_consistence(): check that 4
       fingers are enough, splitting a barre if needed
    4. chord_autofingers(): assign fingers from the lowest fret up

The result is a guess: it can give odd fingerings, and when a shape needs
more than 4 fingers the strings that cannot be fingered stay 'x'.
"""


# local application imports
from libs import global_utilities


def make_frets_cluster(frets_int):
    '''
    generate a fret cluster from frets_int:
    frets_clusters is a list of tuples. Every tuple element is: 
    a fret (in ascending order), a list of position that fret is 
    present in the frets original list and another list (fret_slice) which is
    the frets list with only the single fret retained (others are set to 0)
    ie: for Bm [None, 2, 4, 4, 3, 2] ->
    [
      (2, [1, 5], [0, 2, 0, 0, 0, 2])
    , (3, [4],    [0, 0, 0, 0, 3, 0])
    , (4, [2, 3], [0, 0, 4, 4, 0, 0])
    ]
    
    for C [None, 3, 2, 0, 1, 0], we have: 
    [
      (0, [3, 5], [0, 0, 0, 0, 0, 0])
    , (1, [4],    [0, 0, 0, 0, 1, 0])
    , (2, [2],    [0, 0, 2, 0, 0, 0])
    , (3, [1],    [0, 3, 0, 0, 0, 0])
    ]
    
    frets_int: List, number fret list of a chord
    
    return: List, frets_cluster (see above)
    '''
    # frets_int: [None, 3, 2, 0, 1, 0]
    # fret used grouped in a list (included 0s), ie: [2, 0, 1, 3]
    fret_group = list(set([elem for elem in frets_int if elem!=None]))
    # and sorted, ie: fret_group = [0, 1, 2, 3]
    fret_group.sort()
    frets_cluster = []
    # if fret is 1
    for fret in fret_group:
        positions = []
        # fret_slice = [0, 0, 0, 0, 1, 0]
        fret_slice = [elem if (elem == fret) else 0 for elem in frets_int]
        for idx, elem in enumerate(frets_int):
            if elem == fret:
                # positions = [4]
                positions.append(idx)
        frets_cluster.append((fret, positions, fret_slice))
    return frets_cluster


def expand_fr_clst(fr_clst):
    '''
    from a fret_cluster tuple (single tuple)
    generate an expanded_fr_clst which can be tought as
    single tuple splitted in two: 
    - first fret position from left part
    - remaining part
    ie:
    for E9: [None, 7, 6, 7, 7, 7] ->
    frets_cluster = [
        (6, [2],          [0, 0, 6, 0, 0, 0])
      , (7, [1, 3, 4, 5], [0, 7, 0, 7, 7, 7])
    ]
    if fr_clst is second elem =
    (7, [1, 3, 4, 5], [0, 7, 0, 7, 7, 7])
    -> expanded_fr_clst =
    [
      (7, [1],       [0, 7, 0, 0, 0, 0])
    , (7, [3, 4, 5], [0, 0, 0, 7, 7, 7])
    ]
    
    fr_clst: Tuple, single fret_cluster tuple
    
    return: List of tuple, splitted fret_cluster tuple in two parts
    '''
    expanded_fr_clst = []
    new_fret_slice = [0, 0, 0, 0, 0, 0]
    # fr_clst = (7, [1, 3, 4, 5], [0, 7, 0, 7, 7, 7])
    # list(fr_clst) is to make a list copy so changes on fret_slice do not affect fr_clst
    fret, positions, fret_slice = list(fr_clst)
    # skip single fret case, ie: [0, 0, 6, 0, 0, 0]
    if len(positions) > 2:
        # new_position = 1
        new_position = positions[0]
        # positions = [3, 4, 5]
        positions = positions[1:]
        # new_fret_slice: [0, 0, 0, 0, 0, 0] -> [0, 7, 0, 0, 0, 0]
        new_fret_slice[new_position] = fret
        # fret_slice: [0, 7, 0, 7, 7, 7] -> [0, 0, 0, 7, 7, 7]
        fret_slice[new_position] = 0
        expanded_fr_clst.append((fret, [new_position], new_fret_slice))
        expanded_fr_clst.append((fret, positions, fret_slice))
    else:
        # nothing to split: return a list with the original tuple, so the
        # caller can always do 'list += expand_fr_clst(...)'. It returned
        # the bare tuple, and 'list += tuple' added its 3 elements one by
        # one, ie chord 3,2,x,3,4,5 raised TypeError
        expanded_fr_clst = [fr_clst]
    return expanded_fr_clst


def make_frets_clst_barre(frets_cluster):
    '''
    generate a frets_clst_barre from frets_cluster:
    frets_clst_barre is a list of tuples similar to frets_cluster.    
    Every tuple element is generated from frets_cluster and is: 
    - a fret (in ascending order) -> same as frets_cluster
    - a list of position that fret is present in the frets original list -> same as frets_cluster
    - fret_slice -> same as frets_cluster
    - a list (fret_slice_sum) which is sum of fret_slice lists 
      preceding (in fret order) actual fret_slice. 
      But only if fret is not 0 and is repeated > 1 (candidate barre)
      otherwise output fret_slice_sum = fret_slice
    - a boolean flag, candidate_barre. It is True if a fret is not 0 and is 
      repeated more than one time
    - a boolean flag, valid_barre. It is True if there is no shadowing effect,
      ie: for ['x','7','6','7','7','7'] a barre on all 7 fret would shadow 6 fret
    
    ie: for Bm
    frets_cluster =
    [
      (2, [1, 5], [0, 2, 0, 0, 0, 2])
    , (3, [4],    [0, 0, 0, 0, 3, 0])
    , (4, [2, 3], [0, 0, 4, 4, 0, 0])
    ]
    -> frets_clst_barre =
    [
      (2, [1, 5], [0, 2, 0, 0, 0, 2], [0, 2, 0, 0, 0, 2], True,  True)
    , (3, [4],    [0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 3, 0], False, False)
    , (4, [2, 3], [0, 0, 4, 4, 0, 0], [0, 2, 4, 4, 3, 2], True,  True)
    ]
    
    for E9: ['x', '7', '6', '7', '7', '7']
    frets_cluster =
    [
      (6, [2], [0, 0, 6, 0, 0, 0])
    , (7, [1, 3, 4, 5], [0, 7, 0, 7, 7, 7])
    ]
    -> frets_clst_barre =
    [
      (6, [2],          [0, 0, 6, 0, 0, 0], [0, 0, 6, 0, 0, 0], False, False)
    , (7, [1, 3, 4, 5], [0, 7, 0, 7, 7, 7], [0, 7, 6, 7, 7, 7], True,  False)
    ]
    
    frets_cluster: List (see make_frets_cluster)
    
    return: List, frets_clst_barre (see above)
    '''
    frets_clst_barre = []
    for fret, positions, fret_slice in frets_cluster:
        fret_slice_sum = fret_slice
        candidate_barre = False
        valid_barre = False
        # if a fret is not 0 and is repeated more
        # than one time, then it's a candidate for barre
        if fret and len(positions) > 1:
            candidate_barre = True
            # min string position for that fret
            min_string_pos = min(positions)
            # max string position for that fret
            max_string_pos = max(positions)
            # do all the fret_slice sums for preceding actual fret_slice
            for elem in frets_cluster:
                if elem[0] < fret:
                    fret_slice_sum = list(map(sum, list(zip(fret_slice_sum, elem[2]))))
            # if fret_slice is equal to fret_slice_sum for 
            # actual fret positions then there is not shadowing effect
            # and valid_barre is True: 
            # [2, 0, 0, 0, 2] = [2, 0, 0, 0, 2]  -> no shadowing, True
            # [4, 4] == [4, 4]                   -> no shadowing, True            
            # [7, 0, 7, 7, 7] != [7, 6, 7, 7, 7] -> shadowing,    False
            if fret_slice[min_string_pos: max_string_pos] == \
                fret_slice_sum[min_string_pos: max_string_pos]:
                valid_barre = True
        # append to frets_clst_barre but omit fret 0 (open string)
        if fret:
            frets_clst_barre.append(
                (fret, positions, fret_slice, fret_slice_sum,
                candidate_barre, valid_barre)
                )
    return frets_clst_barre


def valid_frets_cluster(frets_cluster):
    '''
    check if a fret cluster can have a valid number fingering.
    Given four left-hand fingers it takes account of possible barre
    and check if fingers are enough for string pressed
    
    frets_cluster: List (see make_frets_cluster)
    
    return 
    - isvalid: Boolean, True if frets_cluster has enough fingers with barre included
    - n_strg_fng: Number, number of string pressed
    - frets_clst_barre: see make_frets_clst_barre above
    '''
    isvalid = False
    # frets_cluster for E9
    # [
    #   (6, [2],          [0, 0, 6, 0, 0, 0])
    # , (7, [1, 3, 4, 5], [0, 7, 0, 7, 7, 7])
    # ]
    # 
    # frets_clst_barre for E9
    # [
    #   (6, [2],          [0, 0, 6, 0, 0, 0], [0, 0, 6, 0, 0, 0], False, False)
    # , (7, [1, 3, 4, 5], [0, 7, 0, 7, 7, 7], [0, 7, 6, 7, 7, 7], True,  False)
    # ]
    #
    # --> return
    # (False, 5
    # , [
    #     (6, [2],          [0, 0, 6, 0, 0, 0], [0, 0, 6, 0, 0, 0], False, False)
    #   , (7, [1, 3, 4, 5], [0, 7, 0, 7, 7, 7], [0, 7, 6, 7, 7, 7], True,  False)
    #   ])
    #
    # frets_cluster for C
    # [
    #   (0, [3, 5], [0, 0, 0, 0, 0, 0])
    # , (1, [4],    [0, 0, 0, 0, 1, 0])
    # , (2, [2],    [0, 0, 2, 0, 0, 0])
    # , (3, [1],    [0, 3, 0, 0, 0, 0])
    # ]
    # 
    # frets_clst_barre for C
    # [
    #   (1, [4], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 0], False, False)
    # , (2, [2], [0, 0, 2, 0, 0, 0], [0, 0, 2, 0, 0, 0], False, False)
    # , (3, [1], [0, 3, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0], False, False)
    # ]
    # 
    # --> return
    # (True, 3
    # , [
    #     (1, [4], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 0], False, False)
    #   , (2, [2], [0, 0, 2, 0, 0, 0], [0, 0, 2, 0, 0, 0], False, False)
    #   , (3, [1], [0, 3, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0], False, False)
    #   ])
    frets_clst_barre = make_frets_clst_barre(frets_cluster)
    n_fngs_avail = 4
    # for E9
    # n_strg_fng = number of string pressed, ie 5
    n_strg_fng = sum([len(elem[1]) for elem in frets_clst_barre])
    for elem in frets_clst_barre:
        # [2], False, False
        # [1, 3, 4, 5], True,  False
        positions, candidate_barre, valid_barre = elem[1], elem[4], elem[5]
        if (n_strg_fng > n_fngs_avail):
            # if is a valid barre
            if candidate_barre:
                if valid_barre:
                    # then is just one finger less from avaiable fingers
                    n_fngs_avail -= 1
                else:
                    # else subctract all fingers needed for that fret (4 fingers for 7th fret)
                    n_fngs_avail = n_fngs_avail - len(positions)
            else:
                # no barre -> subctract all fingers needed for that fret
                n_fngs_avail = n_fngs_avail - len(positions)
        else:
            # subctract all fingers needed for that fret
            n_fngs_avail = n_fngs_avail - len(positions)
    # if, after all, there are fingers left, then we are ok
    if n_fngs_avail >= 0: isvalid = True
    return isvalid, n_strg_fng, frets_clst_barre



def check_fingers_consistence(frets_cluster):
    '''
    this function make last attempt to find a fingering scheme if there are
    not enough fingers avaiable including barre. It calls expand_fr_clst on
    first not valid barre (if present) splitting it in two and checking again fingers number
    
    For E9: frets_cluster
    [
      (6, [2],          [0, 0, 6, 0, 0, 0])
    , (7, [1, 3, 4, 5], [0, 7, 0, 7, 7, 7])
    ]
    -> not enough fingers (5): valid_frets_cluster
    (False, 5
    , [
        (6, [2],          [0, 0, 6, 0, 0, 0], [0, 0, 6, 0, 0, 0], False, False)
      , (7, [1, 3, 4, 5], [0, 7, 0, 7, 7, 7], [0, 7, 6, 7, 7, 7], True,  False)
      ])
    -> try to split first candidate but not valid barre (second elem)
    (5, [
            (6, [2],       [0, 0, 6, 0, 0, 0], [0, 0, 6, 0, 0, 0], False, False), 
            (7, [1],       [0, 7, 0, 0, 0, 0], [0, 7, 0, 0, 0, 0], False, False), 
            (7, [3, 4, 5], [0, 0, 0, 7, 7, 7], [0, 0, 6, 7, 7, 7], True,  True)
        ]
    )
    
    frets_cluster: List (see make_frets_cluster)
    
    return: 
    - n_strg_fng: Number, number of string pressed
    - frets_clst_barre: frets_clst_barre of new splitted (if that is the case) configuration
    
    '''
    temp_fret_cluster = []
    # For E9 valid_frets_cluster: (
    # False, 5, [
    #           (6, [2],          [0, 0, 6, 0, 0, 0], [0, 0, 6, 0, 0, 0], False, False)
    #         , (7, [1, 3, 4, 5], [0, 7, 0, 7, 7, 7], [0, 7, 6, 7, 7, 7], True,  False)
    #         ]
    # )
    isvalid_frets_cluster, n_strg_fng, frets_clst_barre = valid_frets_cluster(frets_cluster)
    # if cluster do not match fingers number
    if not isvalid_frets_cluster:
        for elem in frets_clst_barre:
            # fret, positions,    fret_slice,         candidate_barre, valid_barre =
            # 7,    [1, 3, 4, 5], [0, 7, 0, 7, 7, 7], True,            False
            fret, positions, fret_slice, candidate_barre, valid_barre = \
                elem[0], elem[1], elem[2], elem[4], elem[5]
            # and there is a valid barre
            if (candidate_barre and not valid_barre):
                # then try splitting that barre:
                # expand_fr_clst on (7, [1, 3, 4, 5], [0, 7, 0, 7, 7, 7]) -> 
                # [
                #   (7, [1],       [0, 7, 0, 0, 0, 0])
                # , (7, [3, 4, 5], [0, 0, 0, 7, 7, 7])
                # ]
                # and add it to temp_fret_cluster
                temp_fret_cluster += expand_fr_clst((fret, positions, fret_slice))
            else:
                # else do not split and temp_fret_cluster current element is just like frets_cluster
                temp_fret_cluster += [(fret, positions, fret_slice)]
    else:
        temp_fret_cluster = frets_cluster
    return n_strg_fng, make_frets_clst_barre(temp_fret_cluster)
                 


def next_finger(fngs_avail):
    '''
    take the next free finger (the lowest number) out of fngs_avail.
    Return None when all 4 fingers are already used: this happens for shapes
    that cannot be played with 4 fingers (ie frets 1,2,3,4,5,6), which used
    to raise "IndexError: pop from empty list"
    
    fngs_avail: List of numbers, free fingers, ie [4, 3, 2, 1]
    
    return: Number or None
    '''
    # pop() removes and returns the last element: [4, 3, 2, 1] -> 1
    return fngs_avail.pop() if fngs_avail else None


def chord_autofingers(frets_str):
    '''
    Given a fret list of strings try to calculate its finger list.
    It uses previous defined functions (make_frets_cluster, check_fingers_consistence
    Sometimes gives odds fingerings ...
    
    frets_str: List of strings, input fret list, ie for Bm: ['x','2','4','4','3','2']
    
    return fingers: List of strings, out finger list, ie: ['x','1','3','4','2','1']
    '''
    # return fingers list initialize
    fingers = ['x','x','x','x','x','x',]
    # list of fingers avaiable, initialization
    fngs_avail = [4,3,2,1]
    # number of avaiable fingers in the beginning: all 4 fingers
    n_fngs_avail = len(fngs_avail)
    # frets_str -> frets_int, ie: ['x','2','4','4','3','2'] -> [None, 2, 4, 4, 3, 2]
    frets_int = global_utilities.crd_slst2ilst(frets_str)
    # frets_cluster = [
    #   (2, [1, 5], [0, 2, 0, 0, 0, 2])
    # , (3, [4],    [0, 0, 0, 0, 3, 0])
    # , (4, [2, 3], [0, 0, 4, 4, 0, 0])
    # ]
    frets_cluster = make_frets_cluster(frets_int)
    # now use check_fingers_consistence to find a valid 
    # fingering scheme (see function explanation, it can do splitting if needed)
    # check_fingers_consistence -> (
    #     5
    #     , [
    #           (2, [1, 5], [0, 2, 0, 0, 0, 2], [0, 2, 0, 0, 0, 2], True,  True)
    #         , (3, [4],    [0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 3, 0], False, False)
    #         , (4, [2, 3], [0, 0, 4, 4, 0, 0], [0, 2, 4, 4, 3, 2], True,  True)
    #       ]
    # )
    n_strg_fng, frets_clst_barre = check_fingers_consistence(frets_cluster)
    
    for elem in frets_clst_barre:
        # positions, candidate_barre, valid_barre
        # [2, 3],    True,            True
        positions, candidate_barre, valid_barre = elem[1], elem[4], elem[5]
        if candidate_barre:
            # barre must happen if number of strings fingered
            # is > than number of fingers avaiable (5 > 4) and is a valid barre
            if (n_strg_fng > n_fngs_avail) and valid_barre:
                # use first avaiable finger on lower fret
                # remove that finger from avaiable fingerslist
                # pop() with no argument remove last element (right) 
                # from fngs_avail and return it
                act_finger = next_finger(fngs_avail)
                # decrease number of avaiable fingers
                n_fngs_avail -= 1
                # modify fingers list with that finger
                for pos in positions:
                    # (no finger left: the string stays 'x', see next_finger)
                    if act_finger: fingers[pos] = str(act_finger)
                    # decrease number of strings fingered
                    n_strg_fng -= 1
            # if no barre is needed, just add fingers in order
            # starting from lower strings (fingers list from left is
            # populatede by lower strings)
            else:
                for pos in positions:
                    # use first avaiable finger on lower fret
                    # remove that finger from avaiable fingerslist
                    act_finger = next_finger(fngs_avail)
                    # decrease number of avaiable fingers
                    n_fngs_avail -= 1
                    # modify fingers list with that finger
                    if act_finger: fingers[pos] = str(act_finger)
                    # decrease number of strings fingered
                    n_strg_fng -= 1
        # if a fret is repeated only once
        # just add an avaiable fingers
        else:
            act_finger = next_finger(fngs_avail)         
            n_fngs_avail -= 1
            if act_finger: fingers[positions[0]] = str(act_finger)
            n_strg_fng -= 1
    
    return fingers



if __name__ == "__main__":
    
    # testing this functions
    
    # ---- simple test ----
    
    #test_fret = (['0','2','4','4','3','2'], ['x', '1', '3', '4', '2', '1'], 'Bm')
    test_fret = (['x','3','2','0','1','0'], ['x', '3', '2', 'x', '1', 'x'], 'C')
    #test_fret = (['x','7','6','7','7','7'], ['x', '2', '1', '3', '3', '3'], 'E9')
    #test_fret = (['3','2','3','3','4','4'], ['2', '1', '3', '3', '4', '4'], 'GY')
    #test_fret = (['3','3','5','5','6','6'], ['1', '1', '2', '2', '3', '4'], 'XY')
    
    print('------------------------------------------------------------------')
    print(test_fret[2], ':', test_fret[0])
    print('Assert: ', test_fret[1])
    frets_int = global_utilities.crd_slst2ilst(test_fret[0])
    print('frets_int', frets_int)    
    frets_cluster = make_frets_cluster(frets_int)
    print('frets_cluster', frets_cluster)
    exp_fr_cl = expand_fr_clst(frets_cluster[1])
    print('expand_fr_clst', exp_fr_cl)
    print(frets_cluster)
    frets_clst_barre = make_frets_clst_barre(frets_cluster)
    print('frets_clst_barre', frets_clst_barre)
    print(frets_cluster)      
    valid_check = valid_frets_cluster(frets_cluster)
    print('valid_frets_cluster', valid_check)    

    chk_fng_cns= check_fingers_consistence(frets_cluster)
    print('check_fingers_consistence', chk_fng_cns)
    
    print('chord_autofingers', chord_autofingers(test_fret[0]))

