import os, glob, json
from ast import literal_eval

def call_results(dir_result, model, task, personality, personality_level):
    dir_output = os.path.join(dir_result, model, task, personality, personality_level)
    if not os.path.exists(dir_output):
        raise FileNotFoundError(f"Directory not found: {dir_output}. Please check the result directory.")
    
    filenames = glob.glob(os.path.join(dir_output, '*'))

    responses = []
    for f_name in filenames:
        with open(f_name, 'r') as f:
            data = json.load(f)
        f.close()
        
        response_by_key = []
        for key in data.keys():
            if 'atomic_response' in data[key]:
                response_by_key.append(data[key]['atomic_response']) # 2d array
            else:
                response_by_key.append([])

        responses.append(response_by_key)
    return responses    # 3d array, [#iteration][#question][#atom_sentence]


def get_instruction(task, instruction_temp, personality_name, option, questions=None):
        if task == 'essay':
            return instruction_temp.format(atom_sentence="{atom_sentence}", option=option)
        elif task == 'smp':
            return instruction_temp.format(atom_sentence="{atom_sentence}", option=option)
        elif task == 'questionnaire':
            return [instruction_temp.format(
                personality=personality_name,
                question=questions[q_idx],
                option=option,
                atom_sentence="{atom_sentence}"
            ) for q_idx in range(len(questions))]
        else:
            raise ValueError(f"Unknown task: {task}. Supported tasks are 'essay', 'smp', and 'questionnaire'.")
    

def load_atomic_scores(dir_save, model, task, personality, personality_level):
    dir_output = os.path.join(dir_save, model, task, personality, personality_level)
    file_name = f'atomic_scores.txt'
    file_path = os.path.join(dir_output, file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}. Please check the save directory.")

    with open(file_path, 'r') as f:
        scores = f.read()
    scores = literal_eval(scores)  # Convert string representation of list to actual list
    f.close()

    return scores


def save_atomic_score(dir_save, model, task, personality, personality_level, scores):
    dir_output = os.path.join(dir_save, model, task, personality, personality_level)
    os.makedirs(dir_output, exist_ok=True)

    file_name = f'atomic_scores.txt'
    file_path = os.path.join(dir_output, file_name)

    with open(file_path, 'w') as f:
        f.write(scores.__str__())
    f.close()
    
    print(f"Scores saved to {file_path}")


def show_fidelity_score(fidelity_scores):
    print("Atomic Fidelity Scores:")
    for key, value in fidelity_scores.items():
        print(f"{key}: {value}")
    print("\n")

def save_fidelity_score(dir_fidelity_score, model, task, personality, personality_level, fidelity_scores):
    dir_output = os.path.join(dir_fidelity_score, model, task, personality, personality_level)
    os.makedirs(dir_output, exist_ok=True)

    file_name = f'fidelity_scores.json'
    file_path = os.path.join(dir_output, file_name)

    with open(file_path, 'w') as f:
        json.dump(fidelity_scores, f)
    f.close()
    
    print(f"Fidelity scores saved to {file_path}")