import string
from faker import Faker

fake = Faker()

class GenerateData:
    """
    Class to generate random project data
    """
    @staticmethod
    def fake_project_id():
        first_letter = fake.random.choice(string.ascii_letters)
        rest_characters = ''.join(fake.random.choices(string.ascii_letters + string.digits, k=10))
        project_id = first_letter + rest_characters
        print(project_id)
        return project_id
    
    @staticmethod
    def fake_name():
        return fake.word()