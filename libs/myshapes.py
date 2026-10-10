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


def square2font(square, nchars):
    """
    Given dot square get font size

    square: Number, square lenght  
    nchars: Number, lenght in chars of dot label
    
    return font size
    """       
    weight_dict = {1: 1.95, 2: 1.15, 3: 1.10, 4: 1.10}
    return (square/weight_dict[nchars])


def circle2font(radius, nchars):
    """
    Given radius dot get font size

    radius: Number, dot radius
    nchars: Number, lenght in chars of dot label
    
    return font size
    """           
    weight_dict = {1: 1.10, 2: 0.70, 3: 0.61, 4: 0.65}
    return (radius/weight_dict[nchars])


def mycircle(dwg, mycenter, radius, stroke_width,
             fill='none', fill_opacity='1',
             stroke='black', stroke_opacity='1', stroke_dasharray='none'):
    """
    Draw Single Circle

    dwg: Svgwrite object
    mycenter: Tuple, circle center (x, y) 
    radius: Number, circle radius
    stroke_width: String, circle stroke width
    fill: String, circle fill color
    fill_opacity: String, circle fill opacity value
    stroke: String, circle stroke color
    stroke_opacity: String, circle stroke fill opacity value
    stroke_dasharray: String, circle stroke pattern of dashes and gaps, '0' to disable

    return nothing
    """
    dwg.add(
        dwg.circle(
              center=mycenter
            , r=radius
            , fill=fill
            , fill_opacity=fill_opacity
            , stroke=stroke
            , stroke_width=stroke_width
            , stroke_dasharray=stroke_dasharray
            , stroke_opacity=stroke_opacity
            )
        )


def mysquare(dwg, mycenter, wh, stroke_width,
             rotate=False, fill='none', fill_opacity='1',
             stroke='black', stroke_opacity='1', stroke_dasharray='none'):
    """
    Draw Single Square

    dwg: Svgwrite object
    mycenter: Tuple, square center (x, y) 
    wh: Tuple, (square width, square heigth) 
    stroke_width: String, square stroke width
    rotate: Boolean, if true rotate square by 90 deg
    fill: String, square fill color
    fill_opacity: String, square fill opacity value
    stroke: String, square stroke color
    stroke_opacity: String, square stroke fill opacity value
    stroke_dasharray: String, square stroke pattern of dashes and gaps, '0' to disable

    return nothing
    """    
    w = wh[0]
    h = wh[1]
    if rotate:
        # svg transform function to rotate
        mytransform = 'rotate(45,' + str(mycenter[0]) + ',' + str(mycenter[1]) + ')'
    else:
        mytransform = 'rotate(0)'
    dwg.add(
        dwg.rect(
                (mycenter[0] - (w/2), mycenter[1] - (h/2))
              , (w, h)
              , fill=fill
              , fill_opacity=fill_opacity
              , stroke=stroke
              , stroke_width=stroke_width
              , stroke_dasharray=stroke_dasharray
              , stroke_opacity=stroke_opacity
              , transform=mytransform
              )
        )


def add_arrow_endmarker(dwg, marker_name, 
                        arrow_fill_color='black', 
                        arrow_fill_opacity='1'):
    '''
    Add an arrow end marker def in dwg definition that can be used to draw arrows
    
    dwg: Svgwrite object
    marker_name: String, unique name of arrow marker
    arrow_fill_color: String, arrow marker color
    arrow_fill_opacity: String, arrow fill opacity value
    
    return: String, marker FuncIRI reference of the object. (i.e. 'url(#id)')
            used in myarrow() function to reference marker end arrow
    '''
    marker_w = 4.5
    marker_h = marker_w
    # 'M0,0 L0,4 L6,2 z'
    # see http://vanseodesign.com/web-design/svg-markers/
    path_d = 'M0,0 L0,' + str(marker_h) + ' L' + str(marker_w) + ',' + str(marker_h/2) + ' z'
    arrow_end = dwg.marker(
          id=marker_name
        , insert=(marker_w*0.7, marker_h/2)
        , size=(marker_w, marker_h)
        , orient='auto'
        , markerUnits='strokeWidth'
        )
    arrow_end.add(
        dwg.path(
              d=path_d
            , stroke_width='0'  
            , fill=arrow_fill_color
            , fill_opacity=arrow_fill_opacity
        )
    )
    dwg.defs.add(arrow_end)
    return arrow_end.get_funciri()


