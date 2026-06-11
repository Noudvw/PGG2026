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
    question1 = models.IntegerField(label ="Q1: What is your income?" )
    question2 = models.IntegerField(label ="Q2: What is the income of the other group members?" )
    question3 = models.IntegerField(label="Q3: What is your income?")
    question4 = models.IntegerField(label="Q4: What is the income of the other group members?")
    question5 = models.IntegerField(label="Q5: What is your income if you contribute 0 Points to the group project?")
    question6 = models.IntegerField(label="Q6: What is your income if you contribute 10 Points to the group project?")
    question7 = models.IntegerField(label="Q7: By how many Points will your income be reduced by assigning Deduction Points?")
    question8 = models.IntegerField(label="Q8: By how many Points will your income be reduced by assigning Deduction Points?")
    question9 = models.IntegerField(label="Q9: By how many Points will your income be reduced by receiving Deduction Points?")
    question10 = models.IntegerField(label="Q10: You can earn bonus Points by making correct estimates. "
                                           "What is the maximum bonus you can receive by making estimates?")
    question11 = models.IntegerField(label = "Which statement is correct?",
                                     choices = (
                                        [1, "The number of bonus Points I get is fully randomly determined, it does not matter what estimates I make"],
                                        [2, "To maximize expected earnings, I should not necessarily make estimates I believe in. "
                                         "Instead, I can increase earnings by estimating strategically."],
                                        [3, "To maximize expected earnings, I should report estimates I think are true."]
                                     ))
    info_clicked = models.IntegerField(initial=0)

    q1mistakes = models.IntegerField(initial=0)
    q2mistakes = models.IntegerField(initial=0)
    q3mistakes = models.IntegerField(initial=0)
    q4mistakes = models.IntegerField(initial=0)
    q5mistakes = models.IntegerField(initial=0)
    q6mistakes = models.IntegerField(initial=0)
    q7mistakes = models.IntegerField(initial=0)
    q8mistakes = models.IntegerField(initial=0)
    q9mistakes = models.IntegerField(initial=0)
    q10mistakes = models.IntegerField(initial=0)
    q11mistakes = models.IntegerField(initial=0)
# PAGES
class QuestionsPGG(Page):
    form_model = "player"
    form_fields = ["question1", "question2", "question3", "question4", "question5", "question6"]
    Qpage = 1


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
            if qdata["page"] != QuestionsPGG.Qpage:
                continue

            if values[f"question{qnum}"] != qdata["question_answer"]:
                incorrect_questions.append(qnum)
                field = f"q{qnum}mistakes"
                setattr(player, field, getattr(player, field) + 1)
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

class QuestionsDP(Page):
    form_model = "player"
    form_fields = ["question7", "question8", "question9"]
    Qpage = 2


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
            if qdata["page"] != QuestionsDP.Qpage:
                continue
            if values[f"question{qnum}"] != qdata["question_answer"]:
                incorrect_questions.append(qnum)
                field = f"q{qnum}mistakes"
                setattr(player, field, getattr(player, field) + 1)
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


class QuestionsBonus(Page):
    form_model = "player"
    form_fields = ["question10", "question11", "info_clicked"]
    Qpage = 3

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
            if qdata["page"] != QuestionsBonus.Qpage:
                continue
            if values[f"question{qnum}"] != qdata["question_answer"]:
                incorrect_questions.append(qnum)
                field = f"q{qnum}mistakes"
                setattr(player, field, getattr(player, field) + 1)
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

class Match(Page):
    pass

page_sequence = [
    QuestionsPGG,
    QuestionsDP,
    QuestionsBonus,
    Match,
]
