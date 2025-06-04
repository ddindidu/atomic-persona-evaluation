import os, json, argparse
import time
from prompts.personas.persona_prompt import call_persona_prompt
from prompts.tasks.task_prompt import call_prompt
from model import gen_model
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize


def chop_response(text):
    # change invalid characters to valid characters
    text = text.replace("\u2019", "'")
    text = text.replace("\u2014", "--")
    #text = text.replace("\n", " ")
    
    # Split by '.', '\n', or '!'
    # sentences = re.split(r'[.!\n]+', text)
    # split by sentence
    sentences = sent_tokenize(text)

    # Remove any empty strings from the result
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


def generate(args):
    """
    Generate persona-assigned generation based on the task and personality type.

    Args:
        args (argparse.Namespace): Command line arguments.
        
    Returns:
        Save generated outputs as json format.
    """
    
    task = args.task 
    personality = args.personality  
    personality_level = args.personality_level

    source_dir = args.dir_prompt
    source_dir_task = os.path.join(source_dir, 'tasks')
    source_dir_persona = os.path.join(source_dir, 'personas')

    persona_prompts = call_persona_prompt(source_dir_persona, personality, personality_level)
    print(f"Generated {len(persona_prompts)} persona prompts for personality {personality} at level {personality_level}.")
    print(persona_prompts)

    task_prompts = call_prompt(source_dir_task, task, personality)
    print(f"Generated {len(task_prompts)} task prompts for task {task} with personality {personality}.")
    print(task_prompts)

    output_dir = os.path.join(args.dir_output, args.model, task, personality, personality_level)
    os.makedirs(output_dir, exist_ok=True)

    for persona_idx, persona_pmpt in enumerate(persona_prompts):
        responses = dict()
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        for task_idx, task_prompt in enumerate(task_prompts):
            system_prompt = persona_pmpt
            main_prompt = task_prompt            

            model_response = gen_model(system_prompt, main_prompt)
            responses[task_idx] = dict()
            responses[task_idx]['raw_response'] = model_response
            responses[task_idx]['atomic_response'] = chop_response(model_response)

            # Print or save the generated prompts
            output_file = os.path.join(output_dir, f"persona_{personality}_{personality_level}_{persona_idx}_{timestamp}.json")
            with open(output_file, 'w') as f:
                json.dump(responses, f)


def get_args():
    parser = argparse.ArgumentParser(description="Run persona generation tasks.")
    parser.add_argument('--dir_prompt', type=str, default='./prompts')

    parser.add_argument('--task', type=str,default='essay', choices=['essay', 'smp', 'questionnaire'], help='Type of generation task.')
    parser.add_argument('--personality', type=str, default='O', choices=['O', 'C', 'E', 'A', 'N'], help='Personality type.')
    parser.add_argument('--personality_level', type=str, default='high', choices=['high', 'neutral', 'low'], help='Level of the personality.')
    
    parser.add_argument('--model', type=str, default='myModel')

    parser.add_argument('--dir_output', type=str, default='./results', help='Output directory to save generated prompts.')

    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()

    

    generate(args, task, personality, personality_level)
