# -*- coding: utf-8 -*-

# Copyright (c) 2005-2013 Jochen Kupperschmidt
# Released under the terms of the GNU General Public License
#  _                               _
# | |_ ___ _____ ___ _ _ _ ___ ___| |_
# |   | . |     | ._| | | | . |  _| . /
# |_|_|___|_|_|_|___|_____|___|_| |_|_\
#   http://homework.nwsnet.de/

from bisect import bisect_right
from collections import namedtuple


class Evaluator(object):

    def __init__(self, rating_levels):
        self.rating_levels = rating_levels

    def calculate_score(self, questionnaire, user_input):
        """Calculate the score depending on the given answers."""
        assert user_input.all_questions_answered

        questions = questionnaire.get_questions()
        weightings = self._collect_selected_answers_weightings(questionnaire,
            questions, user_input)
        score = sum(weightings)
        return float(score) / len(questions) * 100

    def _collect_selected_answers_weightings(self, questionnaire, questions,
            user_input):
        for question in questions:
            answer_hash = user_input.get_answer_hash(question.hash)
            answer = questionnaire.get_answer_by_hash(question, answer_hash)
            yield answer.weighting

    def get_rating_text(self, score):
        """Return the rating text for the given score."""
        minimum_scores_to_texts = dict((rl.minimum_score, rl.text)
            for rl in self.rating_levels)

        minimum_scores = sorted(minimum_scores_to_texts.keys())

        # Don't include the lowest value in the thresholds.
        thresholds = minimum_scores[1:]
        index = bisect_right(thresholds, score)

        ratings = list(map(minimum_scores_to_texts.get, minimum_scores))
        return ratings[index]

    def get_result(self, questionnaire, user_input):
        """Return the evaluation result."""
        score = self.calculate_score(questionnaire, user_input)
        text = self.get_rating_text(score)
        return Result(score, text)


RatingLevel = namedtuple('RatingLevel', 'minimum_score text')

Result = namedtuple('Result', 'score text')