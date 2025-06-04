import os, json


def call_persona_prompt(source_dir, personality, personality_level):
    """
    Returns a list of prompts for the given personality and question format.

    Args:
        source_dir (str): 
            The directory containing the persona prompt files.
        personality (str):
            The personality type.
            {'O', 'C', 'E', 'A', 'N'} (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
        personality_level (str): 
            The level of the personality. 
            {'high', 'medium', 'low'}

    Returns:
        prompts (list):
            A list of prompts, each prompt is a string.
    """

    prompts = []

    instruction_templates = call_instruction_template(source_dir)
    entities = call_persona_entity(source_dir, personality, personality_level)

    for inst in instruction_templates:
        for entity in entities:
            prompt = inst.format(entity)
            prompts.append(prompt)
    
    return prompts


def call_instruction_template(source_dir, n=None):
    file_name = 'persona_instruction.txt'
    file_path = os.path.join(source_dir, file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}. Please check the source directory.")
    
    inst = []

    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line= line.strip()
            inst.append(line)

    if n is not None:
        inst = inst[:n]

    return inst


def call_persona_entity(source_dir, personality, personality_level):
    file_name = 'entity_personality.json'
    file_path = os.path.join(source_dir, file_name)

    with open(file_path, 'r') as f:
        data = json.load(f)
    
    entities = data[personality_level][personality]
    
    return entities