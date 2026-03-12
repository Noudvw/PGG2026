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

COUNTRIES = ["Afghanistan", "Albania", "Algeria", "American Samoa", "Andorra", "Angola", "Anguilla", "Antarctica",
             "Antigua and Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas",
             "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia",
             "Bonaire, St. Eustatius, and Saba", "Bosnia and Herzegovina", "Botswana", "Bouvet Island", "Brazil",
             "British Indian Ocean Territory", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia",
             "Cameroon", "Canada", "Cayman Islands", "Central African Republic", "Chad", "Chile", "China", "Christmas Island"
             "Cocos Islands", "Colombia", "Comoros", "Congo (Democratic Republic of the)", "Congo (The)", "Cook Islands",
             "Costa Rica", "Croatia", "Cuba", "Curaçao", "Cyprus", "Czechia", "Côte d'Ivoire", "Denmark", "Djibouti"
             , "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia",
             "Eswatini", "Ethiopia", "Falkland Islands", "Faroe Islands", "Fiji", "Finland", "France", "French Guiana",
             "French Polynesia", "French Southern Territories", "Gabon", "Gambia", "Georgia", "Germany", "Ghana",
             "Gibraltar", "Greece", "Greenland", "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guernsey", "Guinea", "Guinea-Bissau",
             "Guyana", "Haiti", "Heard Island and McDonald Islands", "Holy See (Vatican City State)","Honduras", "Hong Kong",
             "Hungary", "Iceland", "India","Indonesia", "Iran", "Iraq", "Ireland", "Isle of Man", "Israel", "Italy", "Jamaica",
             "Japan", "Jersey","Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea (the republic of)", "Kuwait", "Kyrgyzstan",
             "Lao People's Democratic Republic","Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania",
             "Luxembourg", "Macao", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Martinique", "Mauritania",
             "Mauritius", "Mayotte", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Montserrat",
             "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Caledonia", "New Zealand",
             "Nicaragua", "Niger", "Nigeria", "Niue", "Norfolk Island", "North Macedonia", "Northern Mariana Islands",
             "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru",
             "Philippines", "Pitcairn", "Poland", "Portugal", "Puerto Rico", "Qatar", "Romania", "Russian Federation",
             "Rwanda", "Réunion", "Saint Barthélemy", "Saint Helena, Ascension and Tristan da Cunha", "Saint Kitts and Nevis",
             "Saint Lucia", "Saint Martin (French part)", "Saint Pierre and Miquelon", "Saint Vincent and the Grenadines",
             "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone",
             "Singapore", "Sint Maarten (Dutch Part)", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa",
             "South Georgia and the South Sandwich Islands", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname",
             "Svalbard and Jan Mayen", "Sweden", "Switzerland", "Syrian Arab Republic", "Taiwan", "Tajikistan", "Tanzania",
             "Thailand", "Timor-Leste", "Togo", "Tokelau", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan",
             "Turks and Caicos Islands", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom",
             "United States of America", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Virgin Islands (British)",
             "Virgin Islands (US)", "Wallis and Futuna", "Western Sahara", "Yemen", "Zambia", "Zimbabwe", "Åland Islands"]



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
    education = models.StringField( label = "What is your highest completed level of education?",
                                     choices = [
                                         "No formal qualifications",
                                         "Secondary education (e.g. GED/GCSE)",
                                         "High school diploma / A-levels",
                                         "Technical/Community college",
                                         "Undergraduate degree (BA/BSc/other",
                                         "Graduate degree (MA/MSc/MPhil/other",
                                         "Doctorate degree (PhD/other",
                                         "Don't know/not applicable"
                                     ]
                                     )
    education_field = models.StringField( label = "What field of education did you receive your degree in?",
                                           choices = [
                                               "Arts & Humanities",
                                               "Education",
                                               "Economics",
                                               "Social Sciences",
                                               "Journalism & Information Business",
                                               "Administration & Law",
                                               "Mathematics & Statistics",
                                               "Information and Communication Technologies (ICT)",
                                               "Engineering, Manufacturing, and Construction",
                                               "Agriculture, Forestry, Fisheries, and Veterinary Science",
                                               "Health and Welfare",
                                               "Services",
                                               "Natural Sciences",
                                               "History",
                                               "Other",
                                               "None"
                                           ])
    nationality = models.StringField( label = "What is your nationality?", choices = COUNTRIES)
    residence = models.StringField( label = "What is your country of residence?", choices = COUNTRIES)
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
