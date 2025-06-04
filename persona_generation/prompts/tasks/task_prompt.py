import os, json


def call_prompt(dir_task, task, personality, question_format='generation'):
    """
    Call the appropriate prompt function based on the task type.
    Args:
        args: Command line arguments containing directory paths.
        domain: The domain of the task (e.g., 'health', 'education').
        personality: The personality type for the prompt.
        question_format: The format of the question (e.g., 'generation', 'mcq').
        task: The specific task type (e.g., 'essay', 'sns', 'questionnaire').
    Returns:
        A list of prompt(s), each prompt is a string.
            essay: list of one string
            smp: list of one string
            questionnaire: list of 10 strings
    """
    
    dir_path = os.path.join(dir_task)

    get_function = {
        'essay': get_prompt_essay,
        'smp': get_prompt_smp,
        'questionnaire': get_prompt_questionnaire
    }
    
    if task not in get_function:
        raise Exception(f"INVALID TASK: {task}. Expected one of {list(get_function.keys())}")
    
    prompts = get_function[task](dir_path, personality, question_format)  # call the appropriate function based on task

    if not isinstance(prompts, list):                                       
        raise Exception("Expected prompts to be a list.")
    
    if len(prompts) == 0:
        raise Exception("Expected prompts to be a non-empty list.")
    
    return prompts  # return list of prompts, each prompt is a string


def get_prompt_essay(dir_path, personality, question_format):
    file_name = 'instruction_essay.json'
    file_path = os.path.join(dir_path, file_name)

    data = read_json(file_path)

    instruction = data['instruction'][question_format]
    context = data[personality]

    prompt = [f"{instruction}\n{context}\nResponse:"]
    return prompt


def get_prompt_smp(dir_path, personality, question_format):
    file_name = 'instruction_smp.json'
    file_path = os.path.join(dir_path, file_name)

    data = read_json(file_path)

    instruction = data['instruction'][question_format]

    prompt = [f"{instruction}\nResponse:"]
    return prompt


def get_prompt_questionnaire(dir_path, personality, question_format):
    file_name = 'instruction_questionnaire.json'
    file_path = os.path.join(dir_path, file_name)

    data = read_json(file_path)

    instruction = data['instruction'][question_format]

    column_name = None
    if question_format == 'generation':
        column_name = 'questions'
    elif question_format == 'mcq':
        column_name = 'original_questions'
    else:
        raise Exception(f"INVALID QUESTION FORMAT: {question_format}")

    questions = data[personality][column_name]
    prompt = [f"{instruction} {q}\nResponse:" for q in questions]

    return prompt


def read_json(f_path):
    with open(f_path) as f:
        data = json.load(f)
    f.close()
    return data


def get_questionnaire_items(dir_path, personality):
    """
    Get the questionnaire items for a given personality and question format.
    
    Args:
        dir_path (str): The directory path containing the questionnaire data.
        personality (str): The personality type (e.g., 'O', 'C', 'E', 'A', 'N').
        question_format (str): The format of the questions (e.g., 'generation', 'mcq').
    
    Returns:
        list: A list of questionnaire items.
    """
    file_name = 'instruction_questionnaire.json'
    file_path = os.path.join(dir_path, file_name)

    data = read_json(file_path)

    questions = data[personality]['questions']

    return questions