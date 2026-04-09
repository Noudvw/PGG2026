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
TREATMENT_OPTIONS = [True, False]
RANDOM_LIST = [0, 1]

class C(BaseConstants):
    NAME_IN_URL = 'Experiment'
    PLAYERS_PER_GROUP = None
    GROUP_SIZE = 4
    NUM_ROUNDS = 1
    ENDOWMENT = 20
    MPCR = 0.4
    PUN_MULTIPLIER = 3
    BONUS_MULTIPLIER = 4
    MINIMUM_PLAYERS_PER_GROUP = 3
    TIMEOUTTIME = 40

class Subsession(BaseSubsession):
    def group_by_arrival_time_method(self, waiting_players):
        if len(waiting_players) >= C.GROUP_SIZE:
            return waiting_players[: C.GROUP_SIZE]
        return None

class Group(BaseGroup):
    PG_earnings = models.FloatField()
    collective_contribution = models.IntegerField()
    active_player_count = models.IntegerField(initial=0)
    game_terminated = models.BooleanField(initial=False)
    treatment = models.BooleanField()

    #Creates a variable that stores the number of men and women in the group as a variable at the individual level.

    def compute_group_gender(self):
        fem_count = 0
        male_count = 0
        self.treatment= random.choice(TREATMENT_OPTIONS)
        for p in self.get_players():
            if p.gender == 1:
                fem_count += 1
            elif p.gender == 2:
                male_count += 1
            else:
                pass
        for p in self.get_players():
            p.fem_in_group = fem_count
            p.male_in_group = male_count
            p.info_treatment = self.treatment


    def compute_active_players(self):
        self.active_player_count = 0
        for p in self.get_players():
            if p.time_out_dummy == False:
                self.active_player_count += 1
            else:
                self.active_player_count += 0

    def terminate_game_contribution_check(self):
        if self.active_player_count < C.MINIMUM_PLAYERS_PER_GROUP:
            self.game_terminated = True
        else:
            pass

    def set_bonus_rounds(self):
        #Sets multiple values at the player level, such as size of endowment, gender, round that counts for bonus and probability of winning said bonus
        for p in self.get_players():
            p.endowment = C.ENDOWMENT
            p.gender = p.participant.vars['gender']
            p.prob_of_winning = random.randint(1,100)
            if C.GROUP_SIZE == 4:
                p.belief_that_counts_1 = random.randint(0,8)
                p.belief_that_counts_2 = random.randint(0,8)
            if C.GROUP_SIZE < 4:
                p.belief_that_counts_1 = random.randint(0,5)
                p.belief_that_counts_2 = random.randint(0,5)

    # Allocates nicknames to each person. Currently still allocates nicknames to non-binary people. I can change that once a screening-out code has been added
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
    #Computes collective contribution and preliminary earnings, using contribution of each player. Only computes group-level outcomes
    #, such as group collective contribution and group earnings from the PGG
    def compute_group_earnings(self):
        if self.game_terminated == True: pass
        else:
            self.collective_contribution = sum(p.contribution for p in self.get_players())
            unrounded_earnings = self.collective_contribution * C.MPCR
            self.PG_earnings = round(unrounded_earnings, 2)
    # Note: Using the code in this way means that I always have to call compute_earnings after compute_group_earnings
    # Computes individual variables, such as remaining endowment and contribution of others in group
    def compute_earnings(self):
        if self.game_terminated == True: pass
        else:
            for p in self.get_players():
                p.remaining_endowment = p.endowment - p.contribution
                p.intermediate_earnings = p.remaining_endowment + self.PG_earnings
                p.contribution_others = self.collective_contribution - p.contribution

    #Post punishment, so this is where things get a little messy.
    # Gives bonus points if predictions are correct and received punishment, both dependent on id in group and total group size
    def compute_earnings_post_punishment(self):
        if self.game_terminated == True: pass
        else:
            for p in self.get_players():
                p.remaining_endowment = p.endowment - p.contribution
                if C.GROUP_SIZE > 3:
                    p.punishment_costs = p.punishment_co0 * (1- p.p2_time_out_dummy) + p.punishment_co1 * (1 - p.p3_time_out_dummy) + p.punishment_co2 * (1-p.p4_time_out_dummy)
                else:
                    p.punishment_costs = p.punishment_co0 * (1-p.p2_time_out_dummy) + p.punishment_co1 * (1-p.p3_time_out_dummy)
                if p.id_in_group == 1 and C.GROUP_SIZE > 3:
                    p.pun_received = p.p2_punishment_co0 + p.p3_punishment_co0 + p.p4_punishment_co0
                    if p.p2_punishment_co0 == p.pun_belief_co0:
                        p.bonus_pun_co0 += 1
                    if p.p3_punishment_co0 == p.pun_belief_co1:
                        p.bonus_pun_co1 += 1
                    if p.p4_punishment_co0 == p.pun_belief_co2:
                        p.bonus_pun_co2 += 1
                if p.id_in_group == 1 and C.GROUP_SIZE < 4:
                    p.pun_received = p.p2_punishment_co0 + p.p3_punishment_co0
                    if p.p2_punishment_co0 == p.pun_belief_co0:
                        p.bonus_pun_co0 += 1
                    if p.p3_punishment_co0 == p.pun_belief_co1:
                        p.bonus_pun_co1 += 1
                if p.id_in_group == 2 and C.GROUP_SIZE > 3:
                    p.pun_received = p.p2_punishment_co0 + p.p3_punishment_co1 + p.p4_punishment_co1
                    if p.p2_punishment_co0 == p.pun_belief_co0:
                        p.bonus_pun_co0 += 1
                    if p.p3_punishment_co1 == p.pun_belief_co1:
                        p.bonus_pun_co1 += 1
                    if p.p4_punishment_co1 == p.pun_belief_co2:
                        p.bonus_pun_co2 += 1
                if p.id_in_group == 2 and C.GROUP_SIZE < 4:
                    p.pun_received = p.p2_punishment_co0 + p.p3_punishment_co1
                    if p.p2_punishment_co0 == p.pun_belief_co0:
                        p.bonus_pun_co0 += 1
                    if p.p3_punishment_co1 == p.pun_belief_co1:
                        p.bonus_pun_co1 += 1
                if p.id_in_group == 3 and C.GROUP_SIZE > 3:
                    p.pun_received = p.p2_punishment_co1 + p.p3_punishment_co1 + p.p4_punishment_co2
                    if p.p2_punishment_co1 == p.pun_belief_co0:
                        p.bonus_pun_co0 += 1
                    if p.p3_punishment_co1 == p.pun_belief_co1:
                        p.bonus_pun_co1 += 1
                    if p.p4_punishment_co2 == p.pun_belief_co2:
                        p.bonus_pun_co2 += 1
                if p.id_in_group == 3 and C.GROUP_SIZE < 4:
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
# Part that allows for bonus earnings based on reported beliefs and a randomly-drawn bonus round
                if C.GROUP_SIZE > 3:
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
                    beliefs_list = [
                        p.prob_pre_co0,
                        p.prob_pre_co1,
                        p.prob_pre_co2,
                        p.prob_post_co0,
                        p.prob_post_co1,
                        p.prob_post_co2,
                        p.prob_pun_co0,
                        p.prob_pun_co1,
                        p.prob_pun_co2
                    ]
                    p.correct_prediction = bonuses_list[p.belief_that_counts_1]
                    p.prob_stated = beliefs_list[p.belief_that_counts_1]
                    probability = p.prob_of_winning / 100
                    p.won_lottery = 1 if random.random() < probability else 0
                    if p.prob_of_winning > p.prob_stated:
                        p.won_bonus = p.won_lottery
                    elif p.prob_of_winning <= p.prob_stated:
                        p.won_bonus = p.correct_prediction
                    p.bonus_earnings = p.won_bonus * C.BONUS_MULTIPLIER
                if C.GROUP_SIZE < 4:
                    bonuses_list = [
                        p.bonus_pre_co0,
                        p.bonus_pre_co1,
                        p.bonus_post_co0,
                        p.bonus_post_co1,
                        p.bonus_pun_co0,
                        p.bonus_pun_co1,
                    ]
                    beliefs_list = [
                        p.prob_pre_co0,
                        p.prob_pre_co1,
                        p.prob_post_co0,
                        p.prob_post_co1,
                        p.prob_pun_co0,
                        p.prob_pun_co1
                    ]
                    p.correct_prediction = bonuses_list[p.belief_that_counts_1]
                    p.prob_stated = beliefs_list[p.belief_that_counts_1]
                    probability = p.prob_of_winning / 100
                    p.won_lottery = 1 if random.random() < probability else 0
                    if p.prob_of_winning > p.prob_stated:
                        p.won_bonus = p.won_lottery
                    elif p.prob_of_winning <= p.prob_stated:
                        p.won_bonus = bonuses_list[p.belief_that_counts_1]
                    p.bonus_earnings = p.won_bonus * C.BONUS_MULTIPLIER
                p.both_punishment_costs = p.punishment_costs + p.pun_received_costs
                p.earnings = p.remaining_endowment + self.PG_earnings - p.punishment_costs - p.pun_received_costs + p.bonus_earnings
                p.participant.group_size = C.GROUP_SIZE
                if p.time_out_dummy == 1:
                    p.earnings = 0
                if p.earnings <= 0:
                    p.earnings = 0
    def set_other_contributions(self):
        if self.game_terminated == True: pass
        else:
            for p in self.get_players():
                    others = p.get_others_in_group()
                    if len(others) > 0:
                        p.p2_contribution = others[0].contribution
                    if len(others) > 1:
                        p.p3_contribution = others[1].contribution
                    if len(others) > 2:
                        p.p4_contribution = others[2].contribution

    def bonus_pre_beliefs(self):
        if self.game_terminated == True: pass
        else:
            for p in self.get_players():
                others = p.get_others_in_group()
                if p.pre_belief_co0 == p.p2_contribution :
                    p.bonus_pre_co0 += 1
                if p.pre_belief_co1 == p.p3_contribution :
                    p.bonus_pre_co1 += 1
                if C.GROUP_SIZE > 3:
                    if p.pre_belief_co2 == p.p4_contribution:
                        p.bonus_pre_co2 += 1

    def bonus_post_beliefs(self):
        if self.game_terminated == True: pass
        else:
            for p in self.get_players():
                if p.post_belief_co0 == p.p2_contribution:
                    p.bonus_post_co0 += 1
                if p.post_belief_co1 == p.p3_contribution:
                    p.bonus_post_co1 += 1
                if C.GROUP_SIZE > 3:
                    if p.post_belief_co2 == p.p4_contribution:
                        p.bonus_post_co2 += 1
                else: pass

    def set_other_time_outs(self):
        if self.game_terminated == True: pass
        else:
            for p in self.get_players():
                others = p.get_others_in_group()
                p.p2_time_out_dummy = others[0].time_out_dummy
                p.p3_time_out_dummy = others[1].time_out_dummy
                if C.GROUP_SIZE > 3:
                    p.p4_time_out_dummy = others[2].time_out_dummy
                if p.p2_time_out_dummy == True or p.p3_time_out_dummy == True or p.p4_time_out_dummy == True:
                    p.others_time_out_dummy = True



    def set_other_punishments(self):
        if self.game_terminated == True: pass
        else:
            for p in self.get_players():
                others = p.get_others_in_group()
                if C.GROUP_SIZE < 4:
                    if len(others) > 0:
                        p.p2_punishment_co0 = others[0].punishment_co0
                        p.p2_punishment_co1 = others[0].punishment_co1
                    if len(others) > 1:
                        p.p3_punishment_co0 = others[1].punishment_co0
                        p.p3_punishment_co1 = others[1].punishment_co1
                    if len(others) > 2:
                        p.p4_punishment_co0 = others[2].punishment_co0
                        p.p4_punishment_co1 = others[2].punishment_co1

                if C.GROUP_SIZE > 3:
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

    def randomize_ids(self):
        players = self.get_players()
        random.shuffle(players)
        for new_id, p in enumerate(players, start=1):
            p.id_in_group = new_id

    def set_other_names(self):
        import time
        for p in self.get_players():
            p.time_start_one = time.time()
            others = p.get_others_in_group()
            p.p2_nickname = others[0].nickname
            p.p3_nickname = others[1].nickname
            if len(others) > 2:
                p.p4_nickname = others[2].nickname
            p.participant.nickname_own = p.nickname
            p.participant.nickname_co0 = p.p2_nickname
            p.participant.nickname_co1 = p.p3_nickname
            if C.GROUP_SIZE > 3:
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
    time_start_one = models.FloatField(initial=0)
    time_start_two = models.FloatField(initial=0)
    time_out_dummy = models.BooleanField(default = False)
    info_contribution_clicked = models.BooleanField(default = False)
    info_punishment_clicked = models.BooleanField(default = False)
    info_bonus_clicked = models.BooleanField(default = False)
    info_dropout_clicked = models.BooleanField(default = False)
    others_time_out_dummy = models.BooleanField(default = False)
    last_heartbeat = models.FloatField(initial = 0)
    #PGG-related
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
    prob_of_winning = models.IntegerField()
    pre_belief_co0 = models.IntegerField()
    prob_pre_co0 = models.IntegerField()
    pre_belief_co1 = models.IntegerField()
    prob_pre_co1 = models.IntegerField()
    pre_belief_co2 = models.IntegerField()
    prob_pre_co2 = models.IntegerField()
    post_belief_co0 = models.IntegerField()
    prob_post_co0 = models.IntegerField()
    post_belief_co1 = models.IntegerField()
    prob_post_co1 = models.IntegerField()
    post_belief_co2 = models.IntegerField()
    prob_post_co2 = models.IntegerField()
    pun_belief_co0 = models.IntegerField()
    prob_pun_co0 = models.IntegerField()
    pun_belief_co1 = models.IntegerField()
    prob_pun_co1 = models.IntegerField()
    pun_belief_co2 = models.IntegerField()
    prob_pun_co2 = models.IntegerField()
    #Punishment
    punishment_costs = models.IntegerField()
    pun_received_costs = models.IntegerField()
    punishment_co0 = models.IntegerField()
    punishment_co1 = models.IntegerField()
    punishment_co2 = models.IntegerField()
    pun_received = models.IntegerField()
    both_punishment_costs = models.IntegerField()
    #Earnings
    earnings = models.CurrencyField()
    intermediate_earnings = models.FloatField()
    bonus_earnings = models.IntegerField()
    won_bonus = models.IntegerField( default = 0)
    won_lottery = models.IntegerField( default = 0)
    correct_prediction = models.IntegerField( default = 0)
    prob_stated = models.IntegerField( default = 0)

    #Fields filled in by other players
    p2_time_out_dummy = models.BooleanField(default = False)
    p2_nickname = models.StringField()
    p2_contribution = models.IntegerField()
    p2_punishment_co0 = models.IntegerField()
    p2_punishment_co1 = models.IntegerField()
    p2_punishment_co2 = models.IntegerField()
    p3_time_out_dummy = models.BooleanField(default=False)
    p3_nickname = models.StringField()
    p3_contribution = models.IntegerField()
    p3_punishment_co0 = models.IntegerField()
    p3_punishment_co1 = models.IntegerField()
    p3_punishment_co2 = models.IntegerField()
    p4_time_out_dummy = models.BooleanField(default=False)
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
        if C.GROUP_SIZE > 3:
            return self.get_others_in_group()[2]
        return None

