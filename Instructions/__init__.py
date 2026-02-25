from otree.api import (
    BaseConstants,
    BaseGroup,
    BasePlayer,
    BaseSubsession,
    Page,
    WaitPage,
    models,
)

from . import Questions

doc = """
Demo of one way to do a multiple-choice quiz, including counting the
number of attempts.  Also demonstrates one way of incorporating question
data (by creating a Python data structure).
"""


class C(BaseConstants):
    NAME_IN_URL = "Instructions"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    attempt_count = models.IntegerField(initial=0)
    question1 = models.IntegerField(label ="Your income?" )
    question2 = models.IntegerField(label ="The income of the other group members?" )


# PAGES
class QuestionsPGG(Page):
    form_model = "player"
    form_fields = ["question1", "question2"]

    @staticmethod
    def error_message(player: Player, values: dict) -> str | None:
        player.attempt_count += 1
        if values["question1"] != Questions.question_data[1]["question_answer"]:
            return Questions.question_data[1]["question_hint"]
        if values["question2"] != Questions.question_data[2]["question_answer"]:
            return Questions.question_data[2]["question_hint"]
        return None


class WaitPageCompleted(WaitPage):
    template_name = "quiz/WaitPageCompleted.html"
    wait_for_all_groups = True

    @staticmethod
    def is_displayed(player: Player) -> bool:
        return player.round_number == C.NUM_ROUNDS


page_sequence = [
    QuestionsPGG,
    WaitPageCompleted,
]
