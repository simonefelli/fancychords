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


# local application imports
from libs import myshapes
from libs import mylabels


def mydot(dwg, mycenter,
          label, labelfont_weight, labelfont_family,
          radius, square, sq_rotate,
          dotfill='black',
          dotfill_opacity='1',
          dotstroke='black',
          dotstroke_opacity='1',
          dotstroke_width='3',
          dotstroke_dasharray='none',
          labelfill='white',
          labelfill_opacity='1'
          ):
    
    """
    Draw Single Note Dot

    dwg: Svgwrite object
    mycenter: Tuple, dot center (x, y)
    label: String, label inside dot
    labelfont_weight: String, font weight
    labelfont_family: String, font family
    radius: Number, dot radius
    square: Boolean, if true draw square
    sq_rotate: Boolean, if true rotate square by 90 deg
    dotfill: String, Dot fill color
    dotfill_opacity: String, Dot fill opacity value
    dotstroke: String, Dot stroke color
    dotstroke_opacity: String, Dot stroke fill opacity value
    dotstroke_width: String, Dot stroke width
    dotstroke_dasharray: String, Dot stroke pattern of dashes and gaps, "0" to disable
    labelfill: String, label color inside dot
    labelfill_opacity: String, label fill opacity value

    return nothing
    """
    nchars = len(label)
    if square:
        sqrwdth = 2 * radius
        myshapes.mysquare(dwg, mycenter, (sqrwdth, sqrwdth),
                 rotate=sq_rotate,
                 fill=dotfill,
                 fill_opacity=dotfill_opacity,
                 stroke=dotstroke,
                 stroke_opacity=dotstroke_opacity,
                 stroke_width=dotstroke_width,
                 stroke_dasharray=dotstroke_dasharray)
        if label: mylabels.mylabel_given_wdth(dwg, mycenter, label, 
                            myshapes.square2font(sqrwdth, nchars),
                            fill=labelfill, fill_opacity=labelfill_opacity, 
                            font_weight=labelfont_weight,
                            font_family=labelfont_family, edge_debug=False)
    else:
        myshapes.mycircle(dwg, mycenter, radius,
                 fill=dotfill,
                 fill_opacity=dotfill_opacity,
                 stroke=dotstroke,
                 stroke_opacity=dotstroke_opacity,
                 stroke_width=dotstroke_width,
                 stroke_dasharray=dotstroke_dasharray)
        if label: mylabels.mylabel_given_wdth(dwg, mycenter, label, 
                            myshapes.circle2font(radius, nchars),
                            fill=labelfill, fill_opacity=labelfill_opacity,
                            font_weight=labelfont_weight,
                            font_family=labelfont_family, edge_debug=False)


if __name__ == "__main__":
    
    # testing this functions
    
    import svgwrite
    
    sqr_wdth = 30.0
    crcl_rad = sqr_wdth / 2.0
    
    dwg = svgwrite.Drawing(filename='../dirout/dots_test.svg', size=(155, 200), debug=True)

    test_label1 = 'X'
    test_label2 = 'X'
    test_label3 = 'X'
    test_label4 = 'X'
    font_family='Ubuntu Mono Legacy'
    # font_family='Courier New'
    # font_family='Liberation Mono'
    # font_family = 'DejaVu Sans Mono'

    mydot(dwg, (30, 30), test_label1
          , labelfont_weight='bold'
          , labelfont_family=font_family
          , radius = (sqr_wdth / 2)
          , square=True
          , sq_rotate=False
          , dotfill='lightgrey'
          , dotstroke='black'
          , dotstroke_width='3'
          , labelfill='black'
          )

    mydot(dwg, (80, 30), test_label1 * 2
          , labelfont_weight='bold'
          , labelfont_family=font_family
          , radius = (sqr_wdth / 2)
          , square=True
          , sq_rotate=False
          , dotfill='black'
          , dotstroke='black'
          , dotstroke_width='3'
          , labelfill='white'
          )

    mydot(dwg, (130, 30), test_label1 * 3
          , labelfont_weight='bold'
          , labelfont_family=font_family
          , radius = crcl_rad
          , square=True
          , sq_rotate=False
          , dotfill='black'
          , dotstroke='black'
          , dotstroke_width='3'
          , labelfill='white'
          )

    mydot(dwg, (30, 80), test_label2
          , labelfont_weight='bold'
          , labelfont_family=font_family
          , radius = crcl_rad
          , square=True
          , sq_rotate=False
          , dotfill='white'
          , dotstroke='black'
          , dotstroke_width='2'
          , dotstroke_dasharray='5,3'
          , labelfill='black'
          )
    
    mydot(dwg, (80, 80), test_label2 * 2
          , labelfont_weight='bold'
          , labelfont_family=font_family
          , radius = crcl_rad
          , square=True
          , sq_rotate=False
          , dotfill='white'
          , dotstroke='black'
          , dotstroke_width='2'
          , dotstroke_dasharray='5,3'
          , labelfill='black'
          )

    mydot(dwg, (130, 80), test_label2 * 3
          , labelfont_weight='bold'
          , labelfont_family=font_family
          , radius = crcl_rad
          , square=True
          , sq_rotate=False
          , dotfill='white'
          , dotstroke='black'
          , dotstroke_width='2'
          , dotstroke_dasharray='5,3'
          , labelfill='black'
          )

    mydot(dwg, (30, 120), test_label3
          , labelfont_weight='bold'
          , labelfont_family=font_family
          , radius = crcl_rad
          , square=False
          , sq_rotate=False
          , dotfill='black'
          , dotstroke='black'
          , dotstroke_width='3'
          , labelfill='white'
          )
    
    mydot(dwg, (80, 120), test_label3 * 2
          , labelfont_weight='bold'
          , labelfont_family=font_family
          , radius = crcl_rad
          , square=False
          , sq_rotate=False
          , dotfill='black'
          , dotstroke='black'
          , dotstroke_width='3'
          , labelfill='white'
          )

    mydot(dwg, (130, 120), test_label3 * 3
          , labelfont_weight='bold'
          , labelfont_family=font_family
          , radius = crcl_rad
          , square=False
          , sq_rotate=False
          , dotfill='black'
          , dotstroke='black'
          , dotstroke_width='3'
          , labelfill='white'
          )

    mydot(dwg, (30, 170), test_label4
          , labelfont_weight='bold'
          , labelfont_family=font_family
          , radius = crcl_rad
          , square=False
          , sq_rotate=False
          , dotfill='white'
          , dotfill_opacity='0.2'
          , dotstroke='black'
          , dotstroke_width='2'
          , dotstroke_dasharray='5,3'
          , labelfill='black'
          )
    
    mydot(dwg, (80, 170), test_label4 * 2
          , labelfont_weight='bold'
          , labelfont_family=font_family
          , radius = crcl_rad
          , square=False
          , sq_rotate=False
          , dotfill='white'
          , dotstroke='black'
          , dotstroke_width='2'
          , dotstroke_dasharray='5,3'
          , dotstroke_opacity='0.5'
          , labelfill='black'
          )

    mydot(dwg, (130, 170), test_label4 * 3
          , labelfont_weight='bold'
          , labelfont_family=font_family
          , radius = crcl_rad
          , square=False
          , sq_rotate=False
          , dotfill='white'
          , dotstroke='black'
          , dotstroke_width='2'
          , dotstroke_dasharray='5,3'
          , labelfill='black'
          , labelfill_opacity='0.5'
          )

    dwg.save()
