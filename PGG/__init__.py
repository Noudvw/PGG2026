from otree.api import (
    BaseConstants,
    BaseGroup,
    BasePlayer,
    BaseSubsession,
    Page,
    WaitPage,
    models,
)
import random

doc = """
Public Goods Game
"""

MALE_NAMES = ['Christopher', 'Daniel', 'David', 'James', 'Joseph', 'Matthew', 'Michael', 'Thomas' ]
FEMALE_NAMES = ['Emily', 'Julia', 'Katherine', 'Natalie', 'Rachel', 'Samantha', 'Sarah']
RANDOM_LIST = [0, 1]

class C(BaseConstants):
    NAME_IN_URL = 'Experiment'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    ENDOWMENT = 20
    MPCR = 0.4
    PUN_MULTIPLIER = 3
    BONUS_MULTIPLIER = 4
    TREATMENT = True

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
            p.info_treatment = C.TREATMENT

    def set_bonus_rounds(self):
        for p in self.get_players():
            p.endowment = C.ENDOWMENT
            p.gender = p.participant.vars['gender']
            if C.PLAYERS_PER_GROUP == 4:
                p.belief_that_counts_1 = random.randint(0,8)
                p.belief_that_counts_2 = random.randint(0,8)
            if C.PLAYERS_PER_GROUP < 4:
                p.belief_that_counts_1 = random.randint(0,5)
                p.belief_that_counts_2 = random.randint(0,5)

    def set_nicknames_group(self):
        fem = 0
        male = 0
        random.shuffle(MALE_NAMES)
        random.shuffle(FEMALE_NAMES)


        for p in self.get_players():
            #count genders
            if p.gender == 1:
                p.nickname = FEMALE_NAMES[fem]
                fem +=1
            elif p.gender == 2:
                p.nickname = MALE_NAMES[male]
                male +=1
            else:
                random.shuffle(RANDOM_LIST)
                if RANDOM_LIST[0] == 0:
                    p.nickname = FEMALE_NAMES[fem]
                    fem +=1
                elif RANDOM_LIST[0] == 1:
                    p.nickname = MALE_NAMES[male]
                    male +=1

    def compute_group_earnings(self):
        self.collective_contribution = sum(p.contribution for p in self.get_players())
        unrounded_earnings = self.collective_contribution * C.MPCR
        self.PG_earnings = round(unrounded_earnings, 2)

    def compute_earnings(self):
        for p in self.get_players():
            p.remaining_endowment = p.endowment - p.contribution
            p.intermediate_earnings = p.remaining_endowment + self.PG_earnings
            p.contribution_others = self.collective_contribution - p.contribution

    def compute_earnings_post_punishment(self):
        for p in self.get_players():
            p.remaining_endowment = p.endowment - p.contribution
            if C.PLAYERS_PER_GROUP > 3:
                p.punishment_costs = p.punishment_co0 + p.punishment_co1 + p.punishment_co2
            else:
                p.punishment_costs = p.punishment_co0 + p.punishment_co1
            if p.id_in_group == 1 and C.PLAYERS_PER_GROUP > 3:
                p.pun_received = p.p2_punishment_co0 + p.p3_punishment_co0 + p.p4_punishment_co0
                if p.p2_punishment_co0 == p.pun_belief_co0:
                    p.bonus_pun_co0 += 1
                if p.p3_punishment_co0 == p.pun_belief_co1:
                    p.bonus_pun_co1 += 1
                if p.p4_punishment_co0 == p.pun_belief_co2:
                    p.bonus_pun_co2 += 1
            if p.id_in_group == 1 and C.PLAYERS_PER_GROUP < 4:
                p.pun_received = p.p2_punishment_co0 + p.p3_punishment_co0
                if p.p2_punishment_co0 == p.pun_belief_co0:
                    p.bonus_pun_co0 += 1
                if p.p3_punishment_co0 == p.pun_belief_co1:
                    p.bonus_pun_co1 += 1
            if p.id_in_group == 2 and C.PLAYERS_PER_GROUP > 3:
                p.pun_received = p.p2_punishment_co0 + p.p3_punishment_co1 + p.p4_punishment_co1
                if p.p2_punishment_co0 == p.pun_belief_co0:
                    p.bonus_pun_co0 += 1
                if p.p3_punishment_co1 == p.pun_belief_co1:
                    p.bonus_pun_co1 += 1
                if p.p4_punishment_co1 == p.pun_belief_co2:
                    p.bonus_pun_co2 += 1
            if p.id_in_group == 2 and C.PLAYERS_PER_GROUP < 4:
                p.pun_received = p.p2_punishment_co0 + p.p3_punishment_co1
                if p.p2_punishment_co0 == p.pun_belief_co0:
                    p.bonus_pun_co0 += 1
                if p.p3_punishment_co1 == p.pun_belief_co1:
                    p.bonus_pun_co1 += 1
            if p.id_in_group == 3 and C.PLAYERS_PER_GROUP > 3:
                p.pun_received = p.p2_punishment_co1 + p.p3_punishment_co1 + p.p4_punishment_co2
                if p.p2_punishment_co1 == p.pun_belief_co0:
                    p.bonus_pun_co0 += 1
                if p.p3_punishment_co1 == p.pun_belief_co1:
                    p.bonus_pun_co1 += 1
                if p.p4_punishment_co2 == p.pun_belief_co2:
                    p.bonus_pun_co2 += 1
            if p.id_in_group == 3 and C.PLAYERS_PER_GROUP < 4:
                p.pun_received = p.p2_punishment_co1 + p.p3_punishment_co1
                if p.p2_punishment_co0 == p.pun_belief_co1:
                    p.bonus_pun_co0 += 1
                if p.p3_punishment_co0 == p.pun_belief_co1:
                    p.bonus_pun_co1 += 1
            if p.id_in_group == 4:
                p.pun_received = p.p2_punishment_co2 + p.p3_punishment_co2 + p.p4_punishment_co2
                if p.p2_punishment_co2 == p.pun_belief_co0:
                    p.bonus_pun_co0 += 1
                if p.p3_punishment_co2 == p.pun_belief_co1:
                    p.bonus_pun_co1 += 1
                if p.p4_punishment_co2 == p.pun_belief_co2:
                    p.bonus_pun_co2 += 1
            p.pun_received_costs = C.PUN_MULTIPLIER * p.pun_received

            if C.PLAYERS_PER_GROUP > 3:
                bonuses_list = [
                    p.bonus_pre_co0,
                    p.bonus_pre_co1,
                    p.bonus_pre_co2,
                    p.bonus_post_co0,
                    p.bonus_post_co1,
                    p.bonus_post_co2,
                    p.bonus_pun_co0,
                    p.bonus_pun_co1,
                    p.bonus_pun_co2
                ]
                p.bonus_earnings = bonuses_list[p.belief_that_counts_1] * C.BONUS_MULTIPLIER
            if C.PLAYERS_PER_GROUP < 4:
                bonuses_list = [
                    p.bonus_pre_co0,
                    p.bonus_pre_co1,
                    p.bonus_post_co0,
                    p.bonus_post_co1,
                    p.bonus_pun_co0,
                    p.bonus_pun_co1,
                ]
                p.bonus_earnings = bonuses_list[p.belief_that_counts_1] * C.BONUS_MULTIPLIER
            p.earnings = p.remaining_endowment + self.PG_earnings - p.punishment_costs - p.pun_received_costs + p.bonus_earnings
            p.participant.group_size = C.PLAYERS_PER_GROUP

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
                p.bonus_pre_co0 += 1
            if p.pre_belief_co1 == p.p3_contribution :
                p.bonus_pre_co1 += 1
            if C.PLAYERS_PER_GROUP > 3:
                if p.pre_belief_co2 == p.p4_contribution:
                    p.bonus_pre_co2 += 1

    def bonus_post_beliefs(self):
        for p in self.get_players():
            others = p.get_others_in_group()
            if p.info_treatment == False:
                if p.post_belief_co0 == p.p2_contribution:
                    p.bonus_post_co0 += 1
                if p.post_belief_co1 == p.p3_contribution:
                    p.bonus_post_co1 += 1
                if C.PLAYERS_PER_GROUP > 3:
                    if p.post_belief_co2 == p.p4_contribution:
                        p.bonus_post_co2 += 1
            else: pass


    def set_other_punishments(self):
        for p in self.get_players():
            others = p.get_others_in_group()
            if C.PLAYERS_PER_GROUP < 4:
                if len(others) > 0:
                    p.p2_punishment_co0 = others[0].punishment_co0
                    p.p2_punishment_co1 = others[0].punishment_co1
                if len(others) > 1:
                    p.p3_punishment_co0 = others[1].punishment_co0
                    p.p3_punishment_co1 = others[1].punishment_co1
                if len(others) > 2:
                    p.p4_punishment_co0 = others[2].punishment_co0
                    p.p4_punishment_co1 = others[2].punishment_co1

            if C.PLAYERS_PER_GROUP > 3:
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
            p.participant.nickname_own = p.nickname
            p.participant.nickname_co0 = p.p2_nickname
            p.participant.nickname_co1 = p.p3_nickname
            if C.PLAYERS_PER_GROUP > 3:
                p.participant.nickname_co2 = p.p4_nickname
            else:
                p.participant.nickname_co2 = None


