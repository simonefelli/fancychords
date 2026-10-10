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
from libs import global_constants
from libs import global_utilities

def parse_chord_name(chord_name):
    '''
    given a chord name return root_note, quality, detail, slash_note
    chord name can be in english or latin notation
    ie: 
        parse_chord_name(FA#m(no5)/SOLb) -> ('FA#', 'm', '(no5)', 'SOLb')
        parse_chord_name(Gbmaj9/D#)      -> ('Gb', 'maj9', '', 'D#')
        parse_chord_name(Gmaj7b5)        -> ('G', 'maj7b5', '', '')
    
    chord_name: String, chord name
    
    return: root_note, quality, detail, slash_note
    '''
    len_chord_name = len(chord_name)
    notes_latin_chk = ['DO', 'RE', 'MI', 'FA', 'SO', 'LA', 'SI']
    root_note, quality_detail_slash, quality, detail, slash_note = '', '', '', '', ''
    # if chord_name is just 1 letter then it's english notation
    if len_chord_name == 1:
        root_note = chord_name
    # handle latin notation case
    elif chord_name[:2] in notes_latin_chk:
        if chord_name[:2] == 'SO':
            root_note = 'SOL'
            quality_detail_slash = chord_name[3:]
        else:
            root_note = chord_name[:2]
            quality_detail_slash = chord_name[2:]
    # english notation case, when chord_name has more than 1 letter
    else:
        root_note = chord_name[0]
        quality_detail_slash = chord_name[1:]
    # check if chord name has sharp or flat
    if quality_detail_slash:
        if quality_detail_slash[0] in ('b', '#'):
            # add 'b's or '#'s to root_note
            root_note += quality_detail_slash[0]
            # remove 'b's or '#'s from quality_detail_slash
            quality_detail_slash = quality_detail_slash[1:]
    if quality_detail_slash:
        # if there is a slash note remove '/' from quality
        # and add it to slash_note
        if '/' in quality_detail_slash:
            slash_pos = quality_detail_slash.index('/')
            slash_note = quality_detail_slash[slash_pos + 1:]
            quality = quality_detail_slash[:slash_pos]
        else:
            quality = quality_detail_slash
        # if there is a '(no5)' remove it from quality
        # and add it to detail
        detail = ''
        if '(no5)' in quality:
            quality = quality.replace('(no5)', '')
            detail = '(no5)' + detail
        # if there is a '(no3)' remove it from quality
        # and add it to detail
        if '(no3)' in quality:
            quality = quality.replace('(no3)', '')
            detail = '(no3)' + detail

    return (root_note, quality, detail, slash_note)


def check_fretlist_correct(fretlist):
    '''
    check if frets string is correct
    ie:
    - there must be 6 elements 
    - all elements are numbers between 0 and 24
      or, if char, only 'x' or 'X'
    
    fretlist: List of strings, fret sequence ie: ['x', '3', '2', '0', '1', '0']
    
    return boolean correct variable
    '''
    correct = True
    if len(fretlist) != 6:
        correct = False
    else:
        for el in fretlist:
            if el.isdigit():
                el_int = int(el)
                correct = correct and ((el_int >= 0) and (el_int <= 24))
            else:
                correct = correct and (el.lower() == 'x')
    return correct


