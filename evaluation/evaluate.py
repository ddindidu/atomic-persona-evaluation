import random

from prompts.eval_prompt import call_instruction_template, call_personality_name, call_option
from model import get_openai_client, eval_model
from utils import call_results, get_instruction, save_atomic_score

import sys
sys.path.append('./../')
from persona_generation.prompts.tasks.task_prompt import get_questionnaire_items


def evaluate(args):
    dir_task_prompt = args.dir_task_prompt
    dir_eval_prompt = args.dir_eval_prompt
    dir_result = args.dir_result
    dir_save = args.dir_atomic_score
    model = args.model
    task = args.task
    personality = args.personality
    personality_level = args.personality_level
    evaluator_model = args.evaluator_model

    # if the task is questionnaire, load the questions
    questions = []
    if task == 'questionnaire':
        questions = get_questionnaire_items(dir_task_prompt, personality)


    # call responses
    responses = call_results(dir_result, model, task, personality, personality_level)


    instruction_temp = call_instruction_template(dir_eval_prompt, task)
    personality_name = call_personality_name(personality)
    option = call_option(personality)


    # evaluator model
    eval_client = get_openai_client(args.api_key)    # you can change the evaluator model to any model you want
    # evaluation instruction
    INSTRUCTION = get_instruction(task, instruction_temp, personality_name, option, questions)


    refusal_keywords = get_refusal_keywords()

    scores = []
    for iteration_idx, response in enumerate(responses):
            
        scores_question = []
        for q_idx, atom_list in enumerate(response):
            
            atomic_scores = []

            # if the model response refused to generate persona-related responses, skip the evaluation
            full_response = ' '.join(atom_list)
            for keyword in refusal_keywords:
                if keyword.lower() in full_response.lower():
                    atomic_scores.append(99)
                    break
            if len(atomic_scores) > 0:
                scores_question.append(atomic_scores)
                continue

            # evaluate each atomic sentence
            for atom_sentence in atom_list:
                eval_instruction = INSTRUCTION[q_idx].format(atom_sentence=atom_sentence)
                
                # evaluate the atomic sentence
                if args.test:
                    eval_response = random.randint(1, 5)
                else:
                    eval_response = eval_model(client=eval_client, 
                                            evaluator_model=evaluator_model, 
                                            system_prompt=None, 
                                            main_prompt=eval_instruction)
                    eval_response = sent2scr(eval_response)    # convert the long response to a score (1-5)
                
                atomic_scores.append(eval_response)
            scores_question.append(atomic_scores)
        scores.append(scores_question)

    # save scores
    save_atomic_score(dir_save,  model, task, personality, personality_level, scores)



def sent2scr(text):
    # 9: a written text does not contain such a character
    # 999: an evaluator model refused to evaluate (e.g., "Based on the given sentence, I cannot select an option.")
        
    # valid short answer
    if len(text) == 1:
        try:
            score = int(text)
        except: # not a number
            score = 9

        if score in [1, 2, 3, 4, 5, 9]:
            return score
        else:
            print("Invalid: ", text)
            return 999

    # valid long answer
    if "1" in text:
        return 1
    elif "2" in text:
        return 2
    elif "3" in text:
        return 3
    elif "4" in text:
        return 4
    elif "5" in text:
        return 5
    elif "9" in text:
        return 9
    # invalid answer
    else:
        print("Invalid: ", text)
        return 999

def get_refusal_keywords():
    # recommended by gpt-4o
    refusal_keywords = [
        "I'm sorry, but I can't", 
        "I’m unable to",
        "For privacy reasons",
        "This topic is outside the scope",
        "I recommend consulting a professional",
        "I'm not qualified to",
        "For privacy and security reasons",
        "I can't perform that action",
        "This request goes against our content guidelines",
        "I can't create that type of content",
        "This topic is sensitive",
        "I can’t discuss that topic"
    ]
    general_refusals =  [
        "I'm sorry, but I can't", "I’m unable to", "I'm not allowed to", "I cannot provide", "I'm restricted from", "I’m not equipped to", "This request is outside my scope"
    ]
    policy_and_content_restrictions = [
        "content guidelines",
        "violates policy",
        "against our policy",
        "restricted topic",
        "inappropriate content",
        #"sensitive topic",
        "prohibited",
    ]
    privacy_and_security = [
        "privacy reasons",
        "for security reasons",
        "confidential information",
        "personal data",
        "identifying information",
        #"sensitive information",
        "data protection",
    ]
    ethical_and_harm_concerns = [
        "ethical implications",
        "cause harm",
        "may be misused",
        "risk of harm",
        "cannot assist with that",
        "ethical guidelines",
    ]
    medical_legal_and_financial_advice_limitations = [
        "consult a professional",
        "not qualified to",
        "recommend seeking advice from",
        "not a substitute for",
        "licensed professional",
        "legal (or medical/financial) advice"
    ]
    unsupported_or_infeasible_actions = [
        "I can't perform that action",
        "cannot directly assist with",
        "unable to fulfill that",
        "not capable of",
        "can’t complete that request"
    ]
    requests_for_fabrication_impersonation_or_falsification = [
        "cannot fabricate",
        "I can’t impersonate",
        "I’m unable to create false",
        "cannot provide fake",
        "I cannot generate that type of content",
    ]
    total_keywords = refusal_keywords +\
            general_refusals + policy_and_content_restrictions + privacy_and_security + ethical_and_harm_concerns +\
            medical_legal_and_financial_advice_limitations + unsupported_or_infeasible_actions + requests_for_fabrication_impersonation_or_falsification
    total_keywords = list(set(total_keywords))
    
    return total_keywords