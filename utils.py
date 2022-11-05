from collections import defaultdict
def judge_to_couple_scoresheet(scores_by_judge):
    """
    scores_by_judge = Dict[int, Dict[int, Optional[int]]]: Scores keyed by judge then by couple.
    Returns:
    scores_by_couple = Dict[int, List[int]]: Dict of scores receieved by each couple.
    """

    scores_by_couple=defaultdict(list)
    for judge_score in scores_by_judge.values():
        if len(scores_by_couple) > 0:
            assert len(judge_score) == len(scores_by_couple)
        for couple in judge_score:
            scores_by_couple[couple].append(judge_score[couple])
    return scores_by_couple


