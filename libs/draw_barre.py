# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Simone Felli
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
draw_barre: find and draw barres (one finger pressing more strings).

A barre is drawn as an arc over the dots when the same finger number is
used on more strings at the same fret, ie: fingers 1,3,4,2,1,1 on frets
8,10,10,9,8,8 -> finger 1 on fret 8 makes a barre from string 6 to string 1.
"""

# library to handle chord barre


def check_barre(fingers_int, frets_int):
    """
    Given two integer lists (fingers_int, frets_int) for fingers and frets
    this function return a tuples of list. First tuple element is a list that
    comes from fingers where there are only equal fingers. 
    Second tuple element is a list that comes from frets where
    there are only elemets that match first tuple element:
    [None, 1, 4, 4, 4, 1], [None, 4, 6, 6, 6, 4] ->
    [
        ([None, 1, None, None, None, 1], [None, 4, None, None, None, 4]), 
        ([None, None, 4, 4, 4, None], [None, None, 6, 6, 6, None])
    ]

    fingers_int: List, finger sequence converted to ints (None for non digit)
    frets_int: List, fret sequence converted to ints (None for non digit)

    return a tuples of list (see above)
    """
    # example1: frets, fingers = [None, 1, 4, 4, 4, 1], [None, 4, 6, 6, 6, 4]
    # example2: frets, fingers = [None, 1, 3, 1, 2, 1], [None, 4, 6, 4, 5, 4]
       
    # fingers_int_flt: filter None from fingers_int list: 
    # example1: [None, 4, 6, 6, 6, 4] -> [4, 6, 6, 6, 4]
    # example2: [None, 4, 6, 4, 5, 4] ->  [4, 6, 4, 5, 4]    
    fingers_int_flt = list([x for x in fingers_int if (x and (x >= 0))])
    
    # fingers_int_grp: remove duplicates (group by) from fingers_int_flt: [4, 6, 4, 5, 4] -> [4, 5, 6]
    # example1: [4, 6, 6, 6, 4] -> [4, 6]
    # example2: [4, 6, 4, 5, 4] -> [4, 5, 6]
    fingers_int_grp = list(set(fingers_int_flt))
    
    # count_fingers: list with all duplicate frets:
    # example1: [4, 6, 6, 6, 4] -> 4 occours 2 times, 6 occours 3 times. Append both 4 and 6 -> [4, 6]
    # example2: [4, 6, 4, 5, 4] -> 4 occours 3 times other frets only 1. Append only 4 -> [4]
    count_fingers = []
    for fr in fingers_int_grp:
        # example2: 4 -> occours 3 times
        c_fr = fingers_int_flt.count(fr)
        # example2: Append [4]
        if c_fr > 1: count_fingers.append(fr)
   
    # return_list: list of tuples. Every tuple is formed of two list built like that; 
    # for every duplicate finger in count_fingers: 
    # first list (fingers_dbl) comes from fingers_int where we keep only positions for duplicate finger (None for others)
    # second list (fingers_frets) comes from frets_int where we keep only frets for duplicate finger 
    # example1: [4, 6] -> [ ([None, 1, None, None, None, 1], [None, 4, None, None, None, 4]),
    #                       ([None, None, 4, 4, 4, None], [None, None, 6, 6, 6, None]) ]
    # example2: [4] -> [ ([None, 1, None, 1, None, 1], [None, 4, None, 4, None, 4]) ]
    return_list = []   
    for elem in count_fingers:
        # example2: [None, 4, None, 4, None, 4]
        fingers_dbl = [el if (el == elem) else None for el in fingers_int]
        # example2: [None, 1, None, None, None, 1]
        fingers_frets = [frets_int[idx] if el else None for idx, el in enumerate(fingers_dbl)]
        return_list.append((fingers_dbl, fingers_frets))
    
    return return_list 


def myarc(pt1, pt2,
          horiz, alfa, beta, strk_wdth, dwg,
          radius, fd
          ):
    """
    Draw single arc

    pt1, pt2: Tuples (x,y), edge points of arc
    horiz: Boolean, if true chord is horizontal otherwise vertical
    alfa, beta: Numbers, params for bezier-curve
    strk_wdth: Number, arc tickness
    dwg: Svgwrite object
    radius: Number, dot radius
    fd: Number, fret distance (px)

    return nothing    
    """
    # calculate params for bezier-curve
    if horiz:
        pt1_y = pt1[1] + (radius / 2)
        pt1_x = pt1[0] - (fd * 0.75)
        pt2_y = pt2[1] - (radius / 2)
        pt2_x = pt2[0] - (fd * 0.75)           
        delta = pt2_y - pt1_y
        y2, x2 = pt1_y + (delta * alfa), pt1_x + (delta * beta)
        y3, x3 = pt2_y - (delta * alfa), pt1_x + (delta * beta)         
    else:
        pt1_x = pt1[0] - (radius / 2)
        pt1_y = pt1[1] - (fd * 0.75)
        pt2_x = pt2[0] + (radius / 2)
        pt2_y = pt2[1] - (fd * 0.75)        
        delta = pt2_x - pt1_x
        x2, y2 = pt1_x + (delta * alfa), pt1_y - (delta * beta)
        x3, y3 = pt2_x - (delta * alfa), pt1_y - (delta * beta)
  
    # --------------------------------------------
    # M - move to the specified coordinate. This is the starting point of the curve
    # C - cubic Bézier curve consisting of 4 points, the previous point and the 3 after the C
    # "M 10,10 C 20,20, 40,20, 50,10"
    bezstring = "M" + str(pt1_x) + "," + str(pt1_y) + \
                " C" + str(x2) + "," + str(y2) + " " + \
                 str(x3) + "," + str(y3) + " " + \
                 str(pt2_x) + "," + str(pt2_y)
    # draw a cubic-bezier-curve path
    dwg.add(dwg.path(d=bezstring,
                     stroke="#000",
                     fill="none",
                     stroke_width=strk_wdth
                     )
    )


def draw_arc(dot1, dot2, centers_matrix, nf,
             horiz, dwg, radius, fd, arc_strk_wdth,
             alfa=0.33,
             beta=0.1):
    """
    Draw arc given a couples of point in (nut, string) format

    dot1, dot2: Tuples (fret, string), vertex of barre arc. Note that 
            fret start from 1 and thinner string is 6
    centers_matrix: List of list, dot centers matrix
    nf: Number, number of frets
    horiz: Boolean, if true chord is horizontal otherwise vertical
    dwg: Svgwrite object
    radius: Number, dot radius
    fd: Number, fret distance (px)
    arc_strk_wdth: Number, arc tickness
    alfa, beta: Numbers, params for bezier-curve
    strk_wdth: Number, arc tickness

    return nothing
    """    
    if len(centers_matrix) > nf: # if true then means first line is fret 0
        centers_matrix = centers_matrix[1::] # so we start from fret 1
    myarc(
        centers_matrix[dot1[0] - 1][dot1[1] - 1],
        centers_matrix[dot2[0] - 1][dot2[1] - 1],
        horiz, alfa, beta, arc_strk_wdth, dwg,
        radius, fd
        )


def draw_barre(enable_barre, frets_int, fingers_int, first_fret,
               centers_matrix, nf, horiz, dwg, radius, fd, barre_strk_wdth):
    """
    Draw chord barre/s (may be one or more)

    frets_int: List, fret sequence converted to ints (None for non digit)
    fingers_int: List, fingers sequence converted to ints (None for non digit)
    first_fret: Number, min fret
    enable_barre: Boolean, if true draw barre/s on chord
    centers_matrix: List of list, dot centers matrix
    nf: Number, number of frets
    horiz: Boolean, if true chord is horizontal otherwise vertical
    dwg: Svgwrite object
    radius: Number, dot radius
    fd: Number, fret distance (px)
    barre_strk_wdth: Number, barre arc tickness

    return nothing
    """      
    if enable_barre: 
        # apply check_barre() and store result lit in cand_barre
        # [None, 2, 1, 3, 3, 3], [None, 5, 4, 5, 5, 5] ->
        # cand_barre = [([None, None, None, 3, 3, 3], [None, None, None, 5, 5, 5])]
        cand_barre = check_barre(fingers_int, frets_int)
        # barre is a tuple list representing barre/s we are going to draw.
        # barre list structure is: [(starting string, ending string, fret number), ...]
        barre = []
        for elem in cand_barre:
            # remove duplictes from fret lists in cand_barre and remove 'None' elements:
            # [None, None, None, 5, 5, 5] - > [5]
            barre_frets = list(set([x for x in elem[1] if (x and (x >= 0))]))
            #  if there is only one fret in barre_frets then it is a real barre 
            # (fingers are already checked in cand_barre function)
            if len(barre_frets) == 1:
                # tmp_barre_strings is a list with index position (+1) of element in fret list above
                # [None, None, None, 5, 5, 5] - > [4, 5, 6], ie: 5 fret is in position 4, 5, 6 of list
                tmp_barre_strings = [(idx + 1) for idx, el in enumerate(elem[1]) if el]
                # append in barre tuple ((starting string, ending string, fret number): (5, 4, 6)
                barre.append((barre_frets[0], min(tmp_barre_strings), max(tmp_barre_strings)))
        # barre = [(5, 4, 6)]    
        for elem in barre:
            # if chord first fret is > 0 (no nut) first fret must be normalized (set to 1, 5 -> 1)
            if (first_fret > 0): 
                normfrt = elem[0] - (first_fret) + 1
            else:
                normfrt = elem[0]
            # arc point1 (fret, string) -> (1, 4)
            dot1 = (normfrt, elem[1])
            # arc point2 (fret, string)) -> (1, 6)
            dot2 = (normfrt, elem[2])
            # draw arc
            draw_arc(dot1, dot2, centers_matrix, nf, horiz, dwg, radius, fd, barre_strk_wdth)     


if __name__ == "__main__":
    
    # testing this function
    
    # third party imports
    import svgwrite
    from libs import mydots
     
    # --- functions parameters ---
    enable_barre = True
    frets_int = [10, 10, 12, 12, 11, 10]
    fingers_int = [1, 1, 3, 4, 2, 1]
    first_fret = 10
    centers_matrix =  [
         [(57,  96),  (107, 96),  (157, 96), 
          (207, 96),  (257, 96),  (307, 96)], 
         [(57,  161), (107, 161), (157, 161), 
          (207, 161), (257, 161), (307, 161)], 
         [(57,  226), (107, 226), (157, 226), 
          (207, 226), (257, 226), (307, 226)], 
         [(57,  291), (107, 291), (157, 291), 
          (207, 291), (257, 291), (307, 291)], 
         [(57,  356), (107, 356), (157, 356), 
          (207, 356), (257, 356), (307, 356)]
    ]
    nf = 4
    horiz = False
    radius = 20.5
    fd = 65.0
    barre_strk_wdth = 3.0    

    dwg = svgwrite.Drawing(filename='../dirout/draw_barre_test.svg', size=(350, 450), debug=True)

    for row in centers_matrix:
        for point in row:
            dwg.add(dwg.circle(center=point, r=2, fill="red", stroke="red", stroke_width="0"))

    mydots.mydot(dwg, centers_matrix[1][0], 'X'
          , labelfont_weight='bold'
          , labelfont_family='Courier New'
          , radius = radius
          , square=False
          , sq_rotate=False
          , dotfill='black'
          , dotstroke='black'
          , dotstroke_width='3'
          , labelfill='white'
          )

    mydots.mydot(dwg, centers_matrix[1][5], 'Y'
          , labelfont_weight='bold'
          , labelfont_family='Courier New'
          , radius = radius
          , square=False
          , sq_rotate=False
          , dotfill='black'
          , dotstroke='black'
          , dotstroke_width='3'
          , labelfill='white'
          )

    draw_barre(enable_barre, frets_int, fingers_int, first_fret,
               centers_matrix, nf, horiz, dwg, radius, fd, barre_strk_wdth)

    dwg.save()