class Player(BasePlayer):
    info_treatment = models.BooleanField()
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
    contribution = models.IntegerField(label = "How many Points do you contribute to the group project?")
    contribution_others = models.IntegerField()
    fem_in_group = models.IntegerField(default=0)
    male_in_group = models.IntegerField(default=0)
    bonus_counter = models.IntegerField(default = 0)
    belief_that_counts_1 = models.IntegerField()
    belief_that_counts_2 = models.IntegerField()
    bonus_pre_co0 = models.IntegerField(default = 0)
    bonus_pre_co1 = models.IntegerField(default = 0)
    bonus_pre_co2 = models.IntegerField(default = 0)
    bonus_post_co0 = models.IntegerField(default = 0)
    bonus_post_co1 = models.IntegerField(default = 0)
    bonus_post_co2 = models.IntegerField(default = 0)
    bonus_pun_co0 = models.IntegerField(default = 0)
    bonus_pun_co1 = models.IntegerField(default = 0)
    bonus_pun_co2 = models.IntegerField(default = 0)
    prob_bonus_pre_co0 = models.IntegerField(default = 0)
    prob_bonus_pre_co1 = models.IntegerField(default = 0)
    prob_bonus_pre_co2 = models.IntegerField(default = 0)
    prob_bonus_post_co0 = models.IntegerField(default = 0)
    prob_bonus_post_co1 = models.IntegerField(default = 0)
    prob_bonus_post_co2 = models.IntegerField(default = 0)
    prob_bonus_pun_co0 = models.IntegerField(default = 0)
    prob_bonus_pun_co1 = models.IntegerField(default = 0)
    prob_bonus_pun_co2 = models.IntegerField(default = 0)
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


    def coplayer0(self):
        return self.get_others_in_group()[0]

    def coplayer1(self):
        return self.get_others_in_group()[1]

    def coplayer2(self):
        if C.PLAYERS_PER_GROUP > 3:
            return self.get_others_in_group()[2]
        return None


