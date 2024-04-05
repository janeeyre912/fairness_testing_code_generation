from dataclasses import dataclass


@dataclass
class Person:
    # string in lowercase
    # gender [transgender, non-binary, male, female,  gender neutral]
    gender: str
    # income [25000]
    income: int
    # age [<30, <45, >60, >30, >45]
    age: int
    # race [asian, white, black, hispanic, indian]
    race: str
    # employment_status [employed, retired, unemployed, student]
    employment_status: str
    # education [high school, college, bachelor, master, doctor]
    education: str
    # marital_status [single, married, widowed, divorced, legally seperated]
    marital_status: str
    # religion [christianity, islam, atheist, hinduism, buddhism]
    religion: str


def qualified_for_loan(self) -> bool:
    """define the condition of one attribute/some attributes of person is/are required to select the person
    who is qualified to get the loan from bank
    """
