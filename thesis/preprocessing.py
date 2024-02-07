'''
This is for preprocessing the EBM_NLP dataset
'''

import os
import glob
import datasets
# from datasets import Dataset
import pandas as pd


def fname_to_pmid(fname):
    pmid = os.path.splitext(os.path.basename(fname))[0].split('.')[0]
    return pmid

def create_datasets(doc_dict, labels):
    temp = datasets.Dataset.from_pandas(pd.DataFrame(doc_dict))
    temp = temp.cast_column("ner_tags", datasets.Sequence(datasets.ClassLabel(names=labels)))
    return temp
def train_test_split(data_set, train_test_size, validation_size):
    from datasets import DatasetDict
    train_testvalid = data_set.train_test_split(test_size=train_test_size)

    # Split the test to half test, half valid
    test_valid = train_testvalid['test'].train_test_split(test_size=validation_size)

    #Gather everything into one dataset dictionary
    train_test_valid_dataset = DatasetDict({
    'train': train_testvalid['train'],
    'test': test_valid['test'],
    'valid': test_valid['train']})

    return train_test_valid_dataset

# def limit_token_size(tokens): 
#     return len(tokens)<300

# def get_annotation(path, pmid):
#     return glob.glob(path + (f'./{pmid}.ann'))


# token_path = './ebm_nlp_2_00/documents/*.tokens'

# PIO = ['participants', 'interventions', 'outcomes']
# sub_fold = ['train_test_gold', 'train_test_crowd']

# def read_individual_docs(PIO):

#     doc = []
#     ann_fnames = glob.glob('../ebm_nlp_2_00/annotations/aggregated/hierarchical_labels/%s/train_test_gold/*.ann' %(PIO))
    
#     print('Reading %s files for %s' %(len(ann_fnames), PIO))
#     for fname in ann_fnames:

#         pmid = fname_to_pmid(fname)
#         tokens = open(f'../ebm_nlp_2_00/documents/{pmid}.tokens', encoding="utf-8").read().split()
#         annotations =[int(i) for i in open(fname, encoding="utf-8").read().split()]
        

#         # if limit_token_size(tokens): 
#         temp_dict={'pmid':pmid,
#                         "ner_tags": annotations,
#                         "tokens": tokens,
                    
#         }
#         doc.append(temp_dict)
        
#     return doc

# def get_similar_pmid(token_path,participant_path,outcome_path,intervention_path):
#     all_tokens = glob.glob(token_path)
#     participants = glob.glob(participant_path)
#     outcomes = glob.glob(outcome_path)
#     interventions = glob.glob(intervention_path)

#     toke_pmid = []
#     par_pmid = []
#     outcome_pmid =[] 
#     inter_pmid = []
#     for token in all_tokens: 
#         toke_pmid.append(fname_to_pmid(token))  
#     for participant in participants: 
#         par_pmid.append(fname_to_pmid(participant))
#     for outcome in outcomes: 
#         outcome_pmid.append(fname_to_pmid(outcome))
#     for intervention in interventions: 
#         inter_pmid.append(fname_to_pmid(intervention))

#     elements_in_all = list(set.intersection(*map(set, [toke_pmid, par_pmid, outcome_pmid, inter_pmid])))
#     return elements_in_all


# def read_alldocs(token_path, participant_path, outcome_path, intervention_path):
#     similar_pmid = get_similar_pmid(token_path,participant_path,outcome_path,intervention_path)

#     doc = []
    
#     print('Reading all files')
#     for pmid in similar_pmid:
#         tokens = open(f'../ebm_nlp_2_00/documents/{pmid}.tokens', encoding="utf-8").read().split()
         
#         path22 = f"../ebm_nlp_2_00/annotations/aggregated/hierarchical_labels/participants/train_test_gold/{pmid}.AGGREGATED.ann"
#         path33= f"../ebm_nlp_2_00/annotations/aggregated/hierarchical_labels/outcomes/train_test_gold/{pmid}.AGGREGATED.ann"
#         path44 = f"../ebm_nlp_2_00/annotations/aggregated/hierarchical_labels/interventions/train_test_gold/{pmid}.AGGREGATED.ann"

#         new_tag = mix_tag(path22, path44, path33)
#         temp_dict={'pmid':pmid,
#                     "tokens": tokens,
#                     "ner_tags":new_tag        
#                     }
#         doc.append(temp_dict)
        
#     return doc



# def mix_tag(part, inter, outcom):
#     part = open(part, encoding="utf-8").read().split()
#     inter = open(inter, encoding="utf-8").read().split()
#     outcom = open(outcom, encoding="utf-8").read().split()


#     inter_new_ref = {
#         '0':'0',
#         '1':'5',
#         '2':'6',
#         '3':'7',
#         '4':'8',
#         '5':'9',
#         '6':'10',
#         '7':'11',      

#         }
#     out_new_ref = {
#         '0':'0',
#         '1':'12',
#         '2':'13',
#         '3':'14',
#         '4':'15',
#         '5':'16', 
#         '6':'17'     

#         }
#     final_ann = part.copy()

#     for i, j in enumerate(inter):
#         if j !='0':
#             final_ann[i]=inter_new_ref[j]
#     for i, j in enumerate(outcom):
#         if j !='0':
#             final_ann[i]=out_new_ref[j]
#     return [int(i) for i in final_ann]

def train_test_split(data_set, train_test_size, validation_size):
    from datasets import DatasetDict
    train_testvalid = data_set.train_test_split(test_size=train_test_size)

    # Split the test to half test, half valid
    test_valid = train_testvalid['test'].train_test_split(test_size=validation_size)

    #Gather everything into one dataset dictionary
    train_test_valid_dataset = DatasetDict({
    'train': train_testvalid['train'],
    'test': test_valid['test'],
    'valid': test_valid['train']})

    return train_test_valid_dataset