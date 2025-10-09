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
    PG_earnings = models.FloatField()
    collective_contribution = models.IntegerField()

    def compute_group_earnings(self):
        self.collective_contribution = sum(p.contribution for p in self.get_players())
        unrounded_earnings = self.collective_contribution * C.MPCR
        self.PG_earnings = round(unrounded_earnings, 2)

    def compute_earnings(self):
        for p in self.get_players():
            p.remaining_endowment = p.endowment - p.contribution
            p.earnings = p.remaining_endowment + self.PG_earnings

    def set_other_contributions(self):
        for p in self.get_players():
                others = p.get_others_in_group()
                if len(others) > 0:
                    p.p2_contribution = others[0].contribution
                if len(others) > 1:
                    p.p3_contribution = others[1].contribution
                if len(others) > 2:
                    p.p4_contribution = others[2].contribution


class Player(BasePlayer):
    endowment = models.IntegerField()
    remaining_endowment = models.IntegerField()
    contribution = models.IntegerField()
    earnings = models.FloatField()
    p2_contribution = models.IntegerField()
    p3_contribution = models.IntegerField()
    p4_contribution = models.IntegerField()

    def setup_round(self):
        self.endowment = C.ENDOWMENT

    def coplayer0(self):
        return self.get_others_in_group()[0]

    def coplayer1(self):
        return self.get_others_in_group()[1]

class SetUpRound(WaitPage):
    wait_for_all_groups = True
    @staticmethod
    def after_all_players_arrive(subsession):
        for p in subsession.get_players():
            p.setup_round()

class Contribution(Page):
    form_model = 'player'
    form_fields = ['contribution']

    @staticmethod
    def error_message(player, values):
        if values['contribution'] < 0:
            return "Contribution cannot be negative"
        if values['contribution'] > 20:
            return "Contribution cannot be greater than 20"
        return None

class ComputeResults(WaitPage):
    wait_for_participants = True
    @staticmethod
    def after_all_players_arrive(group):
        group.compute_group_earnings()
        group.compute_earnings()
        group.set_other_contributions()

class Results(Page):
    pass

# PAGES



page_sequence = [
    SetUpRound,
    Contribution,
    ComputeResults,
    Results,
]
