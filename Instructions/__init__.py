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
    question3 = models.IntegerField(label="Your income?")
    question4 = models.IntegerField(label="The income of the other group members?")
    question5 = models.IntegerField(label="Your income if you contribute 0 Points to the group project?")
    question6 = models.IntegerField(label="Your income if you contribute 10 Points to the group project?")

# PAGES
class QuestionsPGG(Page):
    form_model = "player"
    form_fields = ["question1", "question2", "question3", "question4", "question5", "question6"]


    # This error message method checks whether answers are correct, and only allows players to the next page if they are.
    # In case players make mistakes, the attempt_count is increased by one and players can try again.
    # Players receive a message about the questions they answered incorrectly and a hint corresponding to that question.
    @staticmethod
    def error_message(player: Player, values: dict) -> str | None:
        player.attempt_count += 1
        incorrect_questions = []
        hint_to_questions = {}

        # This part of code checks which answers are incorrect
        for qnum, qdata in Questions.question_data.items():
            if values[f"question{qnum}"] != qdata["question_answer"]:
                incorrect_questions.append(qnum)
                group = qdata["hint_group"]
                hint_to_questions.setdefault(group, []).append(qnum)
        if not incorrect_questions:
                return None
        messages = []

        #The following line shows the players which questions they answered incorrectly
        messages.append(
            f"Your answers to the following questions are incorrect: "
            f"{', '.join(map(str, incorrect_questions))}"
        )

        #The following line is used for displaying hints, depending on which questions were answered incorrect
        for group, qnums in hint_to_questions.items():
            qlist = ",".join(map(str, qnums))
            messages.append(
                f"Hint {group} (for question{'s' if len(qnums) > 1 else ''} {qlist}): "
                f"{Questions.hint_messages[group]}"
            )
        return "<br><br>".join(messages)


class WaitPageCompleted(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def is_displayed(player: Player) -> bool:
        return player.round_number == C.NUM_ROUNDS


page_sequence = [
    QuestionsPGG,
    WaitPageCompleted,
]
