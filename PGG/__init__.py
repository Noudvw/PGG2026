from otree.api import (
    BaseConstants,
    BaseGroup,
    BasePlayer,
    BaseSubsession,
    Page,
    WaitPage,
    models,
    widgets,
)

doc = """
Public Goods Game, starting with the most basic implementation possible
"""

MALE_NAMES = ['Kris1', 'Noud1', 'Kris2','Noud2', 'Kris3', 'Noud3', 'Kris4', 'Noud4']
FEMALE_NAMES = ['Joyce1', 'Sarah1', 'Joyce2', 'Sarah2', 'Joyce3', 'Sarah3', 'Joyce4', 'Sarah4']

class C(BaseConstants):
    NAME_IN_URL = 'PGG'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    ENDOWMENT = 20
    MPCR = 0.4
    PUN_MULTIPLIER = 3


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
            p.intermediate_earnings = p.remaining_endowment + self.PG_earnings

    def compute_earnings_post_punishment(self):
        for p in self.get_players():
            p.remaining_endowment = p.endowment - p.contribution
            p.punishment_costs = p.punishment_co0 + p.punishment_co1 + p.punishment_co2
            if p.id_in_group == 1 and C.PLAYERS_PER_GROUP > 3:
                p.pun_received = p.p2_punishment_co0 + p.p3_punishment_co0 + p.p4_punishment_co0
            if p.id_in_group == 1 and C.PLAYERS_PER_GROUP < 4:
                p.pun_received = p.p2_punishment_co0 + p.p3_punishment_co0
            if p.id_in_group == 2 and C.PLAYERS_PER_GROUP > 3:
                p.pun_received = p.p2_punishment_co0 + p.p3_punishment_co1 + p.p4_punishment_co1
            if p.id_in_group == 2 and C.PLAYERS_PER_GROUP < 4:
                p.pun_received = p.p2_punishment_co0 + p.p3_punishment_co1
            if p.id_in_group == 3 and C.PLAYERS_PER_GROUP > 3:
                p.pun_received = p.p2_punishment_co1 + p.p3_punishment_co1 + p.p4_punishment_co2
            if p.id_in_group == 3 and C.PLAYERS_PER_GROUP < 4:
                p.pun_received = p.p2_punishment_co1 + p.p3_punishment_co1
            if p.id_in_group == 4:
                p.pun_received = p.p2_punishment_co2 + p.p3_punishment_co2 + p.p4_punishment_co2
            p.pun_received_costs = C.PUN_MULTIPLIER * p.pun_received
            p.earnings = p.remaining_endowment + self.PG_earnings - p.punishment_costs - p.pun_received_costs

    def set_other_contributions(self):
        for p in self.get_players():
                others = p.get_others_in_group()
                if len(others) > 0:
                    p.p2_contribution = others[0].contribution
                if len(others) > 1:
                    p.p3_contribution = others[1].contribution
                if len(others) > 2:
                    p.p4_contribution = others[2].contribution

    def set_other_punishments(self):
        for p in self.get_players():
            others = p.get_others_in_group()
            if len(others) > 0:
                p.p2_punishment_co0 = others[0].punishment_co0
                p.p2_punishment_co1 = others[0].punishment_co1
                p.p2_punishment_co2 = others[0].punishment_co2
            if len(others) > 1:
                p.p3_punishment_co0 = others[1].punishment_co0
                p.p3_punishment_co1 = others[1].punishment_co1
                p.p3_punishment_co2 = others[1].punishment_co2
            if len(others) > 2:
                p.p4_punishment_co0 = others[2].punishment_co0
                p.p4_punishment_co1 = others[2].punishment_co1
                p.p4_punishment_co2 = others[2].punishment_co2

    def set_other_names(self):
        for p in self.get_players():
            others = p.get_others_in_group()
            p.p2_nickname = others[0].nickname
            p.p3_nickname = others[1].nickname
            if len(others) > 2:
                p.p4_nickname = others[2].nickname


