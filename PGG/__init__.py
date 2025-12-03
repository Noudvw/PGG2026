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

MALE_NAMES = ['Male1', 'Male2', 'Male3', 'Male4', 'Male5', 'Male6', 'Male7', 'Male8' ]
FEMALE_NAMES = ['Female1', 'Female2', 'Female3', 'Female4', 'Female5', 'Female6', 'Female7', 'Female8']

class C(BaseConstants):
    NAME_IN_URL = 'PGG'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    ENDOWMENT = 20
    MPCR = 0.4
    PUN_MULTIPLIER = 3
    BONUS_MULTIPLIER = 4


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    PG_earnings = models.FloatField()
    collective_contribution = models.IntegerField()
    def compute_group_gender(self):
        fem_count = 0
        male_count = 0
        for p in self.get_players():
            if p.gender == 1:
                fem_count += 1
            elif p.gender == 2:
                male_count += 1
            else:
                fem_count += 1
                male_count += 1
        for p in self.get_players():
            p.fem_in_group = fem_count
            p.male_in_group = male_count

    def set_nicknames_group(self):
        fem = 0
        male = 0
        for p in self.get_players():
            #count genders
            if p.gender == 1:
                fem +=1
            elif p.gender == 2:
                male +=1
            else:
                fem +=1
                male +=1
            #Indices
            self.fem_low_index = 0
            if fem >= 3:
                self.fem_high_index = 2
            else:
                self.fem_high_index = 4
            self.male_low_index = 0
            if male >= 3:
                self.male_high_index = 2
            else:
                self.male_high_index = 4
        for p in self.get_players():
            if p.gender == 1:
                names = FEMALE_NAMES[self.fem_low_index: self.fem_high_index]
                self.fem_low_index = self.fem_high_index
                if fem >=3: self.fem_high_index += 2
                else: self.fem_high_index += 4
            elif p.gender == 2:
                names = MALE_NAMES[self.male_low_index: self.male_high_index]
                self.male_low_index = self.male_high_index
                if male >=3:
                    self.male_high_index += 2
                else:
                    self.male_high_index += 4
            else:
                names = (FEMALE_NAMES[self.fem_low_index: self.fem_low_index + 2] +
                         MALE_NAMES[self.male_low_index: self.male_low_index + 2])
                self.fem_low_index += 2
                self.fem_high_index += 2
                self.male_low_index += 2
                self.male_high_index += 2
            p.nickname_choices = ",".join(names)

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
                if p.p2_punishment_co0 == p.pun_belief_co0:
                    p.bonus_counter += 1
                if p.p3_punishment_co0 == p.pun_belief_co1:
                    p.bonus_counter += 1
                if p.p4_punishment_co0 == p.pun_belief_co2:
                    p.bonus_counter += 1
            if p.id_in_group == 1 and C.PLAYERS_PER_GROUP < 4:
                p.pun_received = p.p2_punishment_co0 + p.p3_punishment_co0
                if p.p2_punishment_co0 == p.pun_belief_co0:
                    p.bonus_counter += 1
                if p.p3_punishment_co0 == p.pun_belief_co1:
                    p.bonus_counter += 1
            if p.id_in_group == 2 and C.PLAYERS_PER_GROUP > 3:
                p.pun_received = p.p2_punishment_co0 + p.p3_punishment_co1 + p.p4_punishment_co1
                if p.p2_punishment_co0 == p.pun_belief_co0:
                    p.bonus_counter += 1
                if p.p3_punishment_co1 == p.pun_belief_co1:
                    p.bonus_counter += 1
                if p.p4_punishment_co1 == p.pun_belief_co2:
                    p.bonus_counter += 1
            if p.id_in_group == 2 and C.PLAYERS_PER_GROUP < 4:
                p.pun_received = p.p2_punishment_co0 + p.p3_punishment_co1
                if p.p2_punishment_co0 == p.pun_belief_co0:
                    p.bonus_counter += 1
                if p.p3_punishment_co1 == p.pun_belief_co1:
                    p.bonus_counter += 1
            if p.id_in_group == 3 and C.PLAYERS_PER_GROUP > 3:
                p.pun_received = p.p2_punishment_co1 + p.p3_punishment_co1 + p.p4_punishment_co2
                if p.p2_punishment_co1 == p.pun_belief_co0:
                    p.bonus_counter += 1
                if p.p3_punishment_co1 == p.pun_belief_co1:
                    p.bonus_counter += 1
                if p.p4_punishment_co2 == p.pun_belief_co2:
                    p.bonus_counter += 1
            if p.id_in_group == 3 and C.PLAYERS_PER_GROUP < 4:
                p.pun_received = p.p2_punishment_co1 + p.p3_punishment_co1
                if p.p2_punishment_co0 == p.pun_belief_co1:
                    p.bonus_counter += 1
                if p.p3_punishment_co0 == p.pun_belief_co1:
                    p.bonus_counter += 1
            if p.id_in_group == 4:
                p.pun_received = p.p2_punishment_co2 + p.p3_punishment_co2 + p.p4_punishment_co2
                if p.p2_punishment_co2 == p.pun_belief_co0:
                    p.bonus_counter += 1
                if p.p3_punishment_co2 == p.pun_belief_co1:
                    p.bonus_counter += 1
                if p.p4_punishment_co2 == p.pun_belief_co2:
                    p.bonus_counter += 1
            p.pun_received_costs = C.PUN_MULTIPLIER * p.pun_received
            p.bonus_earnings = p.bonus_counter * C.BONUS_MULTIPLIER
            p.earnings = p.remaining_endowment + self.PG_earnings - p.punishment_costs - p.pun_received_costs + p.bonus_earnings

    def set_other_contributions(self):
        for p in self.get_players():
                others = p.get_others_in_group()
                if len(others) > 0:
                    p.p2_contribution = others[0].contribution
                if len(others) > 1:
                    p.p3_contribution = others[1].contribution
                if len(others) > 2:
                    p.p4_contribution = others[2].contribution

    def bonus_pre_beliefs(self):
        for p in self.get_players():
            others = p.get_others_in_group()
            if p.pre_belief_co0 == p.p2_contribution :
                p.bonus_counter += 1
            if p.pre_belief_co1 == p.p3_contribution :
                p.bonus_counter += 1
            if C.PLAYERS_PER_GROUP > 3:
                if p.pre_belief_co2 == p.p4_contribution:
                    p.bonus_counter += 1

    def bonus_post_beliefs(self):
        for p in self.get_players():
            others = p.get_others_in_group()
            if p.post_belief_co0 == p.p2_contribution:
                p.bonus_counter += 1
            if p.post_belief_co1 == p.p3_contribution:
                p.bonus_counter += 1
            if C.PLAYERS_PER_GROUP > 3:
                if p.post_belief_co2 == p.p4_contribution:
                    p.bonus_counter += 1


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
    fem_low_index = models.IntegerField(initial=0)
    fem_high_index = models.IntegerField(initial=2)
    rare_fem_low_index = models.IntegerField(initial=0)
    rare_fem_high_index = models.IntegerField(initial=4)
    male_low_index = models.IntegerField(initial=0)
    male_high_index = models.IntegerField(initial=2)
    rare_male_low_index = models.IntegerField(initial=0)
    rare_male_high_index = models.IntegerField(initial=4)


