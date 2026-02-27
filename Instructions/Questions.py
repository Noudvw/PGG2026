"""Question data for comprehension quiz questions."""

question_data = {
    1: {
        "question_answer": 20,
        "hint_group":"A",
    },
    2: {
        "question_answer": 20,
        "hint_group":"A"
    },
    3: {
        "question_answer": 32,
        "hint_group":"B",
    },
    4: {
        "question_answer": 32,
        "hint_group":"B"
    },
    5: {
        "question_answer": 36,
        "hint_group":"C",
    },
    6: {
        "question_answer": 30,
        "hint_group":"C"
    },
}

hint_messages = {
    "A": "Earnings consist of two parts: remaining endowment and earnings received from the group project. "
         "For these questions, earnings from the group project are zero",
    "B": "Earnings consist of two parts: remaining endowment and earnings received from the group project."
          "For these questions, the remaining endowment is zero",
    "C": "Earnings consist of two parts: remaining endowment and earnings received from the group project. "
         "To solve this question, you need to calculate remaining endowment and earnings from the group project, and then add both"
}