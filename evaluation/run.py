import os, argparse

from evaluate import evaluate
from utils import load_atomic_scores
from calculate import calculate

API_KEY = "your_openai_api_key_here"  # replace with your OpenAI API key
            
def get_args():
    parser = argparse.ArgumentParser(description="Run evaluation for persona fidelity.")

    parser.add_argument("--dir_task_prompt", type=str, default='./../persona_generation/prompts/tasks')
    parser.add_argument("--dir_eval_prompt", type=str, default='./prompts')
    parser.add_argument("--dir_result", type=str, default='./../persona_generation/results')
    parser.add_argument("--dir_atomic_score", type=str, default='./output/atomic_scores')
    parser.add_argument("--dir_fidelity_score", type=str, default='./output/fidelity_scores')

    # target persona and task
    ### example parameters
    parser.add_argument("--model", type=str, default='gpt-3.5-turbo-0125')  # default model, you can change it to any model you want
    parser.add_argument("--task", type=str, choices=['essay', 'smp', 'questionnaire'], default='essay')
    parser.add_argument("--personality", type=str, choices=['O', 'C', 'E', 'A', 'N'], default='O')
    parser.add_argument("--personality_level", type=str, choices=['high', 'medium', 'low'], default='high')

    parser.add_argument("--evaluator_model", type=str, default='gpt-4o')    # our paper utilized gpt-4o for evaluation, but you can use any model you want
    parser.add_argument("--api_key", type=str, default=API_KEY, help="OpenAI API key for model access")
    
    
    parser.add_argument("--evaluate", action='store_true')
    parser.add_argument("--calculate", action='store_true')
    parser.add_argument("--test", action='store_true')

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    print(args)

    # evaluate the personality level of atomic sentences
    if args.evaluate:
        print("Evaluating atomic sentences...")
        if not args.api_key:
            raise ValueError("API key is required for evaluation.")
        
        evaluate(args)

    # get persona fidelity scores
    dir_atomic_score = args.dir_atomic_score
    dir_fidelity_score = args.dir_fidelity_score
    model = args.model
    task = args.task
    personality = args.personality
    personality_level = args.personality_level

    # Load atomic scores
    atomic_scores = load_atomic_scores(dir_atomic_score, model, task, personality, personality_level)   # 3D array, [#iteration][#question][#atom_sentence]
    
    if args.calculate:
        print("Calculating persona fidelity scores...")
        calculate(args, atomic_scores)