class Player(BasePlayer):
    nickname = models.StringField()
    nickname_choices = models.StringField()
    gender = models.IntegerField(
        label = "What is your gender? ",
        choices = [
            [1, "Female"],
            [2, "Male"],
            [3, "Other"],
            [4, "I prefer not to say"]
        ]
    )
    #Misc
    endowment = models.IntegerField()
    remaining_endowment = models.IntegerField()
    contribution = models.IntegerField()
    fem_in_group = models.IntegerField(default=0)
    male_in_group = models.IntegerField(default=0)
    bonus_counter = models.IntegerField(default = 0)
    #Beliefs
    pre_belief_co0 = models.IntegerField()
    pre_belief_co1 = models.IntegerField()
    pre_belief_co2 = models.IntegerField()
    post_belief_co0 = models.IntegerField()
    post_belief_co1 = models.IntegerField()
    post_belief_co2 = models.IntegerField()
    #Beliefs about punishment
    pun_belief_co0 = models.IntegerField()
    pun_belief_co1 = models.IntegerField()
    pun_belief_co2 = models.IntegerField()
    pun_cond_0_co0 = models.IntegerField()
    pun_cond_0_co1 = models.IntegerField()
    pun_cond_0_co2 = models.IntegerField()
    pun_cond_10_co0 = models.IntegerField()
    pun_cond_10_co1 = models.IntegerField()
    pun_cond_10_co2 = models.IntegerField()
    pun_cond_20_co0 = models.IntegerField()
    pun_cond_20_co1 = models.IntegerField()
    pun_cond_20_co2 = models.IntegerField()
    #Punishment
    punishment_costs = models.IntegerField()
    pun_received_costs = models.IntegerField()
    punishment_co0 = models.IntegerField()
    punishment_co1 = models.IntegerField()
    punishment_co2 = models.IntegerField()
    pun_received = models.FloatField()
    #Earnings
    earnings = models.CurrencyField()
    intermediate_earnings = models.FloatField()
    bonus_earnings = models.IntegerField()

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
#Comment: nickname_choices does not work currently. This is because things are updated every time
# a player puts in a value, so too dynamically. See if you can change this using a group-based function on a waitpage
# before using nickname_choices (for example, storing low_index and high_index separately, before creating the name list with options)
def nickname_choices(player):
    return player.nickname_choices.split(",")

