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
chords_formulas: helpers to work with chord formulas.

A formula is a tuple of intervals, ie ('R', '3', '5', 'b7', '(9)', '11').
An interval in parentheses is optional: the chord is still recognized
without it. formula_expander() turns one formula with optional intervals
into all its variants (with and without each optional interval, up to 3
optional intervals), formula_omitter() removes intervals (ie the 5th) and
formula_extender() adds the half-steps tuples used by intervals.formula_matcher().
"""


# standard library imports
import re

# local application imports
from libs import music_utilities


def formula_omitter(frml_interv, omitting_interv):
    '''
    Given a formula tuple return that formula with omitting_interv intervals erased 
    ie: f(('R','b3','5','7','(9)','11','13'), ('9','5')) -> ('R','b3','7','11','13')
    ie: f(('R','b3','5','7','(9)','11','13'), (13)) -> ('R', 'b3', '5', '7', '(9)', '11')
    
    frml_interv: Tuple, chord interval formula
    omitting_interv: Tuple, intervals to be erased in original formula.
        Note: a single interval must be written ('5',) with the comma:
        ('5') is just the string '5' (it works only by chance, because
        'in' then checks for a substring)
    
    return: Tuple, string tuple of original formula with omitting_interv intervals erased
    ''' 
    return_list = []
    # check for optional intervals string '(#5)' with regex
    re_pattern = re.compile(r'\((.+)\)')
    if omitting_interv:
        for intrv in frml_interv:
            # if an option interval is found
            re_match = re_pattern.search(intrv)
            if re_match:
                # do not consider parentheses for searching in omitting_interv
                # if intrv is '(b5)' -> re_match.group(0) = '(b5)'
                #                    -> re_match.group(1) =  'b5'
                serach_intrv = re_match.group(1)
            else:
                serach_intrv = intrv
            if serach_intrv not in omitting_interv: return_list.append(intrv)
    else:
        return_list = frml_interv
    return tuple(return_list)


def formula_expander(frml_interv):
    '''
    Given a formula tuple get all possible combinations for optional interval
    ie: ('R','b3','5','7','(9)','11','13') -> (('R','b3','5','7','9','11','13'),
                                              ('R','b3','5','7','11','13'))
    however (no change for no optional elements):
        ('R','b3','5','7','9','11','13') -> ('R','b3','5','7','9','11','13')
    
    frml_interv: Tuple, chord interval formula
    
    return: Tuple, string tuple of all possibilities (can be tuple of tuples)
    ''' 
    # check for optional intervals string '(9)' with regex
    re_pattern = re.compile(r'\((.+)\)')
    # all possible combinations dict based on numbers of options {n_option: comb_list, ...}
    comb_matrix = {
          1: (0, 1)
        , 2: ((0, 0), (1, 1), (0, 1), (1, 0))
        , 3: (
              (0, 0, 0), (0, 0, 1), (0, 1, 0)
            , (0, 1, 1), (1, 0, 0), (1, 0, 1)
            , (1, 1, 0), (1, 1, 1)
            )
        }
    # dict with info on each optional interval
    # ie: dict: {'(9)':'9','(11)':'11' ...}
    opt_intervals = {}
    return_list = []
    return_tuple = ()
    for elem in frml_interv:
        re_match = re_pattern.search(elem)
        if re_match:
            # group(0) -> (9) and group(1) -> 9
            opt_intervals[re_match.group(0)] = re_match.group(1)
    # keys list: ['(9)','(11)'...]
    opt_intervals_keys = list(opt_intervals.keys())
    n_opt_intervals = len(opt_intervals_keys)
    # if are there any optional intervals
    if n_opt_intervals:
        # get the correspondig comb_matrix:
        # ie: n_opt_intervals = 1 -> (0,1), 2 -> ((0,0), (1,1), (0,1), (1,0))
        act_comb_matrix = comb_matrix[n_opt_intervals]
        # combination list: 1 option -> [[None], ['(9)']]
        # 2 option -> [[None, None], ['(9)', '(11)'], 
        #              [None, '(11)'], ['(9)', None]]
        combinations = []
        # for case of only 1 option, opt_intervals_keys = ['(9)']
        # and act_comb_matrix = (0,1), so combinations = [[None], ['(9)']]
        if (n_opt_intervals == 1):
            for elem in act_comb_matrix:
                comb_elem = [el if elem else None for el in opt_intervals_keys]
                combinations.append(comb_elem)
        # for more options example 2), opt_intervals_keys = ['(9)', '(11)']
        # and act_comb_matrix = ((0,0), (1,1), (0,1), (1,0)), 
        # so combinations = see above
        else: 
            for elem in act_comb_matrix:
                comb_elem = [el if elem[idx] else None for idx, el in enumerate(opt_intervals_keys)]
                combinations.append(comb_elem)
        # let's see the case for 1 option: combinations = [[None], ['(9)']]
        for elem in combinations:
            return_elem_list = []
            # frml_interv = ('R','b3','5','7','(9)','11','13')
            for el in frml_interv:
                # if frml_interv element is not an element of combinations
                # then append it to return_elem_list, otherwise skip it
                if el not in elem:
                    # but hey, do not append '(9)' instead append '9'
                    new_elem = opt_intervals[el] if (el in opt_intervals) else el
                    return_elem_list.append(new_elem)
            return_list.append(return_elem_list)
        return_tuple = tuple([tuple(elem) for elem in return_list])
    else:
        return_tuple = frml_interv
    return return_tuple


def formula_to_exp_rhsteps(frml_interv):
    '''
    Given a formula tuple get all possible normalized semitones distances tuple
    and info about option intervals were expanded
    
    ie: ('R','b3','5','7','(9)','11','13') -> 
    (
        (
          (('R', 'b3', '5', '7', '9', '11', '13'), (0, 2, 3, 5, 7, 9, 11), (0, 3, 7, 11, 2, 5, 9))
        , (('R', 'b3', '5', '7', '11', '13'), (0, 3, 5, 7, 9, 11), (0, 3, 7, 11, 5, 9))
        ), True
    )
    
    however (no change for no optional elements):
    
    (
        (
            ('R', 'b3', '5', '7', '9', '11', '13'), (0, 2, 3, 5, 7, 9, 11), (0, 3, 7, 11, 2, 5, 9)
        ), False
    )

    frml_interv: Tuple, chord interval formula
    
    return
    - all possible tuples: (
              formula
            , half-steps sorted and normalized formula tuple
            , half-steps and normalized formula tuple
            )
    - boolean variable extend if option intervals were expanded
    '''
    # if exist at least an optional interval extend = True
    extend = True
    # get all possible formulas combinations ie: ('R','b3','5','7','(9)','11','13') -> 
    # formulas == (('R','b3','5','7','9','11','13'), ('R','b3','5','7','11','13'))
    formulas = formula_expander(frml_interv)
    # if no expansion has happened
    if (formulas == frml_interv):
        extend = False
        return_tuple = (
              frml_interv
            , music_utilities.intervals_to_sorted_rhsteps(frml_interv)
            , music_utilities.intervals_to_rhsteps(frml_interv)
            )
    else:
        return_list = []
        for elem in formulas:
            return_list.append(
                    (
                      elem
                    , music_utilities.intervals_to_sorted_rhsteps(elem)
                    , music_utilities.intervals_to_rhsteps(elem)
                    )
                )
        # sort return_list by the sorted rhsteps tuple (ascending order)
        return_list = sorted(return_list, key=lambda x: x[1])
        return_tuple = tuple(return_list)
    return return_tuple, extend


def formula_extender(full_formula):
    '''
    Given a full formula tuple in the form of ('chord quality', 'chord interval formula', majmin)
    ie: ('13', ('R','3','5','b7','(9)','11','13'), 'major')
    get all formula possibilities and half-steps tuples, (tuples of tuples)
    and also info about option intervals were expanded, ie:   
    
    (
        (
          ('13', ('R','3','5','b7','9','11','13'), (0,2,4,5,7,9,10), (0,4,7,10,2,5,9), 'major')
        , ('13', ('R','3','5','b7','11','13'),     (0,4,5,7,9,10),   (0,4,7,10,5,9), 'major')
        ), True
    )
    
    for the case of no otional intervals it's just a tuple
    ie: formula_extender(('add9', ('R', '3', '5', '9'), 'major')):

    (
        ('add9', ('R', '3', '5', '9'), (0, 2, 4, 7), (0, 4, 7, 2), 'major')
        , False
    )

    full_formula: Tuple, ('chord quality', 'chord formula')
    
    return a tuple with 2 elements
    - all possible tuples: (
             'chord quality'
            , formula
            , half-steps sorted and normalized formula tuple (also grouped, no repetitions)
            , half-steps and normalized formula tuple (also grouped, no repetitions)
            )
    - boolean variable extend if option intervals were expanded
    '''    
    # full_formula = ('13',('R','3','5','b7','(9)','11','13'), 'major')
    chord_quality, formula, majmin = full_formula
    # all possible tuples + extend bool variable if option intervals were expanded
    # (
    #   (('R', '3', '5', 'b7', '9', '11', '13'), (0, 2, 4, 5, 7, 9, 10), (0, 4, 7, 10, 2, 5, 9))
    # , (('R', '3', '5', 'b7', '11', '13'),      (0, 4, 5, 7, 9, 10),    (0, 4, 7, 10, 5, 9))
    # )
    #  extend = True
    formula_exp, extend = formula_to_exp_rhsteps(formula)
    # no optional intervals present
    if (not extend):
        return_tuple = (chord_quality, formula_exp[0], formula_exp[1], formula_exp[2], majmin), False
    else:
        return_list = []
        for elem in formula_exp:
            return_list.append((chord_quality, elem[0], elem[1], elem[2], majmin))
        return_tuple = tuple(return_list), extend
    return return_tuple


if __name__ == "__main__":
    
    # testing this functions
    
    formula1 = ('R', 'b3', '5', '7', '9', '11', '13')
    formula2 = ('R', 'b3', '5', '7', '(9)', '11', '13')
    formula3 = ('R', 'b3', '5', '7', '(9)', '(11)', '13')
    
    print('\n- formula_omitter(' + str(formula2) + ', (''9'', ''5'')):\n\t', \
                        formula_omitter(formula2, ('9', '5')))
    print('\n- formula_omitter(' + str(formula2) + ', (''8'')):\n\t', \
                        formula_omitter(formula2, ('8')))
    print('\n- formula_expander(' + str(formula1) + '):\n\t', formula_expander(formula1))
    print('\n- formula_expander(' + str(formula2) + '):\n\t', formula_expander(formula2))
    print('\n- formula_expander(' + str(formula3) + '):\n\t', formula_expander(formula3))    

    print('\n- formula_to_exp_rhsteps(' + str(formula1) + '):\n\t', formula_to_exp_rhsteps(formula1))
    print('\n- formula_to_exp_rhsteps(' + str(formula2) + '):\n\t', formula_to_exp_rhsteps(formula2))
    print('\n- formula_to_exp_rhsteps(' + str(formula3) + '):\n\t', formula_to_exp_rhsteps(formula3))

    formula0 = ('add9', ('R', '3', '5', '9'), 'major')
    formula1 = ('13', ('R', '3', '5', 'b7', '9', '11', '13'), 'major')
    formula2 = ('13', ('R', '3', '5', 'b7', '(9)', '11', '13'), 'major')
    formula3 = ('13', ('R', '3', '5', 'b7', '(9)', '(11)', '13'), 'major')
    
    print('\n- formula_extender(' + str(formula0) + '):\n\t', formula_extender(formula0))
    print('\n- formula_extender(' + str(formula1) + '):\n\t', formula_extender(formula1))
    print('\n- formula_extender(' + str(formula2) + '):\n\t', formula_extender(formula2))
    print('\n- formula_extender(' + str(formula3) + '):\n\t', formula_extender(formula3)) 

    # print formula_omitter(('R', 'b3', '5', 'b7', '(9)', '11'), ('5'))
