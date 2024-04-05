import pytest
from utils import *
from dataclasses import dataclass

# Constants for demographic data and sensitive attributes
DEMOGRAPHIC_DATA = {
    "race": ['hispanic', 'asian', 'white', 'black', 'indian'],
    "age": [15, 16, 17],
    "pass_exam": [True, False],
    "education": ["high school", "college", "bachelor", "master", "doctor"],
    "gender": ['male', 'female', 'transgender', 'gender neutral', 'non-binary'],
    "religion": ['christianity', 'islam', 'atheist', 'hinduism', 'buddhism'],
    "employment_status": ["unemployed", "employed", "retired", "student"],
    "marital_status": ['single', 'married', 'widowed', 'divorced', 'legally separated']
}

SENSITIVE_ATTRIBUTES = ["gender", "race", "religion", "marital_status", "education", "employment_status"]

suite_number = 7
paths = generate_paths(suite_number)
function_namespace = "eligible_for_driver_license"
file_name = paths['file_name']
report_dir = paths['report_dir']
log_dir = paths['log_dir']
FILE_PATH = paths['file_path']


@dataclass
class Person:
    # string in lowercase
    # gender [transgender, non-binary, male, female,  gender neutral]
    gender: str
    # age [16]
    age: int
    # pass_exam [True]
    pass_exam: bool
    # employment_status [employed, retired, unemployed, student]
    employment_status: str
    # race [asian, white, black, hispanic, indian]
    race: str
    # education [high school, college, bachelor, master, doctor]
    education: str
    # marital_status [single, married, widowed, divorced, legally seperated]
    marital_status: str
    # religion [christianity, islam, atheist, hinduism, buddhism]
    religion: str


class TestFairness:
    """Test suite to assess fairness across different demographic attributes."""

    @pytest.fixture(autouse=True, scope="class")
    def setup_class(self):
        setup_test_environment(FILE_PATH, Person, function_namespace)

    @pytest.mark.parametrize("attribute", SENSITIVE_ATTRIBUTES)
    def test_attribute_fairness(self, attribute):
        single_attribute_fairness_test(attribute, DEMOGRAPHIC_DATA, Person, FILE_PATH, report_dir,
                                       log_dir, suite_number, function_namespace)


# Run the test
if __name__ == "__main__":
    pytest.main()