#Helper functions defined below

def live_heartbeat(player, data):
    import time
    if data.get('type') == 'heartbeat':
        player.last_heartbeat = time.time()
        return{ 0: {'type': 'ack'}}

def update_heartbeat(player):
    import time
    player.last_heartbeat = time.time()

#Pages defined below

class MatchingWaitPage(WaitPage):
    group_by_arrival_time = True
    body_text = "Please wait while we match you with other participants..."

class DemographicsWait(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        group.randomize_ids()
        group.set_bonus_rounds()
        group.compute_group_gender()
        group.set_nicknames_group()
        group.set_other_names()

    @staticmethod
    def before_next_page(player, timeout_happened):
        update_heartbeat(player)
        import time
        player.time_start_one = time.time()

class GroupDisplay(Page):
    live_method = live_heartbeat
    timeout_seconds = C.TIMEOUTTIME
    @staticmethod
    def before_next_page(player, timeout_happened):
        update_heartbeat(player)
        if timeout_happened:
            player.time_out_dummy = True



class PreBeliefs(Page):
    live_method = live_heartbeat
    form_model = 'player'

    @staticmethod
    def get_timeout_seconds(player):
        if player.time_out_dummy == False:
            return C.TIMEOUTTIME
        if player.time_out_dummy == True:
            return 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        update_heartbeat(player)
        if timeout_happened:
            player.time_out_dummy = True

    @staticmethod
    def get_form_fields(player):
        fields = ['pre_belief_co0', 'pre_belief_co1',]
        if C.GROUP_SIZE > 3:
            fields += ['pre_belief_co2']
        return fields

    @staticmethod
    def vars_for_template(player):
        if C.GROUP_SIZE > 3:
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
        if C.GROUP_SIZE > 3:
            if values['pre_belief_co2'] > 20:
                return "Please report a number between 0 and 20 for each person"
        return None

class ProbPreBeliefs(Page):
    live_method = live_heartbeat

    @staticmethod
    def get_timeout_seconds(player):
        if player.time_out_dummy == False:
            return C.TIMEOUTTIME
        if player.time_out_dummy == True:
            return 1

    def before_next_page(player, timeout_happened):
        update_heartbeat(player)
        if timeout_happened:
            player.time_out_dummy = True
    form_model = 'player'
    @staticmethod
    def get_form_fields(player):
        fields = [ 'prob_pre_co0', 'prob_pre_co1']
        if C.GROUP_SIZE > 3:
            fields += [ 'prob_pre_co2']
        return fields

    @staticmethod
    def vars_for_template(player):
        if C.GROUP_SIZE > 3:
            return dict(
                prob_pre_co0_label='You reported that <strong> {} </strong>  will contribute <strong> {} </strong>  tokens. '
                                   'On a 0-100 percent scale, how likely do you think this is true?'.format(
                    player.p2_nickname,
                    player.pre_belief_co0),
                prob_pre_co1_label='You reported that <strong> {} </strong>  will contribute <strong> {} </strong> tokens. '
                                   'On a 0-100 percent scale, how likely do you think this is true?'.format(
                    player.p3_nickname,
                    player.pre_belief_co1),
                prob_pre_co2_label='You reported that <strong> {} </strong>  will contribute <strong> {} </strong>  tokens. '
                                   'On a 0-100 percent scale, how likely do you think this is true?'.format(
                    player.p4_nickname,
                    player.pre_belief_co2),
            )
        else:
            return dict(
                prob_pre_co0_label='You reported that <strong> {} </strong>  will contribute <strong> {} </strong>  tokens. '
                                   'On a 0-100 percent scale, how likely do you think this is true?'.format(
                    player.p2_nickname,
                    player.pre_belief_co0),
                prob_pre_co1_label='You reported that <strong> {} </strong>  will contribute <strong> {} </strong>  tokens. '
                                   'On a 0-100 percent scale, how likely do you think this is true?'.format(
                    player.p3_nickname,
                    player.pre_belief_co1),
            )

    @staticmethod
    def error_message(player, values):
        if values['prob_pre_co0'] > 100 or values['prob_pre_co1'] > 100:
            return "Please report a percentage between 0 and 100 for each person."
        if C.GROUP_SIZE > 3:
            if values['prob_pre_co2'] > 100:
                return "Please report a percentage between 0 and 100 for each person"
        return None

class Contribution(Page):
    live_method = live_heartbeat
    @staticmethod
    def get_timeout_seconds(player):
        if player.time_out_dummy == False:
            return C.TIMEOUTTIME
        if player.time_out_dummy == True:
            return 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        update_heartbeat(player)
        if timeout_happened:
            player.time_out_dummy = True
            player.contribution = 0
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
    template_name = 'PGG/ComputeContribution.html'
    @staticmethod
    def vars_for_template(player):
        import time
        now = time.time()
        max_wait = C.TIMEOUTTIME * 5
        if player.time_start_one > 0:
            elapsed = int(now - player.time_start_one)
            max_wait = max(0, max_wait - elapsed)
        return {
            'max_wait': max(0, max_wait),
            'expected_wait': C.TIMEOUTTIME * 1.5
        }


    @staticmethod
    def after_all_players_arrive(group):
        group.compute_active_players()
        group.terminate_game_contribution_check()
        group.compute_group_earnings()
        group.set_other_contributions()
        group.compute_earnings()
        group.bonus_pre_beliefs()


class PostBeliefs(Page):
    live_method = live_heartbeat
    @staticmethod
    def is_displayed(player):
        return not player.group.game_terminated

    @staticmethod
    def get_timeout_seconds(player):
        if player.time_out_dummy == False:
            return C.TIMEOUTTIME
        if player.time_out_dummy == True:
            return 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        update_heartbeat(player)
        import time
        player.time_start_two = time.time()
        if timeout_happened:
            player.time_out_dummy = True
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        fields = ['post_belief_co0', 'post_belief_co1']
        if C.GROUP_SIZE > 3:
            fields += ['post_belief_co2']
        return fields

    @staticmethod
    def vars_for_template(player):
        if player.group.game_terminated:
            return {}
        else:
            if C.GROUP_SIZE > 3:
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
        if C.GROUP_SIZE > 3:
            if values['post_belief_co2'] > 20:
                return "Please report a belief between 0 and 20 for each person"
        total = values['post_belief_co0'] + values['post_belief_co1']
        if C.GROUP_SIZE > 3:
            total += values['post_belief_co2']
        if total != player.contribution_others:
            return (
                f"Note: Your reported values add up to "
            f"{total} points. "
            f"Please ensure that your reported values add up to "
            f"{player.contribution_others} points."
            )
        return None


class ProbPostBeliefs(Page):
    live_method = live_heartbeat
    @staticmethod
    def is_displayed(player):
        return not player.group.game_terminated

    @staticmethod
    def get_timeout_seconds(player):
        if player.time_out_dummy == False:
            return C.TIMEOUTTIME
        if player.time_out_dummy == True:
            return 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        update_heartbeat(player)
        if timeout_happened:
            player.time_out_dummy = True
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        fields = ['prob_post_co0', 'prob_post_co1']
        if C.GROUP_SIZE > 3:
            fields += ['prob_post_co2']
        return fields

    @staticmethod
    def error_message(player, values):
        if values['prob_post_co0'] > 100 or values['prob_post_co1'] > 100:
            return "Please report a percentage between 0 and 100 for each person."
        if C.GROUP_SIZE > 3:
            if values['prob_post_co2'] > 100:
                return "Please report a percentage between 0 and 100 for each person"
        return None

    @staticmethod
    def vars_for_template(player):
        if player.group.game_terminated:
            return {}
        else:
            if C.GROUP_SIZE > 3:
                return dict(
                    prob_post_co0_label='You reported that <strong> {} </strong>  has contributed <strong> {} </strong> tokens. '
                                       'On a 0-100 percent scale, how likely do you think this is true?'.format(
                        player.p2_nickname,
                        player.post_belief_co0),
                    prob_post_co1_label='You reported that <strong> {} </strong>  has contributed <strong> {} </strong> tokens. '
                                       'On a 0-100 percent scale, how likely do you think this is true?'.format(
                        player.p3_nickname,
                        player.post_belief_co1),
                    prob_post_co2_label='You reported that <strong> {} </strong>  has contributed <strong> {} </strong>  tokens. '
                                       'On a 0-100 percent scale, how likely do you think this is true?'.format(
                        player.p4_nickname,
                        player.post_belief_co2),
                )
            else:
                return dict(
                    prob_post_co0_label='You reported that <strong> {} </strong>  has contributed <strong> {} </strong>  tokens. '
                                       'On a 0-100 percent scale, how likely do you think this is true?'.format(
                        player.p2_nickname,
                        player.post_belief_co0),
                    prob_post_co1_label='You reported that <strong> {} </strong>  has contributed <strong> {} </strong>  tokens. '
                                       'On a 0-100 percent scale, how likely do you think this is true?'.format(
                        player.p3_nickname,
                        player.post_belief_co1),
                )


class IntermediateResults(Page):
    live_method = live_heartbeat
    @staticmethod
    def get_timeout_seconds(player):
        if player.time_out_dummy == False:
            return C.TIMEOUTTIME
        if player.time_out_dummy == True:
            return 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        update_heartbeat(player)
        if timeout_happened:
            player.time_out_dummy = True

    @staticmethod
    def is_displayed(player):
        return player.info_treatment and not player.group.game_terminated

class PunBeliefsUncond(Page):
    live_method = live_heartbeat
    @staticmethod
    def is_displayed(player):
        return not player.group.game_terminated

    @staticmethod
    def get_timeout_seconds(player):
        if player.time_out_dummy == False:
            return C.TIMEOUTTIME
        if player.time_out_dummy == True:
            return 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        update_heartbeat(player)
        if timeout_happened:
            player.time_out_dummy = True
    form_model = 'player'
    @staticmethod
    def get_form_fields(player):
        fields = ['pun_belief_co0', 'pun_belief_co1']
        if C.GROUP_SIZE > 3:
            fields += ['pun_belief_co2']
        return fields

    @staticmethod
    def vars_for_template(player):
        if C.GROUP_SIZE > 3:
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
        if C.GROUP_SIZE > 3:
            if values['pun_belief_co2'] > 10:
                return "Please report a belief between 0 and 10 for each person"
        return None


class ProbPunBeliefs(Page):
    live_method = live_heartbeat
    @staticmethod
    def is_displayed(player):
        return not player.group.game_terminated

    @staticmethod
    def get_timeout_seconds(player):
        if player.time_out_dummy == False:
            return C.TIMEOUTTIME
        if player.time_out_dummy == True:
            return 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        update_heartbeat(player)
        if timeout_happened:
            player.time_out_dummy = True
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        fields = ['prob_pun_co0', 'prob_pun_co1']
        if C.GROUP_SIZE > 3:
            fields += ['prob_pun_co2']
        return fields

    @staticmethod
    def error_message(player, values):
        if values['prob_pun_co0'] > 100 or values['prob_pun_co1'] > 100:
            return "Please report a percentage between 0 and 100 for each person."
        if C.GROUP_SIZE > 3:
            if values['prob_pun_co2'] > 100:
                return "Please report a percentage between 0 and 100 for each person"
        return None

    @staticmethod
    def vars_for_template(player):
        if C.GROUP_SIZE > 3:
            return dict(
                prob_pun_co0_label='You reported that <strong> {} </strong>  will assign <strong> {} </strong> deduction points to you. '
                                    'On a 0-100 percent scale, how likely do you think this is true?'.format(
                    player.p2_nickname,
                    player.pun_belief_co0),
                prob_pun_co1_label='You reported that <strong> {} </strong>  will assign <strong> {} </strong> deduction points to you. '
                                    'On a 0-100 percent scale, how likely do you think this is true?'.format(
                    player.p3_nickname,
                    player.pun_belief_co1),
                prob_pun_co2_label='You reported that <strong> {} </strong>  will assign <strong> {} </strong> deduction points to you. '
                                    'On a 0-100 percent scale, how likely do you think this is true?'.format(
                    player.p4_nickname,
                    player.pun_belief_co2),
            )
        else:
            return dict(
                prob_pun_co0_label='You reported that <strong> {} </strong>  will assign <strong> {} </strong> deduction points to you. '
                                    'On a 0-100 percent scale, how likely do you think this is true?'.format(
                    player.p2_nickname,
                    player.pun_belief_co0),
                prob_pun_co1_label='You reported that <strong> {} </strong>  will assign <strong> {} </strong> deduction points to you. '
                                    'On a 0-100 percent scale, how likely do you think this is true?'.format(
                    player.p3_nickname,
                    player.pun_belief_co1),
            )


class Punishment(Page):
    live_method = live_heartbeat
    @staticmethod
    def is_displayed(player):
        return not player.group.game_terminated

    @staticmethod
    def get_timeout_seconds(player):
        if player.time_out_dummy == False:
            return C.TIMEOUTTIME
        if player.time_out_dummy == True:
            return 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        update_heartbeat(player)
        if timeout_happened:
            player.time_out_dummy = True
            player.punishment_co0 = 0
            player.punishment_co1 = 0
            player.punishment_co2 = 0

    form_model = 'player'
    @staticmethod
    def get_form_fields(player):
        fields = ['punishment_co0', 'punishment_co1']
        if C.GROUP_SIZE > 3:
            fields.append('punishment_co2')
        return fields

    @staticmethod
    def vars_for_template(player):
        if C.GROUP_SIZE > 3:
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
            or C.GROUP_SIZE > 3 and values['punishment_co2'] < 0):
                return "Value cannot be negative"
        if (values['punishment_co0'] > 10 or
            values['punishment_co1'] > 10 or
            C.GROUP_SIZE > 3 and values['punishment_co2'] > 10):
                return "Please choose a value between 0 and 10 for each person"
        return None

