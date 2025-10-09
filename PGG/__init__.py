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
Public Goods Game, starting with the most basic implementation possible
"""


class C(BaseConstants):
    NAME_IN_URL = 'PGG'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    ENDOWMENT = 20
    MPCR = 0.4


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    PG_earnings = models.CurrencyField()
    collective_contribution = models.CurrencyField()

    def compute_group_earnings(self):
        self.collective_contribution = sum(player.contribution for player in self.get_players())
        self.PG_earnings = self.collective_contribution * C.MPCR


    def compute_earnings(self):
        for player in self.get_players():
            player.remaining_endowment = player.endowment - player.contribution
            player.earnings = player.remaining_endowment + self.PG_earnings


class Player(BasePlayer):
    endowment = models.CurrencyField()
    remaining_endowment = models.CurrencyField()
    contribution = models.IntegerField()
    earnings = models.CurrencyField()

    def setup_round(self):
        self.endowment = C.ENDOWMENT

class SetUpRound(WaitPage):
    wait_for_all_groups = True
    @staticmethod
    def after_all_players_arrive(subsession):
        for p in subsession.get_players():
            p.setup_round()

class Contribution(Page):
    form_model = 'player'
    form_fields = ['contribution']

class ComputeResults(WaitPage):
    wait_for_participants = True
    @staticmethod
    def after_all_players_arrive(group):
        group.compute_group_earnings()
        group.compute_earnings()

class Results(Page):
    pass

# PAGES



page_sequence = [
    SetUpRound,
    Contribution,
    ComputeResults,
    Results,
]
