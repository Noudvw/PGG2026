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
    age = models.IntegerField( label= "What is your age?")
    nationality = models.StringField( label = "What is your nationality?")
    residence = models.StringField( label = "What is your country of residence?")
    education = models.IntegerField( label = "What is your highest completed level of education?",
                                     choices = [
                                         [0, "No formal qualifications"],
                                         [1, "Secondary education (e.g. GED/GCSE)"],
                                         [2, "High school diploma / A-levels"],
                                         [3, "Technical/Community college"],
                                         [4, "Undergraduate degree (BA/BSc/other"],
                                         [5, "Graduate degree (MA/MSc/MPhil/other"],
                                         [6, "Doctorate degree (PhD/other"],
                                         [7, "Don't know/not applicable"]
                                     ]
                                     )
    education_field = models.IntegerField( label = "What field of education did you receive your degree in?",
                                           choices = [
                                               [0, "Arts & Humanities"],
                                               [1, "Education"],
                                               [2, "Economics"],
                                               [3, "Social Sciences"],
                                               [4, "Journalism & Information Business"],
                                               [5, "Administration & Law"],
                                               [6, "Mathematics & Statistics"],
                                               [7, "Information and Communication Technologies (ICT)"],
                                               [8, "Engineering, Manufacturing, and Construction"],
                                               [9, "Agriculture, Forestry, Fisheries, and Veterinary Science"],
                                               [10, "Health and Welfare"],
                                               [11, "Services"],
                                               [12, "Natural Sciences"],
                                               [13, "History"],
                                               [14, "Other"]
                                           ])
    siblings = models.IntegerField( label = "How many siblings do you have?")

# PAGES
class DemoQuestions(Page):
    form_model = "player"
    form_fields = ["gender", "age", "nationality", "residence", "education", "education_field", "siblings"]

    #Stores gender for usage in the PGG
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.vars['gender'] = player.gender

    @staticmethod
    def error_message(player, values):
        if values['age'] > 120:
            return "Please return an age below 120 years old."
        if values['siblings'] > 15:
            return ('Please return a number of siblings of 15 or lower. '
                    'If you have more than 15 siblings, please return 15')

class DemoWait(WaitPage):
    pass

page_sequence = [
    DemoQuestions,
    DemoWait,
]