class ComputeResults(WaitPage):
    template_name = 'PGG/ComputeResults.html'

    @staticmethod
    def vars_for_template(player):
        import time
        now = time.time()
        max_wait = C.TIMEOUTTIME * 5
        if player.time_start_two > 0:
            elapsed = int(now - player.time_start_two)
            max_wait = max(0, max_wait - elapsed)
        return {
            'max_wait': max(0, max_wait),
            'expected_wait': C.TIMEOUTTIME * 1.5
        }

    @staticmethod
    def after_all_players_arrive(group):
        group.set_other_time_outs()
        group.set_other_punishments()
        group.compute_group_earnings()
        group.bonus_post_beliefs()
        group.compute_earnings_post_punishment()



class Results(Page):
    @staticmethod
    def is_displayed(player):
        return not player.group.game_terminated and not player.time_out_dummy
    form_model = "player"
    form_fields = ['info_contribution_clicked', 'info_punishment_clicked', 'info_bonus_clicked', 'info_dropout_clicked']

class Terminated(Page):
    @staticmethod
    def is_displayed(player): return player.group.game_terminated or player.time_out_dummy


# PAGES
page_sequence = [
    MatchingWaitPage,
    DemographicsWait,
    GroupDisplay,
    PreBeliefs,
    ProbPreBeliefs,
    Contribution,
    ComputeContribution,
    PostBeliefs,
    ProbPostBeliefs,
    IntermediateResults,
    Punishment,
    PunBeliefsUncond,
    ProbPunBeliefs,
    ComputeResults,
    Results,
    Terminated
]