def check_crd_params(chord_name, frets, fingers, intervals, dlabels, footer, subfolder):
    '''
    check if chord main parameters are correct and return
    them stripped (start and/or ending whitespaces removed)
    only chord_name, frets are mandatory
    if a non mandatory parameters is to be given but some 
    preceding ones are to be skipped use '%' or null
    
    chord_name: String, chord name ie: 'G#dim7(no5)/F#'
    frets: String, fret sequence ie: '2,2,0,1,0,1'
    fingers: String, finger numbers list ie: '3,4,x,1,x,2'
    intervals: List of strings, interval sequence ie: 'b7,b3,b5,R,b3,bb7'
    dlabels: String, dot labels sequence ie: '3,4,x,1,x,2'
    footer: List of strings, footer sequence ie: 'b7,b3,b5,R,b3,bb7'
    subfolder: String, output subdir for chord image ie: 'Minor'

    return tuple of parameters:
    error_in_chord, status_str, chord_name, 
    root_note, chord_filename, frets, fingers, intervals,
    dlabels, footer, subfolder, 
    chord_quality, chord_detail, chord_slash
    ie: (
          False
        , '* G#dim7(no5)/F#      Loaded'
        , 'G#dim7(no5)/F#'
        , 'G#'
        , 'G#dim7(no5)_F#'
        , ['2', '2', '0', '1', '0', '1']
        , ['3', '4', 'x', '1', 'x', '2']
        , ['3', '4', 'x', '1', 'x', '2']
        , ['b7', 'b3', 'b5', 'R', 'b3', 'bb7']
        , 'Minor/'
        , 'dim7'
        , '(no5)'
        , 'F#'
        )    
    '''
    
    # error flag for chord syntax
    error_in_chord = False
    # error message in case of errors
    error_message = '' 
    
    # ======== chord_name checks ========
    # check if chord_name is null or only whitespaces
    if chord_name.strip():
        # remove whitespaces from chord_name
        chord_name = chord_name.strip()
        # if a '.' is in chord name then use what string is after that
        # '.' for a postfix in chord file name. Only first '.' from right
        # count for splitting 
        if chord_name.count('.') >= 1:
            (chord_name, chord_postfix) = chord_name.rsplit('.', 1)
            chord_filename = chord_name + '.' + chord_postfix
        else:
            chord_filename = chord_name
        parsed_chord_name = parse_chord_name(chord_name)
        root_note = parsed_chord_name[0]
        chord_quality = parsed_chord_name[1]
        chord_detail = parsed_chord_name[2]
        chord_slash = parsed_chord_name[3]
        # sanitize chord_filename
        for forbidd_char in '/\\':
            chord_filename = chord_filename.replace(forbidd_char, '_', 9)
        # remove the other forbidden chars now, before duplicate filenames
        # are checked, so that names differing only by a forbidden char
        # (ie 'C(add9)' and 'Cadd9') do not overwrite each other
        chord_filename = global_utilities.sanitize_str(chord_filename)
    else:
        error_in_chord = True
        error_message += 'chord name is blank '
    # ======== frets checks ========
    # check if frets is null or only whitespaces    
    if frets.strip():
        # split frets string in a list and remove whitespaces
        # from every single fret number
        frets = global_utilities.crd_str2slst(frets)
        # check if frets list has 6 elements and all are allowed chars
        # note: frets list must exist and must have 6 elements
        if (not check_fretlist_correct(frets)):
            error_in_chord = True
            error_message += 'error in frets syntax '
    else:
        error_in_chord = True
        error_message += 'frets field is blank '
    # ======== fingers checks ========
    # check if fingers is null or only whitespaces    
    if fingers.strip():
        # split fingers string in a list and remove whitespaces
        # from every single finger number
        fingers = global_utilities.crd_str2slst(fingers)
        # if fingers list has not 6 elements
        if (len(fingers) != 6):
            # then it must be a single '%'
            if (len(fingers) == 1) and (fingers[0] == '%'):
                fingers = []                            
            # in all other cases it's an error, fingers list must be complete
            else:
                error_in_chord = True
                error_message += 'error in fingers syntax '
        # check if all 6 finger list elements are all allowed chars
        # fingers_set_allowed_chars = {'t', 'T', '1', '2', '3', '4', 'x', 'X'}
        elif (not set(fingers).issubset(global_constants.fingers_set_allowed_chars)):
            error_in_chord = True
            error_message += 'error in fingers syntax '
    else:
        fingers = []
    # ======== intervals checks ========
    # check if intervals is null or only whitespaces    
    if intervals.strip():
        # split intervals string in a list and remove whitespaces
        # from every single interval
        intervals = global_utilities.crd_str2slst(intervals)
        # if intervals list has not 6 elements
        if (len(intervals) != 6):
            # then it must be a single '%'
            if (len(intervals) == 1) and (intervals[0] == '%'):
                intervals = []                            
            # in all other cases it's an error, fingers list must be complete
            else:
                error_in_chord = True
                error_message += 'error in intervals syntax '
        # check if all 6 interval list elements are all allowed chars
        # intervals_set_allowed_chars = {'r', 'R', 'b2', '2', 'b3', '3', '4', 'b5', '#4', '5' ...
        #                             ,  'rh', 'Rh', 'b2h', '2h', 'b3h', '3h', '4h', 'b5h', '#4h', '5h' ...}
        elif (not set(intervals).issubset(global_constants.intervals_set_allowed_chars)):
            error_in_chord = True
            error_message += 'error in intervals syntax '
    else:
        intervals = []
    # ======== dlabels checks ========
    # check if dlabels is null or only whitespaces    
    if dlabels.strip():
        # split dlabels string in a list and remove whitespaces
        # from every single finger label
        dlabels = global_utilities.crd_str2slst(dlabels)
        # if dlabels has only 1 element then
        if (len(dlabels) == 1):
            # if it is be a single '%' then reset
            if (dlabels[0] == '%'):
                dlabels = []
            # if it is has more than 3 chars then it is an error
            elif (len(dlabels[0]) > 3):
                error_in_chord = True
                error_message += 'error in dlabels syntax '
    else:
        dlabels = []
    # ======== footer checks ========
    # check if footer is null or only whitespaces    
    if footer.strip():
        # split footer string in a list and remove whitespaces
        # from every single footer label
        footer = global_utilities.crd_str2slst(footer)
        # if footer has only 1 element then
        if (len(footer) == 1):
            # if it is be a single '%' then reset
            if (footer[0] == '%'):
                footer = []
            # if it is has more than 3 chars then it is an error
            elif (len(footer[0]) > 3):
                error_in_chord = True
                error_message += 'error in footer syntax '    
    else:
        footer = []
    # ======== subfolder checks ========
    # check if subfolder is null or only whitespaces    
    if subfolder.strip():
        # if it is be a single '%' then reset
        if (subfolder == '%'):
            subfolder = ''
        else:
            subfolder = subfolder.strip() + '/'
    else:
        subfolder = ''
    # ==================================
    
    if error_in_chord:
        status_str = '{:<20} {}'.format("* " + chord_name, " Not loaded, " + error_message)
    else:
        status_str = '{:<20} {:6}'.format("* " + chord_name, " Loaded")           
    return (
        error_in_chord, status_str, chord_name,
        root_note, chord_filename, frets, fingers, intervals,
        dlabels, footer, subfolder, 
        chord_quality, chord_detail, chord_slash
        )


