#!/usr/bin/env python -m pytest

# This is annoying. I don't know why I have to update the path to find source code
# in the parent directory. I can't figure out how else to make this work in 
# VS Code. Grrr.
import sys
import os.path
sys.path.insert(0, os.path.abspath('..'))

from scoring import *

#
# Test scoring
#
def test_score_pair():
    assert score_pair(1, [1, 2, 3]) == (1, 1)
    assert score_pair(2, [1, 2, 3]) == (2, 3)
    assert score_pair(2, []) == (0, 0)
    assert score_pair(1, [2, 2, 2]) == (0, 0)
    assert score_pair(1, [1, None, 2]) == (1, 1)

#
# Test score_round
#
def test_score_round():
    judge_results = { 1: [1, 2, 3 ]}
    assert score_round(1, judge_results) == { 1: (1, 1) }
    assert score_round(2, judge_results) == { 1: (2, 3) }

    judge_results[2] = [ 2, 3, 4 ]
    assert score_round(1, judge_results) == { 1: (1, 1), 2: (0, 0) }
    assert score_round(2, judge_results) == { 1: (2, 3), 2: (1, 2) }

def test_majority():
    assert majority({ 1: [ 1, 2, 3 ]}) == 2
    assert majority({ 1: [ 1, 2, 3, 4, 5 ]}) == 3
    assert majority({ 1: [ 1, 2, 3, 4, 5, 6, 7 ]}) == 4

def test_rule_5():
    judge_results = {}
    judge_results[1] = [1, 1, 3 ]
    judge_results[2] = [2, 2, 4 ]
    judge_results[3] = [3, 3, 5 ]

    # With a threshold of zero, no one wins.
    # With a threshold of one, 1 wins
    # With a threshold of two, no one wins.
    assert(rule_5_winner(0, judge_results)) == None
    assert(rule_5_winner(1, judge_results)) == 1
    assert(rule_5_winner(2, judge_results)) == None

def test_rule_6_7_winners():
    judge_results = {}
    judge_results[1] = [1, 1, 3 ]
    judge_results[2] = [2, 2, 4 ]
    judge_results[3] = [3, 3, 5 ]

    # With threshold of zero, no one wins.
    assert(rule_6_7_winners(0, judge_results)) == []
    
    # With threshold of one, only #1 wins
    assert(rule_6_7_winners(1, judge_results)) == [1]

    # With threshold of two, #1 and #2 win, #1 first (based on sum)
    assert(rule_6_7_winners(2, judge_results)) == [1, 2]

    judge_results[4] = [1, 1, 1]
    # With threshold of one, results should be 4, then 1, all based on count
    assert(rule_6_7_winners(1, judge_results)) == [4, 1]

def test_find_winners_in_round():
    judge_results = {}
    judge_results[1] = [1, 1, 3 ]
    judge_results[2] = [2, 2, 4 ]
    judge_results[3] = [3, 3, 5 ]

    # Threshold of zero, no winners:
    assert(find_winners_in_round(0, judge_results)) == []

    # Threshold of one, #1 wins.
    assert(find_winners_in_round(1, judge_results)) == [1]

    # Threshold of two, winners are 1 and 2
    assert(find_winners_in_round(2, judge_results)) == [1, 2]

    # Threshold of three, winners are 1, 2, 3, all based on sums
    assert(find_winners_in_round(3, judge_results)) == [ 1, 2, 3]

    judge_results[4] = [1, 1, 1]
    
    # With a threshold of one, results should be 4, 1
    assert(find_winners_in_round(1, judge_results)) == [4, 1]
    assert(find_winners_in_round(2, judge_results)) == [4, 1, 2]
    assert(find_winners_in_round(3, judge_results)) == [4, 1, 2, 3]

def test_find_winners():
    # Use test cases from standard document
    judge_results = {}
    judge_results[51] = [1, 1, 1, 2, 1]
    judge_results[52] = [4, 2, 2, 1, 2]
    judge_results[53] = [3, 3, 3, 5, 4]
    judge_results[54] = [2, 4, 5, 4, 3]
    judge_results[55] = [5, 6, 4, 3, 5]
    judge_results[56] = [6, 5, 6, 6, 6]
    assert(find_winners(judge_results)) == [51, 52, 53, 54, 55, 56]

    judge_results = {}
    judge_results[61] = [1, 1, 2, 1, 4, 2, 1]
    judge_results[62] = [6, 2, 1, 5, 2, 1, 2]
    judge_results[63] = [2, 4, 3, 3, 6, 3, 3]
    judge_results[64] = [3, 3, 5, 2, 1, 5, 4]
    judge_results[65] = [4, 5, 6, 4, 3, 6, 5]
    judge_results[66] = [5, 6, 4, 6, 5, 4, 6]
    assert(find_winners(judge_results)) == [61, 62, 63, 64, 65, 66]

    judge_results = {}
    judge_results[71] = [3, 1, 6, 1, 1, 2, 1]
    judge_results[72] = [2, 2, 1, 5, 3, 1, 3]
    judge_results[73] = [1, 5, 4, 2, 2, 6, 2]
    judge_results[74] = [5, 4, 2, 4, 6, 5, 4]
    judge_results[75] = [4, 6, 3, 3, 5, 4, 6]
    judge_results[76] = [6, 3, 5, 6, 4, 3, 5]
    assert(find_winners(judge_results)) == [71, 72, 73, 74, 75, 76]
