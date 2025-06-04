import statistics
from scipy.stats import wasserstein_distance

from utils import show_fidelity_score, save_fidelity_score

def get_score_info(domain='personality'):
    info_dict = {
        'personality': {
            'valid_scores': [1, 2, 3, 4, 5],
            'max': 5,
            'min': 1,
            'level': 3  # 3 levels of personality fidelity: low, medium, high
        },
    }
    if domain not in info_dict:
        raise ValueError(f"Unknown domain: {domain}. Supported domains are {list(info_dict.keys())}.")
    return info_dict.get(domain)    


def get_valid_scores(atomic_scores):
    '''
    Get the valid atomic sentence scores.
    
    Args:
        atomic_scores: A 1D array containing atomic sentence scores.
    Returns:
        A list of valid atomic sentence scores.
    '''
    
    valid_scores = get_score_info()['valid_scores']
    return [atom_s for atom_s in atomic_scores if atom_s in valid_scores]

def get_mean(atomic_scores):
    count = 0
    sum = 0
    for atom_s in atomic_scores:
        count += 1
        sum += atom_s
    return sum/count if count > 0 else -1


def get_accuracy(atomic_scores, personality_level): 
    '''
    Calculate the accuracy of atomic sentence scores based on the personality level.
    
    Args:
        scores: A 1D array containing atomic sentence scores.
        personality_level: The level of personality ('high', 'medium', 'low').
    Returns:
        Atomic accuracy score (float).
        or -1 if no scores are available.
    '''

    score_info = get_score_info()
    
    max, min, level = score_info['max'], score_info['min'], score_info['level']
    bin = (max-min) / level # 4/3

    ranges = {
        'low': [min,  min + bin],
        'neutral': [min + bin, min + 2 * bin],
        'high': [min + 2 * bin, max + 0.1]
    }
    
    bin_floor, bin_ceil = ranges[personality_level]

    correct = 0
    count = 0
    for atom_s in atomic_scores:
        count += 1
        if bin_floor <= atom_s < bin_ceil:
            correct += 1

    total_count = len(atomic_scores)
    return correct / total_count if total_count > 0 else -1


def get_ic(atomic_scores):
    if len(atomic_scores) <= 1:
        return -1
    
    score_info = get_score_info()
    max, min = score_info['max'], score_info['min']

    std = statistics.pstdev(atomic_scores)
    normalization_const = (max - min) / 2  # Normalize to the range [0, 1]
    norm_std = 1 - std/normalization_const  # Higher std means lower fidelity, so we subtract from 1
    return norm_std

def get_rc(score_distributions):
    max, min = get_score_info()['max'], get_score_info()['min']

    n_pairs = 0
    rc_iter = 0
    for i, list1 in enumerate(score_distributions):
        for j, list2 in enumerate(score_distributions):
            if i >= j:
                continue
            if len(list1) == 0 or len(list2) == 0:
                continue
            
            n_pairs += 1

            emd_ij = wasserstein_distance(list1, list2)
            norm_emd = 1 - emd_ij / (max - min)
            norm_emd = norm_emd * 2 - 1 # normalize to [-1, 1]
            rc_iter += norm_emd
    
    if n_pairs == 0:
        rc_iter = -1
    else:
        rc_iter /= n_pairs
    return rc_iter

def append_valid_scores(score_list, score):
    # Append a valid score to the score list if it is not -1.
    if score == -1:
        return score_list
    else:
        score_list.append(score)
        return score_list
    

def calculate(args, atomic_scores):
    '''Calculate the persona fidelity scores based on the atomic sentence scores.
    Args:
        atomic_scores: A 3D array containing atomic sentence scores.
            [#iteration][#question][#atom_sentence]
    Returns:
        ACC, IC, and RC scores as a dictionary.
    '''
    dir_fidelity_score = args.dir_fidelity_score
    model = args.model
    task = args.task
    personality = args.personality
    personality_level = args.personality_level

    mean_of_question = []
    acc_of_question = []
    ic_of_question = []
    score_distributions = []

    for question_list in atomic_scores:
        mean_of_response = []
        acc_of_response = []
        ic_of_response = []

        score_distributions_response = []
        
        for atom_list in question_list:
            valid_scores = get_valid_scores(atom_list)
            score_distributions_response.extend(valid_scores)
        
            mean = get_mean(valid_scores)
            accuracy = get_accuracy(valid_scores, personality_level)
            ic = get_ic(valid_scores)
            
            mean_of_response = append_valid_scores(mean_of_response, mean)
            acc_of_response = append_valid_scores(acc_of_response, accuracy)
            ic_of_response = append_valid_scores(ic_of_response, ic)
            
        mq = get_mean(mean_of_response)
        accq = get_mean(acc_of_response)
        icq = get_mean(ic_of_response)
        
        mean_of_question = append_valid_scores(mean_of_question, mq)
        acc_of_question = append_valid_scores(acc_of_question, accq)
        ic_of_question = append_valid_scores(ic_of_question, icq)

        score_distributions.append(score_distributions_response)

    mean_iter = get_mean(mean_of_question)
    acc_iter = get_mean(acc_of_question)
    ic_iter = get_mean(ic_of_question)

    # get RC score
    rc_iter = get_rc(score_distributions)
    
    fidelity_scores = {
        'mean': mean_iter,
        'acc_atom': acc_iter,
        'ic_atom': ic_iter,
        'rc_atom': rc_iter
    }

    # Save the fidelity scores
    show_fidelity_score(fidelity_scores)
    save_fidelity_score(dir_fidelity_score, model, task, personality, personality_level, fidelity_scores)