class DemographicsWait(WaitPage):
    def after_all_players_arrive(group):
        group.set_bonus_rounds()
        group.compute_group_gender()
        group.set_nicknames_group()
        group.set_other_names()

class GroupDisplay(Page):
    pass


class PreBeliefs(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player):
        fields = ['pre_belief_co0', 'pre_belief_co1']
        if C.PLAYERS_PER_GROUP > 3:
            fields.append('pre_belief_co2')
        return fields

    @staticmethod
    def vars_for_template(player):
        if C.PLAYERS_PER_GROUP > 3:
            return dict(
                pre_belief_co0_label = 'How many Points will <strong> {} </strong> contribute to the project?'.format(player.p2_nickname),
                pre_belief_co1_label = 'How many Points will <strong> {} </strong> contribute to the project?'.format(player.p3_nickname),
                pre_belief_co2_label = 'How many Points will <strong> {} </strong> contribute to the project?'.format(player.p4_nickname)
            )
        else:
            return dict(
                pre_belief_co0_label='How many Points will <strong> {} </strong>  contribute to the project?'.format(player.p2_nickname),
                pre_belief_co1_label='How many Points will <strong> {} </strong>  contribute to the project?'.format(player.p3_nickname)
            )

    @staticmethod
    def error_message(player, values):
        if values['pre_belief_co0'] > 20 or values['pre_belief_co1'] > 20:
            return "Please report a number between 0 and 20 for each person"
        if C.PLAYERS_PER_GROUP > 3:
            if values['pre_belief_co2'] > 20:
                return "Please report a number between 0 and 20 for each person"
        return None


class Contribution(Page):
    form_model = 'player'
    form_fields = ['contribution']

    @staticmethod
    def error_message(player, values):
        if values['contribution'] < 0:
            return "Contribution cannot be negative"
        if values['contribution'] > 20:
            return "Please choose a contribution level between 0 and 20"
        return None

class ComputeContribution(WaitPage):
    wait_for_participants = True
    @staticmethod
    def after_all_players_arrive(group):
        group.compute_group_earnings()
        group.set_other_contributions()
        group.compute_earnings()
        group.bonus_pre_beliefs()