def apply_check_crd_params(onechord_str_list):
    '''
    check if a generic input list of strings can be a correct list for a single chord
    ie: [ chord_name, 'frets', 'fingers', 'intervals', 'dlabels', 'footer', 'subfolder' ]
    we do not suppose all 6 elements exists (only chord_name, frets are mandatory), 
    for example ['G#dim7(no5)/F#', '2,2,0,1,0,1', '3,4,x,1,x,2']
    if a non mandatory parameters is to be given but some 
    preceding ones are to be skipped use '%'
    
    onechord_str_list: List, input candidate single chord list of strings
        [ chord_name, 'frets', 'fingers', 'intervals', 'dlabels', 'footer', 'subfolder' ]
        ['G#dim7(no5)/F#', '2,2,0,1,0,1', '3,4,x,1,x,2', ...]

    return tuple of parameters:
    error_in_chord, status_str, chord_name, 
    root_note, chord_filename, frets, fingers, intervals,
    dlabels, footer, subfolder, 
    chord_quality, chord_detail, chord_slash
    ie: (
          False
        , '* G#dim7(no5)/F#      Loaded'
        , 'G#dim7(no5)/F#'
        , 'G#'
        , 'G#dim7(no5)_F#'
        , ['2', '2', '0', '1', '0', '1']
        , ['3', '4', 'x', '1', 'x', '2']
        , ['3', '4', 'x', '1', 'x', '2']
        , ['b7', 'b3', 'b5', 'R', 'b3', 'bb7']
        , 'Minor/'
        , 'dim7'
        , '(no5)'
        , 'F#'
        )  
    '''
    # strip empty elements (nulls or whitespaces)
    onechord_str_list_flt = [x for x in onechord_str_list if x.strip()]
    len_onechord_str_list_flt = len(onechord_str_list_flt)
    # if onechord_str_list has 1 element then it should be chord_name
    if len_onechord_str_list_flt >= 1:
        chord_name = onechord_str_list_flt[0]
    else:
        chord_name = ''
    # check if onechord_str_list has frets string (2nd element), if so get it
    if len_onechord_str_list_flt >= 2:
        frets = onechord_str_list_flt[1]
    else:
        frets = ''
    # check if onechord_str_list has fingers string (3rd element), if so get it
    if len_onechord_str_list_flt >= 3:
        fingers = onechord_str_list_flt[2]
    else:
        fingers = ''
    # check if onechord_str_list has intervals string (4rd element), if so get it
    if len_onechord_str_list_flt >= 4:
        intervals = onechord_str_list_flt[3]
    else:
        intervals = ''
    # check if onechord_str_list has dlabels column (5th element), if so get it
    if len_onechord_str_list_flt >= 5:
        dlabels = onechord_str_list_flt[4]
    else:
        dlabels = ''
    # check if onechord_str_list has footer column (6th element), if so get it
    if len_onechord_str_list_flt >= 6:
        footer = onechord_str_list_flt[5]
    else:
        footer = ''
    # check if onechord_str_list has subfolder column (7th element), if so get it
    if len_onechord_str_list_flt >= 7:
        subfolder = onechord_str_list_flt[6]
    else:
        subfolder = ''
     
    return check_crd_params(chord_name, frets, fingers, intervals, dlabels, footer, subfolder)


