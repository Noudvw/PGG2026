from otree.api import (
    BaseConstants,
    BaseGroup,
    BasePlayer,
    BaseSubsession,
    Page,
    WaitPage,
    models,
)

doc = """
Demo of a demographics questionnaire. 
My aim is to store the answer to the demographic questions in such a way that they can be recollected later, 
to be used in the PGG app.
"""


class C(BaseConstants):
    NAME_IN_URL = "Demographics"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gender = models.IntegerField(
        label="How do you identify? ",
        choices=[
            [1, "Female"],
            [2, "Male"],
            [3, "Other"],
            [4, "I prefer not to say"]
        ]
    )

# PAGES
class DemoQuestions(Page):
    form_model = "player"
    form_fields = ["gender"]

    #Stores gender for usage in the PGG
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.vars['gender'] = player.gender

class DemoWait(WaitPage):
    pass

page_sequence = [
    DemoQuestions,
    DemoWait,
]