class Player(BasePlayer):
    #Fields about the current player
    nickname = models.StringField()
    gender = models.IntegerField(
        label = "What is your gender? ",
        choices = [
            [1, "Female"],
            [2, "Male"],
            [3, "Other"],
            [4, "I prefer not to say"]
        ]
    )
    endowment = models.IntegerField()
    remaining_endowment = models.IntegerField()
    punishment_costs = models.IntegerField()
    pun_received_costs = models.IntegerField()
    contribution = models.IntegerField()
    punishment_co0 = models.IntegerField()
    punishment_co1 = models.IntegerField()
    punishment_co2 = models.IntegerField()
    earnings = models.FloatField()
    intermediate_earnings = models.FloatField()
    pun_received = models.FloatField()

    #Fields filled in by other players
    p2_nickname = models.StringField()
    p2_contribution = models.IntegerField()
    p2_punishment_co0 = models.IntegerField()
    p2_punishment_co1 = models.IntegerField()
    p2_punishment_co2 = models.IntegerField()
    p3_nickname = models.StringField()
    p3_contribution = models.IntegerField()
    p3_punishment_co0 = models.IntegerField()
    p3_punishment_co1 = models.IntegerField()
    p3_punishment_co2 = models.IntegerField()
    p4_nickname = models.StringField()
    p4_contribution = models.IntegerField()
    p4_punishment_co0 = models.IntegerField()
    p4_punishment_co1 = models.IntegerField()
    p4_punishment_co2 = models.IntegerField()

    def setup_round(self):
        self.endowment = C.ENDOWMENT

    def coplayer0(self):
        return self.get_others_in_group()[0]

    def coplayer1(self):
        return self.get_others_in_group()[1]

    def coplayer2(self):
        if C.PLAYERS_PER_GROUP > 3:
            return self.get_others_in_group()[2]
        return None

def nickname_choices(player):
    start_index = (player.id_in_group - 1) *2
    end_index = start_index + 2
    if player.gender == 1:
        return FEMALE_NAMES[start_index: end_index]
    elif player.gender == 2:
        return MALE_NAMES[start_index: end_index]
    else:
        return FEMALE_NAMES[start_index: end_index] + MALE_NAMES[start_index: end_index]

class SetUpRound(WaitPage):
    wait_for_all_groups = True
    @staticmethod
    def after_all_players_arrive(subsession):
        for p in subsession.get_players():
            p.setup_round()

class Demographics(Page):
    form_model = 'player'
    form_fields = ['gender']

class NameChoice(Page):
    form_model = 'player'
    form_fields = ['nickname']


class NameWait(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        group.set_other_names()

class GroupDisplay(Page):
    pass

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

class ComputePunishment(WaitPage):
    wait_for_participants = True
    @staticmethod
    def after_all_players_arrive(group):
        group.compute_group_earnings()
        group.set_other_contributions()
        group.compute_earnings()

class IntermediateResults(Page):
    pass

class Punishment(Page):
    form_model = 'player'
    form_fields = ['punishment_co0', 'punishment_co1', 'punishment_co2']
    @staticmethod
    def error_message(player, values):
        if (values['punishment_co0'] < 0
            or values['punishment_co1'] < 0
            or values['punishment_co2'] < 0) :
            return "Punishment cannot be negative"
        if (values['punishment_co0'] > 20 or
            values['punishment_co1'] > 20 or
            values['punishment_co2'] > 20) :
            return "Punishment cannot be greater than 20"
        return None

class ComputeResults(WaitPage):
    wait_for_participants = True
    @staticmethod
    def after_all_players_arrive(group):
        group.set_other_punishments()
        group.compute_group_earnings()
        group.compute_earnings_post_punishment()


class Results(Page):
    pass

# PAGES



page_sequence = [
    SetUpRound,
    Demographics,
    NameChoice,
    NameWait,
    GroupDisplay,
    Contribution,
    ComputePunishment,
    IntermediateResults,
    Punishment,
    ComputeResults,
    Results,
]