def fix_duplicate_chordnames(crd_list):
    '''
    process chord list and fix duplicate chord_filenames. ie: Cm, Cm, Cm -> Cm, Cm.v01, Cm.v02
    
    crd_list: List, [[chord_name, root_note, chord_filename, frets, ...], ...]
        ie:         [['Cmaj7', 'C', 'Cmaj7', ['x', '3', '5',   ...], ...], ...]
    where single chord list is [chord_name, root_note, chord_filename, frets, fingers, intervals, dlabels, 
                                footer, subfolder, chord_quality, chord_detail, chord_slash]    
    
    
    return modified crd_list
    '''
    chord_filenames_list = [(elem[0], elem[1][2]) for elem in enumerate(crd_list)]    
    '''
    if crd_list has duplicate chord_filenames we try to fix it using postfix ".vXX". 
    Let'say crd_list is [[chord_name, root_note, chord_filename, frets, ...], ...]
    [
    ['G',     'G',    'G',       ['3', '2', '0',   ...], ...], 
    ['C',     'C' ,   'C' ,      ['x', '3', '2',   ...], ...], 
    ['C',     'C',    'C',       ['x', '3', '5',   ...], ...], 
    ['C',     'C',    'C',       ['8', '10', '10', ...], ...], 
    ['D#m',   'D#',   'D#m',     ['x', '6', '8',   ...], ...], 
    ['Cmaj7', 'C',    'Cmaj7',   ['x', '3', '5',   ...], ...], 
    ]
    now take only list index (implict from enumarete) and chord_filenames  
    chord_filenames_list = [(0, 'G'), (1, 'C'), (2, 'C'), (3, 'C'), (4, 'D#m'), (5, 'Cmaj7')]
    now sort by chord_filename
    '''     
    # chord_filenames_list_sorted =
    # [(1, 'C'), (2, 'C'), (3, 'C'), (5, 'Cmaj7'), (4, 'D#m'), (0, 'G')]
    chord_filenames_list_sorted = sorted(chord_filenames_list, key=lambda lst: lst[1])
    
    # now iterate over chord_filenames_list_sorted
    # and check if actual chordfilename is equal to preceding chordfilename
    # if so create a newchordfilename = AB.vXX
    # and modify original crd_list consequently
    preced_chordfilename = ''
    preced_vers = 1
    for elem in chord_filenames_list_sorted:
        (index, chordfilename) = elem
        if chordfilename == preced_chordfilename:
            newchordfilename = chordfilename + '.v' + str(preced_vers + 1).zfill(2)
            crd_list[index][2] = newchordfilename
            preced_chordfilename = chordfilename
            preced_vers += 1
        else:
            preced_chordfilename = chordfilename
            preced_vers = 1
    return crd_list


