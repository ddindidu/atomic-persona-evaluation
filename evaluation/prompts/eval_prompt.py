import os


PERSONALITY = {
    'O': "openness", 'C': "conscientiousness", 'E': "extroversion", 'A': "agreeableness", "N": "neuroticism"
}

OPTIONS =  {
    'O': "1) Very close-minded. 2) Moderately close-minded. 3) Neither open-minded or closed-minded. 4) Moderately open-minded. 5) Very open-minded. 9) None of the above.", # refusal 은 미리 거르자 string match로
    'C': "1) Very careless. 2) Moderately careless. 3) Neither conscientious or careless. 4) Moderately conscientious. 5) Very conscientious. 9) None of the above.",
    'E': "1) Very introverted. 2) Moderately introverted. 3) Neither extroverted or introverted. 4) Moderately extroverted. 5) Very extroverted. 9) None of the above.",
    'A': "1) Very disagreeable. 2) Moderately disagreeable. 3) Neither agreeable or disagreeable. 4) Moderately agreeable. 5) Very agreeable. 9) None of the above.",
    'N': "1) Very neurotic. 2) Moderately neurotic. 3) Neither neurotic or emotionally stable. 4) Moderately emotionally stable. 5) Very emotionally stable. 9) None of the above."
}


def call_instruction_template(source_dir, task):
    file_name = f'instruction_{task}.txt'
    file_path = os.path.join(source_dir, file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}. Please check the source directory.")
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    instruction_temp = ''.join([line for line in lines])
    
    return instruction_temp

def call_personality_name(personality):
    return PERSONALITY[personality]

def call_option(personality):
    return OPTIONS[personality]



