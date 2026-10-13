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
mymultilabels: chord name labels on one or two lines.

A main label (chord or scale name) can contain one newline to be drawn on
two lines, ie fancyscales titles like 'Am Pentatonic Scale\\nPosition 1'.
These functions extend mylabels to measure and draw such labels, centered
or left aligned. A label without newline is drawn on a single line.
"""

from libs import myshapes
from libs import mylabels


def isvalid_multiline(mystr):
    '''
    Check is input string (mystr) is a multiline string
    (ie, just 2 lines other cases are not supported)
    and return splitted string in a list
    ie:
        isvalid_multiline('Am Pentatonic Blues Scale\nPosition X') ->
        (True, ['Am Pentatonic Blues Scale', 'Position X'])

        isvalid_multiline('Am Pentatonic Scale') ->
        (False, ['Am Pentatonic Scale'])
    
    mystr: String, this is the multilabel
    
    return a Tuple:
    - valid_multiline: Boolean, true if multilabel has only 2 substring separated by \n
    - splitted_mystr: List, splitted input string 
    '''
    # split my input multiline string:
    # mystr = 'Am Pentatonic Blues Scale\nPosition 1' ->
    # splitted_mystr = ['Am Pentatonic Blues Scale', 'Position 1']
    splitted_mystr = mystr.split('\n')
    # input multiline string must consist only of two lines (other cases are not supported)
    valid_multiline = False
    if len(splitted_mystr) == 2: valid_multiline = True
    return valid_multiline, splitted_mystr


def get_multilabelparams(mystr, labelfont_family, align_center_flag,
                         multi_label_w=None, multi_label_h=None):
    '''
    Helper function. Given multilabel, font family and 1 param of choice (between
    multi_label_w and multi_label_h) this function calculate the remaining other param.
    ie: multi_label_w -> f() -> multi_label_h
        multi_label_h -> f() -> multi_label_w
        
    mystr: String, this is the multilabel
    labelfont_family: String, multilabel font family
    label_w: Number, label width (optional argument)
    label_h: Number, label height (optional argument)
    
    return a Tuple:
    - valid_multiline: Boolean, true if multilabel has only 2 substring separated by \n
    - myfont_size: Number, multilabel font size
    - multi_label_w: Number, multilabel width
    - multi_label_h: Number, multilabel height
    - intra_labels_offset: Number, distance (px) between the 2 substrings
    - splitted_mystr: List,splitted multilabel by \n
    - substr_dict: Dict, {substring: (substring_w, substring_h), .. }
    '''
    
    # split my input multiline string. input multiline string must consist 
    # only of two lines (other cases are not supported)
    # mystr = 'Am Pentatonic Blues Scale\nPosition 1' ->
    # splitted_mystr = ['Am Pentatonic Blues Scale', 'Position 1']
    # valid_multiline = True
    valid_multiline, splitted_mystr = isvalid_multiline(mystr)
    
    if valid_multiline:
        
        # calculate substrings lenghts
        # substr_list = [['Am Pentatonic Blues Scale', 25], ['Position 1', 10]]
        substr_list = [[elem, len(elem)] for elem in splitted_mystr]
        
        # check if all substrings have same lenght (2 cases same lenght and 
        # same string, same lenght only)
        # ie: substr_list = [['Test Same Lenght', 16], ['Test Same Lenght', 16]]
        # ie: substr_list = [['Test Same Lenght', 16], ['Test Same Xxxxxx', 16]]
        check_all_same_lenght = all((elem[1]==substr_list[0][1]) for elem in substr_list)
        
        # case we have multi_label_w and not multi_label_h
        if multi_label_w and not multi_label_h:
            # if all substrings have same lenght
            if check_all_same_lenght:
                # calculate myfont_size and label_h given substr and multi_label_w
                # throught get_label_h_given_wdth() function
                myfont_size, label_h = mylabels.get_label_h_given_wdth(
                    splitted_mystr[0], multi_label_w, labelfont_family
                    )
                # now create substr_dict, a dict with the 2 substring as keys and a tuple as value. 
                # Tuple is (substring label_w, substring label_h). In case all substrings have same lenght
                # then (substring label_w, substring label_h) are equal for both keys
                # substr_dict = {substring: (substring label_w, substring label_h), .. }
                # substr_dict = {'Test Same Lenght': (75, 4.89)}
                # substr_dict = {'Test Same Lenght': (75, 4.89), 'Test Same Xxxxxx': (75, 4.89)}
                substr_dict = {
                    splitted_mystr[0]: (multi_label_w, label_h), splitted_mystr[1]: (multi_label_w, label_h)
                    }
            # if all substrings have different lenght
            else:
                # Then find bigger and smaller
                # find max substr: substr_lenmax = 'Am Pentatonic Blues Scale'
                substr_lenmax = max(substr_list, key=lambda item:item[1])[0]
                # max substr will have the smaller font size for given multi_label_w, so we will use this
                # to calculate font size for the both lines and calculate label_h also.
                # we will use get_label_h_given_wdth() function to do that, having multi_label_w set
                myfont_size, label_h = mylabels.get_label_h_given_wdth(
                    substr_lenmax, multi_label_w, labelfont_family
                    )
                # find min substr: substr_lenmin = 'Position 1'
                substr_lenmin = min(substr_list, key=lambda item:item[1])[0]
                # now create substr_dict, a dict with the 2 substring as keys and a tuple as value. 
                # Tuple is (substring label_w, substring label_h)
                # substr_dict = {substring: (substring label_w, substring label_h), .. }
                # default alignment is left so, even if the 2 substring label_w are different,
                # shift amount for left align will be proportional (*1/2) to the bigger label width (multi_label_w)
                # for both substring. This is beacuse by default labels are placed on image center_x with 
                # the bottom left corner of label. So they are already aligned left. We only need an equal left shift
                # equal to the amount of multi_label_w/2
                # substr_dict = {'Am Pentatonic Blues Scale': (75, 3.13), 'Position 1': (75, 3.13)}
                substr_dict = {substr_lenmax: (multi_label_w, label_h), substr_lenmin: (multi_label_w, label_h)}    
                # but if align center is True then shift left for smaller substring is proprtional to its
                # smaller label widht. So we use get_labelparams() to calculate it
                if align_center_flag:
                    smaller_label_w = mylabels.get_labelparams(substr_lenmin, labelfont_family, 
                                                            myfont_size=myfont_size)[1]
                    # substr_dict = {'Am Pentatonic Blues Scale': (75, 3.13), 'Position 1': (30, 3.13)}                                        
                    substr_dict[substr_lenmin] = (smaller_label_w, label_h)

            # offset between labels is set to (label_h/2): 0.5 linespace
            intra_labels_offset = label_h / 2.0
            # total multilabel height (width is already fixed by multi_label_w)
            multi_label_h = (2.0 * label_h) + intra_labels_offset
            
        # case we have multi_label_h and not multi_label_w
        if multi_label_h and not multi_label_w:
            # since multi_label_h = label_h + label_h + intra_labels_offset =
            # = label_h + label_h + (label_h/2) = label_h * (5/2)
            label_h = multi_label_h * (2.0/5.0)
            # offset between labels is set to (label_h/2): 0.5 linespace
            intra_labels_offset = label_h / 2.0
            # if all substrings have same lenght
            if check_all_same_lenght:             
                # calculate myfont_size and label_w (= multi_label_w) given substr and label_h
                # throught get_label_w_given_hght() function
                myfont_size, multi_label_w = mylabels.get_label_w_given_hght(
                    splitted_mystr[0], label_h, labelfont_family
                    )
                # now create substr_dict, a dict with the 2 substring as keys and a tuple as value. 
                # Tuple is (substring label_w, substring label_h). In case all substrings have same lenght
                # then (substring label_w, substring label_h) are equal for both keys
                # substr_dict = {substring: (substring label_w, substring label_h), .. }
                # substr_dict = {'Test Same Lenght': (75, 4.89)}
                # substr_dict = {'Test Same Lenght': (75, 4.89), 'Test Same Xxxxxx': (75, 4.89)}       
                substr_dict = {
                    splitted_mystr[0]: (multi_label_w, label_h), splitted_mystr[1]: (multi_label_w, label_h)
                    }
            # if all substrings have different lenght
            else:
                # Then find bigger and smaller
                # find max substr: substr_lenmax = 'Am Pentatonic Blues Scale'
                substr_lenmax = max(substr_list, key=lambda item:item[1])[0]
                # max substr will have the smaller font size for given label_h, so we will use this
                # to calculate font size for the other line and calculate multi_label_w also.
                # we will use get_label_w_given_hght() function to do that having label_h
                myfont_size, multi_label_w = mylabels.get_label_w_given_hght(
                    substr_lenmax, label_h, labelfont_family
                    )
                # find min substr: substr_lenmin = 'Position 1'
                substr_lenmin = min(substr_list, key=lambda item:item[1])[0]
                # now create substr_dict, a dict with the 2 substring as keys and a tuple as value. 
                # Tuple is (substring label_w, substring label_h)
                # substr_dict = {substring: (substring label_w, substring label_h), .. }
                # default alignment is left so, even if the 2 substring label_w are different,
                # shift amount for left align will be proportional (*1/2) to the bigger label width (multi_label_w)
                # for both substring. This is beacuse by default labels are placed on image center_x with 
                # the bottom left corner of label. So they are already aligned left. We only need an equal left shift
                # equal to the amount of multi_label_w/2
                # substr_dict = {'Am Pentatonic Blues Scale': (75, 3.13), 'Position 1': (75, 3.13)}
                substr_dict = {substr_lenmax: (multi_label_w, label_h), substr_lenmin: (multi_label_w, label_h)}
                # but if align center is True then shift left for smaller substring is proprtional to its 
                # smaller label widht. So we use get_labelparams() to calculate it  
                if align_center_flag:
                    temp_label_w = mylabels.get_labelparams(substr_lenmin, labelfont_family, 
                                                            myfont_size=myfont_size)[1]
                    # substr_dict = {'Am Pentatonic Blues Scale': (75, 3.13), 'Position 1': (30, 3.13)}
                    substr_dict[substr_lenmin] = (temp_label_w, label_h)
                    
        # return all params
        return (
            valid_multiline, myfont_size, 
            multi_label_w, multi_label_h, 
            intra_labels_offset, splitted_mystr, substr_dict            
            )
               
    # if input multiline string do not have two lines only, then
    # treat it like a single line and get_multilabelparams() 
    # default to get_labelparams() function
    # (intra_labels_offset, splitted_mystr, substr_dict are set to None)
    else:
        myfont_size, label_w, label_h = mylabels.get_labelparams(mystr, labelfont_family, 
                                        label_w=multi_label_w, label_h=multi_label_h
                                        )
        return (
            valid_multiline, myfont_size, 
            label_w, label_h, 
            None, splitted_mystr, None
            )
        
def get_multilabel_h_given_wdth(mystr, multi_label_w, labelfont_family):
    """
    Estimate multilabel height and font size from multilabel string 
    and multilabel width using get_multilabelparams() helper function.
    Note, get_multilabelparams returns:
    (
    valid_multiline, myfont_size, 
    multi_label_w, multi_label_h, 
    intra_labels_offset, splitted_mystr, substr_dict            
    )

    mystr: String, this is the label 
    multi_label_w: Number, multilabel width
    labelfont_family: String, label font family

    return a tuple of (font size, multilabel height) 
    """
    # use get_multilabelparams() helper function and
    # get only myfont_size and multi_label_h params
    (
      _, myfont_size, 
      _, multi_label_h, 
      _, _, _
    ) = get_multilabelparams(mystr, labelfont_family, False,
                             multi_label_w=multi_label_w)
    return myfont_size, multi_label_h
    

def my2linelabel_given_wdth(dwg, mycenter, mystr, multi_label_w,
             font_weight, font_family, 
             align_center_flag=True,
             fill="black", fill_opacity='1',
             stroke="none", stroke_width="0",
             edge_debug=False):
    """
    Draw a 2 line Label with fixed width equal to single line width
    (label_w), also return multi_label_h

    dwg: Svgwrite object
    mycenter: Tuple, label center (x, y) 
    mystr: String, this is the multi-label, line separation is '\n'
    multi_label_w: Number, multi label width
    font_weight: String, font weight
    font_family: String, font family
    align_center_flag: Boolean, if true align center the lines 
    fill: String, square fill color
    fill_opacity: String, square fill opacity value
    stroke: String, square stroke color
    stroke_width: String, square stroke width
    edge_debug: Boolean, if true draw label contour

    return Number: multi_label_h, total multi label height
    """
    # use get_multilabelparams() helper function to get all params having multi_label_w as input
    (
     valid_multiline, myfont_size, 
     multi_label_w, multi_label_h, 
     intra_labels_offset, 
     splitted_mystr, substr_dict
    ) = get_multilabelparams(mystr, font_family, align_center_flag, 
                             multi_label_w=multi_label_w)
    
    if valid_multiline:
        
        # remeber, splitted_mystr = [substring1, substring2]
        # and substr_dict = {substring1: (substring1 label_w, substring1 label_h), substring2: (... }
        substr1_w, _ = substr_dict[splitted_mystr[0]]
        substr2_w, substr2_h = substr_dict[splitted_mystr[1]]
        # starting points for text labels, they are placed at the left bottom corner of a single label 
        # (that is why we need to shift left by substrx_w/2 from center to align)
        str_start_point1 = (mycenter[0] - (substr1_w/2), mycenter[1] - (intra_labels_offset / 2))
        str_start_point2 = (mycenter[0] - (substr2_w/2), mycenter[1] + (intra_labels_offset / 2) + substr2_h)
        
        if edge_debug:
            dwg.add(
                dwg.circle(
                    center=mycenter, r=1.5, fill="red", fill_opacity="0.5", 
                    stroke="red",  stroke_width="0"
                    )
                )
            dwg.add(
                dwg.circle(
                    center=str_start_point1, r=1.5, fill="blue", fill_opacity="0.5", 
                    stroke="red",  stroke_width="0"
                    )
                )
            dwg.add(
                dwg.circle(
                    center=str_start_point2, r=1.5, fill="blue", fill_opacity="0.5", 
                    stroke="blue", stroke_width="0"
                    )
                )
            myshapes.mysquare(
                dwg, mycenter, 
                (multi_label_w, multi_label_h), 
                stroke="red", stroke_width="0.5"
                )
            
        my_text0 = dwg.text(
              splitted_mystr[0]
            , insert=str_start_point1
            , stroke=stroke
            , stroke_width=stroke_width
            , fill=fill
            , fill_opacity=fill_opacity
            , font_size=myfont_size
            , font_weight=font_weight
            , font_family=font_family
        )
        my_text0.update(
            {'xml:space' : 'preserve'}
        ) 
        dwg.add(my_text0)
        
        my_text1 = dwg.text(
              splitted_mystr[1]
            , insert=str_start_point2
            , stroke=stroke
            , stroke_width=stroke_width
            , fill=fill
            , fill_opacity=fill_opacity
            , font_size=myfont_size
            , font_weight=font_weight
            , font_family=font_family
        )
        my_text1.update(
            {'xml:space' : 'preserve'}
        ) 
        dwg.add(my_text1)

    # if input multiline string consist of 1 line then fallback to
    # mylabel_given_wdth(), at this moment no support for multilines > 2 lines
    else:
        multi_label_h = mylabels.mylabel_given_wdth(
              dwg
            , mycenter
            , mystr
            , multi_label_w
            , font_weight
            , font_family
            , fill=fill
            , fill_opacity=fill_opacity
            , stroke=stroke
            , stroke_width=stroke_width
            , edge_debug=edge_debug
            )
        
    return multi_label_h


def get_multilabel_w_given_hght(mystr, multi_label_h, labelfont_family):
    """
    Estimate multilabel width and font size from multilabel string 
    and multilabel height using get_multilabelparams() helper function.
    Note, get_multilabelparams returns:
    (
    valid_multiline, myfont_size, 
    multi_label_w, multi_label_h, 
    intra_labels_offset, splitted_mystr, substr_dict            
    )

    mystr: String, this is the label 
    multi_label_h: Number, multilabel height
    labelfont_family: String, label font family

    return a tuple of (font size, multilabel width) 
    """
    # use get_multilabelparams() helper function and
    # get only myfont_size and multi_label_w params
    (
      _, myfont_size, 
      multi_label_w, _, 
      _, _, _
    ) = get_multilabelparams(mystr, labelfont_family, False,
                             multi_label_h=multi_label_h)
    return myfont_size, multi_label_w


def my2linelabel_given_hght(dwg, mycenter, mystr, multi_label_h,
             font_weight, font_family, 
             align_center_flag=True,
             fill="black", fill_opacity='1',
             stroke="none", stroke_width="0",
             edge_debug=False):
    """
    Draw a 2 line Label with fixed height also return multi_label_w

    dwg: Svgwrite object
    mycenter: Tuple, label center (x, y) 
    mystr: String, this is the multi-label, line separation is '\n'
    multi_label_h: Number, multi label height
    font_weight: String, font weight
    font_family: String, font family
    align_center_flag: Boolean, if true align center the lines 
    fill: String, square fill color
    fill_opacity: String, square fill opacity value
    stroke: String, square stroke color
    stroke_width: String, square stroke width
    edge_debug: Boolean, if true draw label contour

    return Number: multi_label_w, total multi label width
    """        
    # use get_multilabelparams() helper function to get all params having multi_label_h as input
    (
     valid_multiline, myfont_size, 
     multi_label_w, multi_label_h, 
     intra_labels_offset, 
     splitted_mystr, substr_dict
    ) = get_multilabelparams(mystr, font_family, align_center_flag, 
                             multi_label_h=multi_label_h)
    
    if valid_multiline:
        
        # remeber, splitted_mystr = [substring1, substring2]
        # and substr_dict = {substring1: (substring1 label_w, substring1 label_h), substring2: (... }
        substr1_w, _ = substr_dict[splitted_mystr[0]]
        substr2_w, substr2_h = substr_dict[splitted_mystr[1]]        

        # starting points for text labels, they are placed at the left bottom corner of a single label 
        # (that is why we need to shift left by substrx_w/2 from center to align)
        str_start_point1 = (mycenter[0] - (substr1_w/2), mycenter[1] - (intra_labels_offset / 2))
        str_start_point2 = (mycenter[0] - (substr2_w/2), mycenter[1] + (intra_labels_offset / 2) + substr2_h)
        
        if edge_debug:
            dwg.add(
                dwg.circle(
                    center=mycenter, r=1.5, fill="red", fill_opacity="0.5", 
                    stroke="red",  stroke_width="0"
                    )
                )
            dwg.add(
                dwg.circle(
                    center=str_start_point1, r=1.5, fill="blue", fill_opacity="0.5", 
                    stroke="red",  stroke_width="0"
                    )
                )
            dwg.add(
                dwg.circle(
                    center=str_start_point2, r=1.5, fill="blue", fill_opacity="0.5", 
                    stroke="blue", stroke_width="0"
                    )
                )
            myshapes.mysquare(
                dwg, mycenter, 
                (multi_label_w, multi_label_h), 
                stroke="red", stroke_width="0.5"
                )
        
        my_text0 = dwg.text(
              splitted_mystr[0]
            , insert=str_start_point1
            , stroke=stroke
            , stroke_width=stroke_width
            , fill=fill
            , fill_opacity=fill_opacity
            , font_size=myfont_size
            , font_weight=font_weight
            , font_family=font_family
        )
        my_text0.update(
            {'xml:space' : 'preserve'}
        ) 
        dwg.add(my_text0)
        
        my_text1 = dwg.text(
              splitted_mystr[1]
            , insert=str_start_point2
            , stroke=stroke
            , stroke_width=stroke_width
            , fill=fill
            , fill_opacity=fill_opacity
            , font_size=myfont_size
            , font_weight=font_weight
            , font_family=font_family
        )
        my_text1.update(
            {'xml:space' : 'preserve'}
        ) 
        dwg.add(my_text1)
        
    # if input multiline string consist of 1 line then fallback to
    # mylabel_given_hght(), at this moment no support for multilines > 2 lines
    elif len(splitted_mystr) == 1:
        multi_label_w = mylabels.mylabel_given_hght(
              dwg
            , mycenter
            , mystr
            , multi_label_h
            , font_weight
            , font_family
            , fill=fill
            , fill_opacity=fill_opacity
            , stroke=stroke
            , stroke_width=stroke_width
            , edge_debug=edge_debug
            )
        
    return multi_label_w


if __name__ == "__main__":
    
    # testing this functions
    
    print('isvalid_multiline("Am Pentatonic Blues Scale\\nPosition X"):\n- ',
        isvalid_multiline('Am Pentatonic Blues Scale\nPosition X')
        )
    
    import svgwrite
    
    dwg = svgwrite.Drawing(filename='../dirout/multilabels_test.svg', size=(180, 130), debug=True)

    font_family="Ubuntu Mono"
    # font_family="Courier New"
    # font_family="Liberation Mono"
    # font_family="DejaVu Sans Mono"
    
    # --- given_wdth tests ---
    
    print('get_multilabelparams(multi_label_w=150):\n- ',
        get_multilabelparams('Am Pentatonic Blues Scale\nPosition X', font_family, True, multi_label_w=150)
        )
    print('get_multilabel_h_given_wdth(multi_label_w=150):\n- ',
        get_multilabel_h_given_wdth('Am Pentatonic Blues Scale\nPosition X', 150, font_family)
        )
    print('my2linelabel_given_wdth(multi_label_w=150, align_center = False):\n- ',
        my2linelabel_given_wdth(dwg, (90, 20), 'Am Pentatonic Blues Scale\nPosition 1', 150,
                               font_weight="bold", font_family=font_family, 
                               align_center_flag = False, edge_debug=True)
        )
    print('my2linelabel_given_wdth(multi_label_w=150, align_center = True):\n- ',
        my2linelabel_given_wdth(dwg, (90, 50), 'Am Pentatonic Blues Scale\nPosition 2', 150,
                               font_weight="bold", font_family=font_family, 
                               align_center_flag = True, edge_debug=True)
        )

    # --- given_hght tests ---

    print('get_multilabelparams(multi_label_h=13):\n- ',
        get_multilabelparams('Am Pentatonic Blues Scale\nPosition X', font_family, True, multi_label_h=13)
        )
    print('get_multilabel_w_given_hght(multi_label_h=13):\n- ',
        get_multilabel_w_given_hght('Am Pentatonic Blues Scale\nPosition X', 13, font_family)
        )
    print('my2linelabel_given_hght(multi_label_h=13, align_center = False):\n- ',
        my2linelabel_given_hght(dwg, (90, 80), 'Am Pentatonic Blues Scale\nPosition 1', 13,
                               font_weight="bold", font_family=font_family, 
                               align_center_flag = False, edge_debug=True)
        )
    print('my2linelabel_given_hght(multi_label_h=13, align_center = True):\n- ',
        my2linelabel_given_hght(dwg, (90, 110), 'Am Pentatonic Blues Scale\nPosition 2', 13,
                               font_weight="bold", font_family=font_family, fill_opacity='0.5',
                               align_center_flag = True, edge_debug=True)
        )

    dwg.save()