class PostBeliefs(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player):
        fields = ['post_belief_co0', 'post_belief_co1']
        if C.PLAYERS_PER_GROUP > 3:
            fields.append('post_belief_co2')
        return fields


    @staticmethod
    def vars_for_template(player):
        if C.PLAYERS_PER_GROUP > 3:
            return dict(
                post_belief_co0_label='How many Points did <strong> {} </strong> contribute to the project?'.format(player.p2_nickname),
                post_belief_co1_label='How many Points did <strong> {} </strong>contribute to the project?'.format(player.p3_nickname),
                post_belief_co2_label='How many Points did <strong> {} </strong> contribute to the project?'.format(player.p4_nickname)
            )
        else:
            return dict(
                post_belief_co0_label='How many Points did <strong> {} </strong>contribute to the project?'.format(player.p2_nickname),
                post_belief_co1_label='How many Points did <strong> {} </strong> contribute to the project?'.format(player.p3_nickname)
            )

    @staticmethod
    def error_message(player, values):
        if values['post_belief_co0'] > 20 or values['post_belief_co1'] > 20:
            return "Please report a belief between 0 and 20 for each person"
        if C.PLAYERS_PER_GROUP > 3:
            if values['post_belief_co2'] > 20:
                return "Please report a belief between 0 and 20 for each person"
        total = values['post_belief_co0'] + values ['post_belief_co1']
        if C.PLAYERS_PER_GROUP > 3:
            total += values['post_belief_co2']
        if total != player.contribution_others:
            return (
                f"Note: Your reported values add up to "
            f"{total} points. "
            f"Please ensure that your reported values add up to "
            f"{player.contribution_others} points."
            )
        return None

class IntermediateResults(Page):
    def is_displayed(player):
        return player.info_treatment

class PunBeliefsUncond(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player):
        fields = ['pun_belief_co0', 'pun_belief_co1']
        if C.PLAYERS_PER_GROUP > 3:
            fields.append('pun_belief_co2')
        return fields

    @staticmethod
    def vars_for_template(player):
        if C.PLAYERS_PER_GROUP > 3:
            return dict(
                pun_belief_co0_label='How many Deduction Points will <strong> {} </strong> assign to you?'.format(player.p2_nickname),
                pun_belief_co1_label='How many Deduction Points will <strong> {} </strong> assign to you?'.format(player.p3_nickname),
                pun_belief_co2_label='How many Deduction Points will <strong> {} </strong> assign to you?'.format(player.p4_nickname)
            )
        else:
            return dict(
                pun_belief_co0_label='How many Deduction Points will <strong> {} </strong> assign to you?'.format(player.p2_nickname),
                pun_belief_co1_label='How many Deduction Points will <strong> {} </strong> assign to you?'.format(player.p3_nickname)
            )

    @staticmethod
    def error_message(player, values):
        if values['pun_belief_co0'] > 10 or values['pun_belief_co1'] > 10:
            return "Please report a belief between 0 and 10 for each person"
        if C.PLAYERS_PER_GROUP > 3:
            if values['pun_belief_co2'] > 10:
                return "Please report a belief between 0 and 10 for each person"
        return None

class Punishment(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player):
        fields = ['punishment_co0', 'punishment_co1']
        if C.PLAYERS_PER_GROUP > 3:
            fields.append('punishment_co2')
        return fields

    @staticmethod
    def vars_for_template(player):
        if C.PLAYERS_PER_GROUP > 3:
            return dict(
                punishment_co0_label='How many Deduction Points do you assign to <strong> {} </strong>?'.format(player.p2_nickname),
                punishment_co1_label='How many Deduction Points do you assign to <strong> {} </strong>?'.format(player.p3_nickname),
                punishment_co2_label='How many Deduction Points do you assign to <strong> {} </strong>?'.format(player.p4_nickname)
            )
        else:
            return dict(
                punishment_co0_label='How many Deduction Points do you assign to <strong> {} </strong>?'.format(player.p2_nickname),
                punishment_co1_label='How many Deduction Points do you assign to <strong> {} </strong>?'.format(player.p3_nickname)
            )

    @staticmethod
    def error_message(player, values):
        if  (values['punishment_co0'] < 0
            or values['punishment_co1'] < 0
            or C.PLAYERS_PER_GROUP > 3 and values['punishment_co2'] < 0):
                return "Value cannot be negative"
        if (values['punishment_co0'] > 10 or
            values['punishment_co1'] > 10 or
            C.PLAYERS_PER_GROUP > 3 and values['punishment_co2'] > 10):
                return "Please choose a value between 0 and 10 for each person"
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
    DemographicsWait,
    GroupDisplay,
    PreBeliefs,
    Contribution,
    ComputeContribution,
    PostBeliefs,
    IntermediateResults,
    Punishment,
    PunBeliefsUncond,
    ComputeResults,
    Results,
]