def add_arrow_startmarker(dwg, marker_name, 
                          arrow_fill_color='black', 
                          arrow_fill_opacity='1'):
    '''
    Add an arrow start marker def in dwg definition that can be used to draw arrows
    
    dwg: Svgwrite object
    marker_name: String, unique name of arrow marker
    arrow_fill_color: String, arrow marker color
    arrow_fill_opacity: String, arrow fill opacity value
    
    return: String, marker FuncIRI reference of the object. (i.e. 'url(#id)')
            used in myarrow() function to reference marker start arrow
    '''
    marker_w = 4.5
    marker_h = marker_w
    # 'M6,4 L6,0 L0,2 z'
    # see http://vanseodesign.com/web-design/svg-markers/
    path_d = 'M' + str(marker_w) + ',' + str(marker_h) + ' L' + str(marker_w) + ',0 L0,' + str(marker_h/2) + ' z'
    arrow_start = dwg.marker(
          id=marker_name
        , insert=(marker_w*0.3, marker_h/2)
        , size=(marker_w, marker_h)
        , orient='auto'
        , markerUnits='strokeWidth'
        )
    arrow_start.add(
        dwg.path(
              d=path_d
            , stroke_width='0'  
            , fill=arrow_fill_color
            , fill_opacity=arrow_fill_opacity
            )
        )
    dwg.defs.add(arrow_start)
    return arrow_start.get_funciri()


def basic_arrow(dwg, start, end, bezier, bez_median, strk_wdth, 
                line_stroke_color='black', line_stroke_opacity='1', 
                start_end_flag='e', arrow_stroke_dasharray=None):
    '''
    Draw a basic single/double arrow
    
    dwg: Svgwrite object
    start: Tuple, start point (x, y)
    end: Tuple, end point
    bezier: Boolean, if true draw a bezier curve (a small arc) instead of a straight line
    bez_median: Q value of bezier string (see code), usually proportional to median point
                between start and end
    strk_wdth: Number, line stroke width
    line_stroke_color: String, line stroke color
    line_stroke_opacity: String, line fill opacity value
    start_end_flag: String, parameter to enable/disable arrowheads, ie:
        start_end_flag = ''   -> no arrowheads
        start_end_flag = 's'  -> start arrowheads
        start_end_flag = 'e'  -> end arrowheads
        start_end_flag = 'se' -> start and end arrowheads
    arrow_stroke_dasharray: String, dot stroke pattern of dashes and gaps
                            'dashes' to enable and None to disable
    '''

    # initialize arrow funciri start/end
    arrow_fstart = 'none'
    arrow_fend   = 'none'

    # if start_end_flag = 's' -> start arrow only
    # if start_end_flag = 'e' -> end arrow only
    # if start_end_flag = 'se' -> start arrow + end arrow
    # if start_end_flag = '' -> no arrows
    if 's' in start_end_flag:
        # arrow_fstart: FuncIRI reference of the start marker object (see add_arrow_xx() funct.)
        arrow_fstart = add_arrow_startmarker(
              dwg
            , 'marker_' + line_stroke_color + '_start'
            , arrow_fill_color=line_stroke_color
            , arrow_fill_opacity=line_stroke_opacity
            )
    if 'e' in start_end_flag:
        #  arrow_fend: FuncIRI reference of the end  marker object (see add_arrow_xx() funct.)
        arrow_fend = add_arrow_endmarker(
              dwg
            , 'marker_' + line_stroke_color + '_end'
            , arrow_fill_color=line_stroke_color
            , arrow_fill_opacity=line_stroke_opacity
            )

    # if arrow_stroke_dasharray is set to keyword 'dashes' then set stroke_dasharray
    if arrow_stroke_dasharray == 'dashes':
        stroke_dasharray = str(strk_wdth*1.6)
    else:
        stroke_dasharray = '0'


    pt1_x, pt1_y = start
    pt2_x, pt2_y = end
    

    # if bezier is True draw an arc else a stright line (however diagonals
    # are straight lines)
    if bezier and bez_median:
        # calculate median point
        pt_median_x, pt_median_y = bez_median
        
        # --------------------------------------------
        # M - move to the specified coordinate. This is the starting point of the curve
        # Q - quadratic Bézier curve from the current point to (x,y) using (x1,y1) as the control point
        # bezstring = 'M2,2 Q5,3 8,2': 
        # - Pick up the pen and Move it to { x: 2, y: 2 }
        # - Put down the pen and Draw a quadratic Bézier curve from the current point to 
        #   a new point { x: 8, y: 2 }. The control point is { x: 5, y: 3 }
        # https://svg-path-visualizer.netlify.app/
        bezstring = 'M' +  str(pt1_x) + ',' + str(pt1_y) + \
                    ' Q' + str(pt_median_x) + ',' +  str(pt_median_y) + \
                    ' ' +  str(pt2_x) + ',' + str(pt2_y)
        mypath = dwg.path(
              d=bezstring
            , fill='none'
            , fill_opacity=line_stroke_opacity
            , stroke_width=strk_wdth*0.67
            , stroke=line_stroke_color            
            , stroke_opacity=line_stroke_opacity
            , stroke_dasharray=stroke_dasharray
            , marker_start=arrow_fstart
            , marker_end=arrow_fend
        )
        dwg.add(mypath)
    else:
        # pt1_offset_x, pt1_offset_y, pt2_offset_x, pt2_offset_y = 0, 0, 0, 0  
        # to remove offsets for testing
        myline = dwg.line(
              start = (pt1_x, pt1_y)
            , end =   (pt2_x, pt2_y)
            , fill=line_stroke_color
            , fill_opacity=line_stroke_opacity
            , stroke_width=strk_wdth*0.67
            , stroke_dasharray=stroke_dasharray            
            , stroke=line_stroke_color
            , stroke_opacity=line_stroke_opacity
            , marker_start=arrow_fstart
            , marker_end=arrow_fend
            )
        dwg.add(myline)



