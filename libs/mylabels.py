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
mylabels: single line text labels.

svgwrite does not measure text, so label sizes are estimated: for a
monospace font every char has the same width, and width/height are
proportional to the font size with a factor that depends on the font
(see get_labelparams). From one known value (font size, label width or
label height) the other ones are computed, so a label can be fitted in a
given width (mylabel_given_wdth) or a given height (mylabel_given_hght).
"""


# local application imports
from libs import myshapes



def get_labelparams(mystr, labelfont_family, myfont_size=None, label_w=None, label_h=None):
    '''
    Helper function. Given label, font family and 1 or 2 param of choice (between
    myfont_size, label_w and label_h) this function calculate the remaining the 1 or 2 param.
    ie: myfont_size -> f() -> label_w, label_h
        myfont_size, label_w -> f() -> label_h
        myfont_size, label_h -> f() -> label_w
        label_w -> f() -> myfont_size, label_h
        label_h -> f() -> myfont_size, label_w
        
    mystr: String, this is the label
    labelfont_family: String, label font family
    myfont_size: Number, font size (optional argument)
    label_w: Number, label width (optional argument)
    label_h: Number, label height (optional argument)
    
    return a tuple of (font size, label width, label height) 
    '''
    nchar = len(mystr)
    # empiric factors for every supported monospace font:
    #   label_w = (font_size * nchar) / label_w_factor
    #   label_h = font_size / label_h_factor
    # ie with label_w_factor = 2.00 every char is half font size wide.
    # Any other font (ie 'Ubuntu Mono', 'Ubuntu Mono Legacy') uses the
    # last (else) factors
    if labelfont_family.lower() == 'courier new':
        label_w_factor = 1.67
        label_h_factor = 1.60
    elif labelfont_family.lower() == 'liberation mono':
        label_w_factor = 1.65
        label_h_factor = 1.45
    elif labelfont_family.lower() == 'dejavu sans mono':
        label_w_factor = 1.67
        label_h_factor = 1.38
    else:
        label_w_factor = 2.00
        label_h_factor = 1.60   
    if myfont_size:
        if label_h and not label_w:
            label_w = (myfont_size * nchar) / label_w_factor
        if label_w and not label_h:
            label_h = (myfont_size / label_h_factor)
        if not label_w and not label_h:
            label_w = (myfont_size * nchar) / label_w_factor
            label_h = (myfont_size / label_h_factor)
    else:
        if label_h and not label_w:
            myfont_size = (label_h * label_h_factor)
            label_w = (myfont_size * nchar) / label_w_factor
        if label_w and not label_h:
            myfont_size = (label_w * label_w_factor) / nchar
            label_h = (myfont_size / label_h_factor)
    return myfont_size, label_w, label_h


def get_label_h_given_wdth(mystr, label_w, labelfont_family):
    """
    Estimate label height and font size from chord label string 
    and label width using get_labelparams() helper function

    mystr: String, this is the label 
    label_w: Number, label width
    labelfont_family: String, label font family

    return a tuple of (font size, label height) 
    """
    myfont_size, _, label_h = get_labelparams(mystr, labelfont_family, label_w=label_w)
    return myfont_size, label_h


def get_label_w_given_hght(mystr, label_h, labelfont_family):
    """
    Estimate label width and font size from chord label string 
    and label height using get_labelparams() helper function

    mystr: String, this is the label 
    label_h: Number, label height
    labelfont_family: String, label font family

    return a tuple of (font size, label width) 
    """
    myfont_size, label_w, _ = get_labelparams(mystr, labelfont_family, label_h=label_h)
    return myfont_size, label_w



def mylabel_given_wdth(dwg, mycenter, mystr, label_w,
             font_weight, font_family,
             align_center_flag=True,
             fill='black', fill_opacity='1',
             stroke='none', stroke_width='0',
             edge_debug=False):
    """
    Draw a Label with fixed width and return label_h

    dwg: Svgwrite object
    mycenter: Tuple, label center (x, y) 
    mystr: String, this is the label
    label_w: Number, label width
    font_weight: String, font weight
    font_family: String, font family
    align_center_flag: Boolean, if true align center the label, otherwise align left
    fill: String, square fill color
    fill_opacity: String, label fill opacity value
    stroke: String, square stroke color
    stroke_width: String, square stroke width
    edge_debug: Boolean, if true draw label contour

    return Number: label_h
    """        
    
    myfont_size, label_h = get_label_h_given_wdth(mystr, label_w, font_family)
    # if align_center_flag is True then to get start string point (bottom left)
    # shift label x to left by (label_w / 2) and shift label
    # y center down by (label_h / 2)
    # debug_square_center is equal to mycenter as mysquare() wants square center (x, y) 
    if align_center_flag: 
        str_start_point = (mycenter[0] - (label_w / 2), mycenter[1] + (label_h / 2))
        debug_square_center = mycenter
    # if align_center_flag is False then to get start string point
    # label x is already at bottom left while you always need to shift label y center 
    # down by (label_h / 2). debug_square_center x must be shifted bach to right by 
    # (label_h / 2), while debug_square_center y is ok
    else:
        str_start_point = (mycenter[0], mycenter[1] + (label_h / 2)) 
        debug_square_center = (mycenter[0] + (label_w / 2), mycenter[1])
    if edge_debug: 
        myshapes.mysquare(dwg, debug_square_center, (label_w, label_h), stroke='red', stroke_width='0.5')
        dwg.add(
            dwg.circle(
                center=mycenter, r=1.5, fill="red", fill_opacity="0.5", 
                stroke="red", stroke_width="0"
                )
            )
        dwg.add(
            dwg.circle(
                center=str_start_point, r=1.5, fill="blue", fill_opacity="0.5", 
                stroke="red", stroke_width="0"
                )
            )
    my_text = dwg.text(
          mystr
        , insert=str_start_point
        , stroke=stroke
        , stroke_width=stroke_width
        , fill=fill
        , fill_opacity=fill_opacity
        , font_size=myfont_size
        , font_weight=font_weight
        , font_family=font_family
    )
    my_text.update(
        {'xml:space' : 'preserve'}
    )
    dwg.add(my_text)
    return label_h


def mylabel_given_hght(dwg, mycenter, mystr, label_h,
             font_weight, font_family,
             align_center_flag=True,
             fill='black', fill_opacity='1',
             stroke='none', stroke_width='0',
             edge_debug=False):
    """
    Draw a Label with fixed height and return label_w

    dwg: Svgwrite object
    mycenter: Tuple, label center (x, y) 
    mystr: String, this is the label
    label_h: Number, label height
    font_weight: String, font weight
    font_family: String, font family
    align_center_flag: Boolean, if true align center the label, otherwise align left
    fill: String, label fill color
    fill_opacity: String, label fill opacity value
    stroke: String, square stroke color
    stroke_width: String, square stroke width
    edge_debug: Boolean, if true draw label contour

    return Number: label_w
    """        
  
    myfont_size, label_w = get_label_w_given_hght(mystr, label_h, font_family)
    # if align_center_flag is True then to get start string point (bottom left)
    # shift label x to left by (label_w / 2) and shift label
    # y center down by (label_h / 2)
    # debug_square_center is equal to mycenter as mysquare() wants square center (x, y) 
    if align_center_flag: 
        str_start_point = (mycenter[0] - (label_w / 2), mycenter[1] + (label_h / 2))
        debug_square_center = mycenter
    # if align_center_flag is False then to get start string point
    # label x is already at bottom left while you always need to shift label y center down by (label_h / 2)
    # debug_square_center x must be shifted bach to right by (label_h / 2), while debug_square_center y is ok
    else:
        str_start_point = (mycenter[0], mycenter[1] + (label_h / 2)) 
        debug_square_center = (mycenter[0] + (label_w / 2), mycenter[1])
    if edge_debug: 
        myshapes.mysquare(dwg, debug_square_center, (label_w, label_h), stroke='red', stroke_width='0.5')
        dwg.add(
            dwg.circle(
                center=mycenter, r=1.5, fill="red", fill_opacity="0.5", 
                stroke="red", stroke_width="0"
                )
            )
        dwg.add(
            dwg.circle(
                center=str_start_point, r=1.5, fill="blue", fill_opacity="0.5", 
                stroke="red", stroke_width="0"
                )
            )
    my_text = dwg.text(
          mystr
        , insert=str_start_point
        , stroke=stroke
        , stroke_width=stroke_width
        , fill=fill
        , fill_opacity=fill_opacity
        , font_size=myfont_size
        , font_weight=font_weight
        , font_family=font_family
    )
    my_text.update(
        {'xml:space' : 'preserve'}
    )
    dwg.add(my_text)
    return label_w


def draw_labels(labels, label_len, labels_vector, dwg,
                font_weight, font_family,
                align_center_flag=True,
                label_len_is_h=False,
                fill='black', fill_opacity='1',
                stroke='none', stroke_width='0',
                edge_debug=False):
    """
    Draw a list of labels

    labels: List of strings, labels sequence
    label_len: Number, labels width or height
    labels_vector: List of tuple, labels center points (x, y)
    dwg: Svgwrite object
    font_weight: String, font weight
    font_family: String, font family
    align_center_flag: Boolean, if true align center the label, otherwise align left
    label_len_is_h: Boolean, if true label_len is label height, otherwise is width
    font_weight: String, font weight
    font_family: String, font family
    label_len_is_h: Boolean, if true use mylabel_given_hght instead of mylabel_given_wdth
    fill: String, labels fill color
    fill_opacity: String, labels fill opacity value
    stroke: String, labels stroke color
    stroke_width: String, labels stroke width
    edge_debug: Boolean, if true draw labels contour
    
    return nothing    
    """
    if labels:
        for idx, label in enumerate(labels):
            if label:
                if label_len_is_h:
                    mylabel_given_hght(dwg, labels_vector[idx], label, label_len,
                                              font_weight=font_weight, font_family=font_family,
                                              align_center_flag=align_center_flag,
                                              fill=fill, fill_opacity=fill_opacity,
                                              stroke=stroke, stroke_width=stroke_width,
                                              edge_debug=edge_debug)
                else:
                    mylabel_given_wdth(dwg, labels_vector[idx], label, label_len,
                                              font_weight=font_weight, font_family=font_family,
                                              align_center_flag=align_center_flag,
                                              fill=fill, fill_opacity=fill_opacity,
                                              stroke=stroke, stroke_width=stroke_width,
                                              edge_debug=edge_debug)   


if __name__ == "__main__":
    
    # testing this functions
    
    import svgwrite
    
    sqr_wdth = 30.0
    crcl_rad = sqr_wdth / 2.0
    
    dwg = svgwrite.Drawing(filename='../dirout/labels_test.svg', size=(150, 300), debug=True)

    labels_centers_vector = [
        (21, 255), (42, 255), (63, 255), (84, 255), (105, 255), (126, 255)
        ]

    lbls_str_lst = ['K', 'j', '7', '5', 'X', 'Qx']

    # font_family='Ubuntu Mono Legacy'
    font_family='Courier New'
    # font_family='Liberation Mono'
    # font_family='DejaVu Sans Mono'
    
    print('get_labelparams("QO#", "Ubuntu Mono Legacy", label_w=50)')
    print(get_labelparams('QO#', 'Ubuntu Mono Legacy', label_w=50))
    print('get_labelparams("QO#", "Ubuntu Mono Legacy", label_h=20.833)')
    print(get_labelparams('QO#', 'Ubuntu Mono Legacy', label_h=20.833))
    
    print('mylabel_given_wdth(dwg, (75, 20), "QO#", 50, ... "Ubuntu Mono Legacy")')
    print(mylabel_given_wdth(dwg, (75, 20), 'QO#', 50,
                       font_weight='bold', font_family='Ubuntu Mono Legacy', edge_debug=True)
        )
    print('mylabel_given_wdth(dwg, (75, 50), "QO#", 50, ... font_family)')
    print(mylabel_given_wdth(dwg, (75, 50), 'QO#', 50,
                       font_weight='bold', font_family=font_family, edge_debug=True)
        )

    print('mylabel_given_wdth(dwg, (40, 80), "QO#", 50, ... "Ubuntu Mono Legacy")')
    print(mylabel_given_wdth(dwg, (40, 80), 'QO#', 50,
                       font_weight='bold', font_family='Ubuntu Mono Legacy', edge_debug=True)
        )
    print('mylabel_given_wdth(dwg, (110, 80), "QO#", 50, ... font_family)')
    print(mylabel_given_wdth(dwg, (110, 80), 'QO#', 50,
                       font_weight='bold', font_family=font_family, edge_debug=True)   
        )

    print('mylabel_given_wdth(dwg, (75, 110), "Align left", 72, ... "Ubuntu Mono Legacy")')
    print(mylabel_given_wdth(dwg, (75, 110), 'Align left', 72,
          align_center_flag=False, font_weight='bold', font_family='Ubuntu Mono Legacy', edge_debug=True)
        )

    print('mylabel_given_hght(dwg, (75, 135), "Align left", 7.5, ... font_family)')
    print(mylabel_given_hght(dwg, (75, 135), 'Align left', 7.5,
          align_center_flag=False, font_weight='bold', font_family=font_family, edge_debug=True)
        )

    print('mylabel_given_hght(dwg, (40, 160), "Qj7b5", 12.5, ... "Ubuntu Mono Legacy")')
    print(mylabel_given_hght(dwg, (40, 160), '#Qj7b5', 12.5,
                       font_weight='bold', font_family='Ubuntu Mono Legacy', edge_debug=True)
        )
    print('mylabel_given_hght(dwg, (110, 160), "Qj7b5", 12.5, ... font_family)')
    print(mylabel_given_hght(dwg, (110, 160), '#Qj7b5', 12.5,
                       font_weight='bold', font_family=font_family, edge_debug=True)
        )

    print('mylabel_given_hght(dwg, (75, 190), "Qj7be", 12.5, ... "Ubuntu Mono Legacy")')
    print(mylabel_given_hght(dwg, (75, 190), '#Qj7be', 12.5,
                       font_weight='bold', font_family='Ubuntu Mono Legacy', edge_debug=True)
        )
    print('mylabel_given_hght(dwg, (75, 220), "Qj7be", 12.5, ... font_family)')
    print(mylabel_given_hght(dwg, (75, 220), 'Qj7be', 12.5,
                       font_weight='bold', font_family=font_family, edge_debug=True)
        )


    draw_labels(lbls_str_lst, (crcl_rad * 0.7),
                labels_centers_vector, dwg,
                label_len_is_h=True,
                font_weight='bold', font_family='Ubuntu Mono Legacy',
                fill_opacity='0.5', edge_debug=True)
    
    print('mylabel_given_hght(dwg, (75, 280), "   Xy45@   ", 12.5, ... "Ubuntu Mono")')
    print(mylabel_given_hght(dwg, (75, 280), '   Xy45@   ', 12.5,
                       font_weight='bold', font_family='Ubuntu Mono Legacy', edge_debug=True)
        )
    
    dwg.save()