def get_crd_list_from_str_list(chords_str_list, print_output=True):
    """
    process a python list of strings (chords_str_list) and return a list of lists 
    compatible with draw_chord_list() ie:
    
    [
        [chord_name, root_note, chord_filename, 
        frets, fingers, intervals, dlabels, footer, 
        subfolder, chord_quality, chord_detail, chord_slash]
        , ...
    ]
    
    [
        ['G#dim7(no5)/F#', 'G#', ''G#dim7(no5)_F#', 
        ['2','2','0','1','0','1'], ['3','4','x','1','x','2'], [], [], [],
        'Diminished', 'dim7','(no5)', 'F#']
        , ...
    ]

    chords_str_list: List, list of chord list of strings (list of lists) like
    [ [ chord_name, 'frets', 'fingers', 'intervals', 'dlabels', 'footer', 'subfolder' ], ... ]
    only chord_name, frets are mandatory, if a non mandatory parameters 
    is to be given but some preceding ones are to be skipped use '%'
    ie:
        [['C', 'x,3,2,0,1,0', 'x,3,2,x,1,x'], ['C/C#', 'x,4,5,5,5,x', 'x,1,2,3,4,x'], ...]
        
    print_output: Optional Boolean param, if False do not print anything
    
    return tuple (crd_list, msg_str)
    where crd_list is 
    [
        [chord_name, root_note, chord_filename, 
        frets, fingers, intervals, dlabels, footer, 
        subfolder, chord_quality, chord_detail, chord_slash]
        , ...
    ]
    """
    crd_list = []
    header = '\nGetting Chords\n==============\n' + \
             'Processing input chords list'
    if print_output: print(header)
    msg_str = header
    for elem in chords_str_list: 
        (
         error_in_chord, status_str,
         chord_name, root_note, chord_filename,
         frets, fingers, intervals, dlabels,
         footer, subfolder, chord_quality, chord_detail, chord_slash
         ) = apply_check_crd_params(elem)
        
        # if chord is ok append to return list
        if not error_in_chord:
            crd_list.append([
                  chord_name, root_note
                , chord_filename, frets
                , fingers, intervals, dlabels,
                  footer, subfolder, chord_quality, chord_detail, chord_slash])            
        if print_output: print(status_str)
        msg_str += '\n' + status_str
    
    len_crd_list = len(crd_list)
    
    body = ">>> " + str(len_crd_list) + " chords loaded <<<"
    if print_output: print(body)
    msg_str += '\n' + body
    
    # fix for duplicate chord_filenames (see function def)
    crd_list = fix_duplicate_chordnames(crd_list)

    return (crd_list, msg_str)


def get_crd_list_from_file(input_crdf, print_output=True):
    """
    process chord list txt file and return a list of list compatible with draw_chord_list() ie:
    
    [
        [chord_name, root_note, chord_filename, 
        frets, fingers, intervals, dlabels, footer, 
        subfolder, chord_quality, chord_detail, chord_slash]
        , ...
    ]
    
    [
        ['G#dim7(no5)/F#', 'G#', ''G#dim7(no5)_F#', 
        ['2', '2', '0', '1', '0', '1'], ['3', '4', 'x', '1', 'x', '2'], ['b7', 'b3', 'b5', 'R', 'b3', 'bb7'], 
        ['b7', 'b3', 'b5', 'R', 'b3', 'bb7'], ['3', '4', 'x', '1', 'x', '2'],
        'Diminished/', 'dim7','(no5)', 'F#']
        , ...
    ]
    
    and also a msg_str
    
    input_crdf: String, chord list txt file path
        only chord_name, frets are mandatory, if a non mandatory parameters 
        is to be given but some preceding ones are to be skipped use '%'
        ie:
        NAME              FRETS         FINGERS       INTERVALS           DOT LABELS          FOOTER        SUBFOLDER
        G#dim7(no5)/F#    2,2,0,1,0,1   3,4,x,1,x,2   b7,b3,b5,R,b3,bb7   b7,b3,b5,R,b3,bb7   3,4,x,1,x,2   Diminished
    print_output: Optional Boolean param, if False do not print anything
    
    return tuple (crd_list, msg_str)
    where crd_list = [
        [
              chord_name
            , root_note
            , chord_filename
            , frets
            , fingers
            , intervals
            , dlabels
            , footer
            , subfolder
            , chord_quality
            , chord_detail
            , chord_slash
        ], ...
    ]
    """
    crd_list = []
    listelem = []
    linenumber = 0
    header = '\nGetting Chords\n==============\n' + \
             'Processing chords file: ' + input_crdf
    if print_output: print(header)
    msg_str = header    
    with open(input_crdf, mode='r') as infile:
        for infile_line in infile: 
            # strip start and final spaces
            infile_line_strip = infile_line.strip()
            # strip empty lines, newlines and comments (//)
            if (not infile_line_strip) or (infile_line_strip[0:2] == '//'): continue
            linenumber += 1
            # make listelem list by tabs splitting
            listelem = infile_line_strip.split('\t')
            # strip header line
            if linenumber > 1:
                (
                 error_in_chord, status_str,
                 chord_name, root_note, chord_filename,
                  frets, fingers, intervals, dlabels,
                 footer, subfolder, chord_quality, chord_detail, chord_slash
                 ) = apply_check_crd_params(listelem)
                # if chord is ok append to return list
                if not error_in_chord:
                    crd_list.append([
                        chord_name, root_note,
                        chord_filename, frets, fingers, intervals,
                        dlabels, footer, subfolder,
                        chord_quality, chord_detail, chord_slash])            
                if print_output: print(status_str)
                msg_str += '\n' + status_str
    
    len_crd_list = len(crd_list)
    
    body = ">>> " + str(len_crd_list) + " chords loaded form file <<<"
    if print_output: print(body)
    msg_str += '\n' + body
    
    # fix for duplicate chord_filenames (see function def)
    crd_list = fix_duplicate_chordnames(crd_list)

    return (crd_list, msg_str)


