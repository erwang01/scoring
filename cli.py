import scoring
import utils

judge_count = int(input("How many judges are there?"))
couples = [int(bib) for bib in input("List the couple numbers:").split(',')]

scores_by_judge = {}
for judge in range(judge_count):
    scores = {}
    for couple in couples:
        try:
            scores[couple] = int(input(f"Judge {judge}, couple {couple} score:[None]"))
        except ValueError:
            scores[couple] = None
    scores_by_judge[judge] = scores

scores_by_couple = utils.judge_to_couple_scoresheet(scores_by_judge)
winners = scoring.find_winners(scores_by_couple)

print(winners)

