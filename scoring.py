#!/usr/bin/env python3

from urllib.parse import _NetlocResultMixinStr
import pytest

#
# Score dance competitions using https://www.worlddancesport.org/Document/99473179446/The_Skating_System.pdf
#
# We start with a list of results. Each result is a pair, a competitor number 
# and a list of votes by judges, e.g.
#
# { 22 => [ 1, 2, None, 4, 1, 1, None ],
#   23 => [ None, 1, 1, 2, 2, None, None ]
# }
#
# Keys to the dict are the competitor number. The value is a list of scores by judges.
# Not every judge scores every competitor, that's what the Nones represent.
#
# We score each round passing in a result dict and return a list of (competitor, score) pairs.
#
# The key to scoring is counting how many judges voted a pair at some level or better.  For
# example, we might count how many times a judge awarded a pair second or better.  We also 
# sometimes need the sum of the scores (e.g. a first and a second sum to 3).
#
# Rules:
#
# Rule 5: 

#
# Score a pair.  Input is a threshold and a list of scores.
#
def score_pair(threshold: int, scores: list) -> tuple:
    count: int = 0
    sum: int = 0

    for score in scores:
        if (score is not None and score <= threshold):
            count += 1
            sum += score
    
    return (count, sum)


def score_round(threshold: int, results: dict) -> dict:
    scores: dict = {}

    for pair in results:
        scores[pair] = score_pair(threshold, results[pair])

    return scores

#
# Add "majority" element to judge scores.  That's half the number of 
# judges, rounded up to an int.  There will always be an odd number of
# judges and every dance pair will be judged by the same number of 
# judges.
#
def majority(judge_scores: dict) -> int:
    first_scores = list(judge_scores.values())[0] 
    num_scores = len(first_scores)
    return int((num_scores + 1) / 2)

#
# Rule 5: Compute count of scores for each dancing pair below threshold.
# If exactly one dance pair exceeds "marjority", that's the winner.
#
# Return the pair number.
#
def rule_5_winner(threshold: int, judge_scores: dict) -> int:
    judge_majority = majority(judge_scores)
    results = score_round(threshold, judge_scores)

    winners = []
    for pair in judge_scores.keys():
        if results[pair][0] >= judge_majority:
            winners.append(pair)

    if len(winners) == 1:
        return winners[0]
    else:
        return None

def rule_6_7_winners(threshold: int, judge_scores: dict) -> list:
    judge_majority = majority(judge_scores)
    results = score_round(threshold, judge_scores)

    winners = []
    for pair in judge_scores.keys():
        if results[pair][0] >= judge_majority:
            winners.append(pair)

    # Winners is now a list of dance pair numbers who had a majority this round
    # Sort list based on rules 6 and 7.
    #
    # Rule 6 says the couple with the greatest majority wins.
    # Rule 7 says if two couples have the same majority, the one with the lowest
    #   sum of scores wins.
    #
    # Python wants to use a key function.  It's shorthand: return a tuple of 
    # values to compare with the first elements winning.  This lambda sorts
    # the list first by increasing count, then decreasing sum.
    winners.sort(key=lambda x: (-results[x][0], results[x][1]))
    return winners

#
# Find winners for a given threshold value.  Return the list.
#
def find_winners_in_round(threshold: int, judge_scores:dict) -> list:
    # Any rule 5 winner?
    r5 = rule_5_winner(threshold, judge_scores)
    if r5 is not None:
        return [r5]

    return rule_6_7_winners(threshold, judge_scores)

def find_winners(judge_scores: dict) -> list:
    winners = []
    threshold = 1

    while len(judge_scores.keys()) > 0:
        new_winners = find_winners_in_round(threshold, judge_scores)
        winners += new_winners
        for winner in new_winners:
            judge_scores.pop(winner)
        threshold += 1

    return winners