if __name__ == "__main__":
    
    # testing this functions
    
    import svgwrite
    
    sqr_wdth = 30.0
    crcl_rad = sqr_wdth/2.0
    
    dwg = svgwrite.Drawing(filename='../dirout/shapes_test.svg', size=(160, 210), debug=True)
    
    # testing mysquare and mycircle
     
    mysquare(dwg, (30, 30), (sqr_wdth, sqr_wdth),
             rotate=False,
             fill='lightgrey', fill_opacity='1',
             stroke='black', stroke_width='3', stroke_opacity='1',
             stroke_dasharray='none')

    mysquare(dwg, (80, 30), (sqr_wdth, sqr_wdth),
             rotate=False,
             fill='black', fill_opacity='1',
             stroke='black', stroke_width='3', stroke_opacity='1',
             stroke_dasharray='none')

    mysquare(dwg, (130, 30), (sqr_wdth, sqr_wdth),
             rotate=True,
             fill='white', fill_opacity='0.5',
             stroke='black', stroke_width='3', stroke_opacity='1',
             stroke_dasharray='5')

    mycircle(dwg, (30, 80), crcl_rad,
                 fill='lightgrey', fill_opacity='1',
                 stroke='black', stroke_width='1', stroke_opacity='1',
                 stroke_dasharray='none')

    mycircle(dwg, (80, 80), crcl_rad,
                 fill='black', fill_opacity='1',
                 stroke='black', stroke_width='3', stroke_opacity='1',
                 stroke_dasharray='none')

    mycircle(dwg, (130, 80), crcl_rad,
                 fill='white', fill_opacity='1',
                 stroke='black', stroke_width='3', stroke_opacity='1',
                 stroke_dasharray='4')


    # testing basic_arrow
    
    strk_wdth = 3  # line/dot tickness
    start_end_flag = 'e' # 'se', 's', 'e', ''
    
    basic_arrow(dwg, (30,110), (130, 200), False, None, strk_wdth, 
                'blue', '1.0', start_end_flag, None)

    start_end_flag = 'se' # 'se', 's', 'e', ''
    basic_arrow(dwg, (30, 200), (130,110), True, (70, 130), strk_wdth, 
                'red', '0.4', start_end_flag, 'dashes')

    dwg.save()
