from otree.api import (
    BaseConstants,
    BaseGroup,
    BasePlayer,
    BaseSubsession,
    Page,
    models,
    widgets,
)

from PGG import C as PGG_C

doc = """
A splash-screen welcome page for the experiment
"""


class C(BaseConstants):
    NAME_IN_URL = "Debrief"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    study_purpose = models.StringField(label = "What do you think is the purpose of this study?")
    study_issues = models.StringField(label = "Did you experience any issues during this study? If so, include them here")

    nickname_child_own = models.IntegerField(choices = [ 1, 2, 3, 4, 5, 6, 7],
                                             widget= widgets.RadioSelect)
    nickname_friends_own = models.StringField()
    nickname_others_own = models.StringField()
    nickname_child_co0 = models.IntegerField(choices = [ 1, 2, 3, 4, 5, 6, 7],
                                             widget= widgets.RadioSelect)
    nickname_friends_co0 = models.StringField()
    nickname_others_co0 = models.StringField()
    nickname_child_co1 = models.IntegerField(choices = [ 1, 2, 3, 4, 5, 6, 7],
                                             widget= widgets.RadioSelect)
    nickname_friends_co1 = models.StringField()
    nickname_others_co1 = models.StringField()
    nickname_child_co2 = models.IntegerField(choices = [ 1, 2, 3, 4, 5, 6, 7],
                                             widget= widgets.RadioSelect)
    nickname_friends_co2 = models.StringField()
    nickname_others_co2 = models.StringField()

# PAGES
class Debrief_Page(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        fields = ['study_purpose', 'study_issues', 'nickname_child_own', 'nickname_friends_own', 'nickname_others_own',
                  'nickname_child_co0', 'nickname_friends_co0', 'nickname_others_co0',
                  'nickname_child_co1', 'nickname_friends_co1', 'nickname_others_co1']
        if PGG_C.PLAYERS_PER_GROUP > 3:
            fields.append('nickname_child_co2')
            fields.append('nickname_friends_co2')
            fields.append('nickname_others_co2')
        return fields


    @staticmethod
    def vars_for_template(player):
        labels = {}

        # --- Own nickname ---
        own = player.participant.nickname_own
        labels.update({
            'nickname_child_own_label':
                f'From a 1-7 scale, how much would you consider giving your child the name {own}? (1 = not at all, 7 = absolutely)',
            'nickname_friends_own_label':
                f'Are any of your best friends or relatives called {own}? Please mention the relationship you have with them',
            'nickname_others_own_label':
                f'Is there anything else you connect with {own} you would like to tell us?',
        })

        # --- Co-players ---
        for i in range(3):
            nickname = getattr(player.participant, f'nickname_co{i}')

            if nickname:
                labels.update({
                    f'nickname_child_co{i}_label':
                        f'From a 1-7 scale, how much would you consider giving your child the name {nickname}? (1 = not at all, 7 = absolutely)',
                    f'nickname_friends_co{i}_label':
                        f'Are any of your best friends or relatives called {nickname}? Please mention the relationship you have with them',
                    f'nickname_others_co{i}_label':
                        f'Is there anything else you connect with {nickname} you would like to tell us?',
                })

        return labels



page_sequence = [
    Debrief_Page,
]