if __name__ == "__main__":
    
    # testing this function
    
    # --- functions parameters ---
    # full path for chord list txt
    input_crdf = '../tests/crds_test_files/chord-list.txt'
    
    print('parse_chord_name(FA#m(no5)/SOLb)', parse_chord_name('FA#m(no5)/SOLb'))
    print('parse_chord_name(Gbmaj9/D#)',      parse_chord_name('Gbmaj9/D#'))
    print('parse_chord_name(Gmaj7b5)',        parse_chord_name('Gmaj7b5'))
    
    print('\n--------\n')
 
    print('check_crd_params("C#", "0,3,2,0,1", "x,3,2,x,1", "x,R,3,5,R,", "%", "x,R,3,5,1,3", "Major")')
    print(check_crd_params( 'C#', '0,3,2,0,1', 'x,3,2,x,1', 'x,R,3,5,R,', '%', 'x,R,3,5,1,3', 'Major'))   
    
    print('check_crd_params("C", "0,3,2,0,1,0", "x,3,2,x,1,x", "x,R,3,5,R,3", "%", "x,R,3,5,1,3", "Major")')
    print(check_crd_params( 'C', '0,3,2,0,1,0', 'x,3,2,x,1,x', 'x,R,3,5,R,3', '%', 'x,R,3,5,1,3', 'Major'))
    
    print('check_crd_params("G#dim7(no5)/F#", "2,2,0,1,0,1", "3,4,x,1,x,2", "b7,b3,b5,R,b3,bb7", "3,4,x,1,x,2", "", "Minor")')
    print(check_crd_params( 'G#dim7(no5)/F#', '2,2,0,1,0,1', '3,4,x,1,x,2', 'b7,b3,b5,R,b3,bb7', '3,4,x,1,x,2', '', 'Minor'))
    
    print('\n--------')
    
    
    chords_str_list1 = [
          ['C',                 'x,3,2,0,1,0',      'x,3,2,x,1,x']
        , ['C',                 '8,10,10,9,8,8',    '1,3,4,2,1,1']
        , ['C/C#',              'x,4,2,0,1,0',      'x,4,2,x,1,x']
        , ['C/C#',              'x,4,5,5,5,x',      'x,1,2,3,4,x']
        , ['G#dim7(no5)/F#',    '2,2,0,1,0,1',      '3,4,x,1,x,2']
        , ['LA/SOL',               '3,x,2,2,2,x',      '2,x,1,1,1,x']
        , ['LA/SOL#',              '4,0,2,2,2,0',      '4,x,1,1,1,x']
        ]
    
    test_fix_chords = [elem for elem in get_crd_list_from_str_list(chords_str_list1)[0]]
    print('\ncrd_list_from_file1:\n')
    for elem in test_fix_chords:
        print(str(elem))


    print('\n--------')

    # list of chord list of strings (list of lists)
    chords_str_list2 = [
          ['C',                 'x,3,2,0,1,0',      'x,3,2,x,1,x']
        , ['C/C#',              'x,4,5,5,5,x',      'x,1,2,3,4,x']
        , ['G#dim7(no5)/F#',    '2,2,0,1,0,1',      '3,4,x,1,x,2']
        , ['Cm/C#',             'x,16,17,17,17,x',  'x,1,2,3,4,x']
        ]
        
    return_crd_list_from_file = get_crd_list_from_file(input_crdf)
    print('\ncrd_list_from_file2:\n')
    for elem in return_crd_list_from_file[0]:
        print(str(elem))

    print('\n--------')

    return_crd_list_from_str_list = get_crd_list_from_str_list(chords_str_list2)
    print('\ncrd_list_from_chords_str_list:\n')
    for elem in return_crd_list_from_str_list[0]:
        print(str(elem))