class SetUpRound(WaitPage):
    wait_for_all_groups = True
    @staticmethod
    def after_all_players_arrive(subsession):
        for p in subsession.get_players():
            p.setup_round()

class Demographics(Page):
    form_model = 'player'
    form_fields = ['gender']

class DemographicsWait(WaitPage):
    def after_all_players_arrive(group):
        group.compute_group_gender()

class AssignNicknames(WaitPage):
    def after_all_players_arrive(group):
        group.set_nicknames_group()

class NameChoice(Page):
    form_model = 'player'
    form_fields = ['nickname']


class NameWait(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        group.set_other_names()

class GroupDisplay(Page):
    pass

class PreBeliefs(Page):
    form_model = 'player'
    form_fields = ['pre_belief_co0', 'pre_belief_co1', 'pre_belief_co2']

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
        group.bonus_pre_beliefs()


class PostBeliefs(Page):
    form_model = 'player'
    form_fields = ['post_belief_co0', 'post_belief_co1', 'post_belief_co2']

class IntermediateResults(Page):
    pass

class PunBeliefsUncond(Page):
    form_model = 'player'
    form_fields = ['pun_belief_co0', 'pun_belief_co1', 'pun_belief_co2']

class PunBeliefsCond0(Page):
    form_model = 'player'
    form_fields = ['pun_cond_0_co0', 'pun_cond_0_co1', 'pun_cond_0_co2']

class PunBeliefsCond10(Page):
    form_model = 'player'
    form_fields = ['pun_cond_10_co0', 'pun_cond_10_co1', 'pun_cond_10_co2']

class PunBeliefsCond20(Page):
    form_model = 'player'
    form_fields = ['pun_cond_20_co0', 'pun_cond_20_co1', 'pun_cond_20_co2']

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
        group.bonus_post_beliefs()
        group.compute_earnings_post_punishment()



class Results(Page):
    pass

# PAGES
page_sequence = [
    SetUpRound,
    Demographics,
    DemographicsWait,
    AssignNicknames,
    NameChoice,
    NameWait,
    GroupDisplay,
    PreBeliefs,
    Contribution,
    ComputePunishment,
    PostBeliefs,
    IntermediateResults,
    PunBeliefsUncond,
    Punishment,
    ComputeResults,
    Results,
]
