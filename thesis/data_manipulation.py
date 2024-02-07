# See some difintions in ner/data/swt/README.md

import json
import re
import os


def read_swt_records(json_file):
    output = []
    with open(json_file, encoding='utf-8') as f:
        for line in f:
            output.append(json.loads(line))
    return output


def read_swt_annotated_records(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def write_records(records, file_path):
    with open(file_path, "w", encoding='utf-8') as f:
        json.dump(records, f)



# deprecated: use read_swt_annotated_records instead
def read_swt_annotations_as_dict(json_file):
    with open(json_file, "r") as f:
        annos = json.load(f)

    return annos


def clean_and_add_annotation_to_swt_records(annos, records):
    clean_records = []

    for record in records:
        if "filenameUploadedAnnotated" not in record or "abstractText" not in record:
            continue
        if record["filenameUploadedAnnotated"] in annos:
            text = record["abstractText"]
            if "title" in record:
                text = record["title"] + "." + text

            pmid = record["pubmedId"] if "pubmedId" in record else "NA"
            new_record = {"pmid": pmid, "paper": record["filenameUploadedAnnotated"], "text": text,
                          "annotations": annos[record["filenameUploadedAnnotated"]]}
            clean_records.append(new_record)
    return clean_records

def get_methods(file_name, filepath):
    temp_path =  os.path.join(filepath, (file_name + '.txt') )
    try: 
        method =open(temp_path, encoding="utf-8").read()
        method = method.split('\n')[1]
    except FileNotFoundError: 
        method = ''
    return method

def get_context(file_name, filepath):
    temp_path =  os.path.join(filepath, (file_name + '.context') )
    context_dict = {}
    
    try: 
        contexts =open(temp_path, encoding="utf-8").read()
        contexts = contexts.split('\n')
        for context in contexts:
            if context !='':
                temp = context.split('::')
                context_dict[temp[0]]= temp[1]
            else: 
                pass

    except FileNotFoundError: 
        contexts = 'N/A'
        

    return context_dict


  


def create_clean_records(annotation_records, context_path):
    clean_records = []
    count_context = 0
    print('getting abstract')

    for record in annotation_records:
        if "abstractTextPubmed" in record:
            text = record["abstractTextPubmed"] 
        elif "abstractText" in record:
            text = record["abstractText"]
        else:
            text = ""
        filename = record["filenameUploadedAnnotated"] if "filenameUploadedAnnotated" in record else ""
        title_and_text = record["title"] + ". " + text
        context_dict = get_context(filename, context_path) 
        if context_dict != 'N/A':
            count_context+=1    


        annotations = {}
        for annotation in record["papers_annotations"]:
            annotations[annotation["annotationVariable"]] = annotation["annotationContent"]

        pmid = record["pubmedId"] if "pubmedId" in record else "NA"
        new_record = {"pmid": pmid,
                      "paper": filename,
                      "text": title_and_text,
                      "context": context_dict,
                      "annotations": annotations}

            
        clean_records.append(new_record)
    print(f'the lenght of document is {len(clean_records)} total number of annotated records is {len(annotation_records)},total number of context is {count_context}')
    
    return clean_records

def splitter(n, s):
    pieces = s.split()
    return (" ".join(pieces[i:i+n]) for i in range(0, len(pieces), n))

def split_list(input_list, chunk_size):
    """
    Split a list into pieces of a predefined length.

    Parameters:
    - input_list: The list to be split.
    - chunk_size: The size of each chunk.

    Returns:
    A list of chunks.
    """
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]




def create_clean_records_with_methods(annotation_records, method_path, context_path):
    clean_records = []
    count_meth = 0
    count_context = 0
    print("getting abstract and method")

    for record in annotation_records:
        if "abstractTextPubmed" in record:
            text = record["abstractTextPubmed"] 
        elif "abstractText" in record:
            text = record["abstractText"]
        else:
            text = ""
        filename = record["filenameUploadedAnnotated"] if "filenameUploadedAnnotated" in record else ""
        title_and_text = record["title"] + ". " + text
        #get the methods for the file name from the method folder
        method = get_methods(filename, method_path)
        if method != '':
            count_meth+=1
        title_and_text_and_method = title_and_text +'\n\n' + method

        context_dict = get_context(filename, context_path) 
        if context_dict != 'N/A':
            count_context+=1    


        annotations = {}
        for annotation in record["papers_annotations"]:
            annotations[annotation["annotationVariable"]] = annotation["annotationContent"]

        pmid = record["pubmedId"] if "pubmedId" in record else "NA"

        new_record = {"pmid": pmid,
                      "paper": filename,
                      "text": title_and_text_and_method,
                      "context": context_dict,
                      "annotations": annotations}

            
        clean_records.append(new_record)
    print(f'total number of annotated records is {len(annotation_records)} and total number of method added is {count_meth}, total number of context is {count_context}')
    return clean_records

def create_splitted_clean_records_with_methods_and_context(annotation_records, method_path, context_path, split):
    clean_records = []
    count_meth = 0
    count_context = 0
    print(f"getting {split} splitted abstract and method")

    for record in annotation_records:
        if "abstractTextPubmed" in record:
            text = record["abstractTextPubmed"] 
        elif "abstractText" in record:
            text = record["abstractText"]
        else:
            text = ""
        filename = record["filenameUploadedAnnotated"] if "filenameUploadedAnnotated" in record else ""
        title_and_text = record["title"] + ". " + text
        #get the methods for the file name from the method folder
        method = get_methods(filename, method_path)
        if method != '':
            count_meth+=1
        title_and_text_and_method = title_and_text +'\n\n' + method

        #get the methods for the file name from the method folder
        context_dict = get_context(filename, context_path) 
        if context_dict != 'N/A':
            count_context+=1    

        annotations = {}
        for annotation in record["papers_annotations"]:
            annotations[annotation["annotationVariable"]] = annotation["annotationContent"]

        pmid = record["pubmedId"] if "pubmedId" in record else "NA"

        for piece in splitter(split, title_and_text_and_method):
            new_record = {"pmid": pmid,
                        "paper": filename,
                        "text": piece,
                        "context": context_dict,
                        "annotations": annotations}

            clean_records.append(new_record)
    print(f'the lenght of document is {len(clean_records)} total number of annotated records is {len(annotation_records)} total number of method added is {count_meth}, total number of context is {count_context}')
    return clean_records


def create_splitted_clean_records_with_methods(annotation_records, method_path, split):
    clean_records = []

    for record in annotation_records:
        if "abstractTextPubmed" in record:
            text = record["abstractTextPubmed"] 
        elif "abstractText" in record:
            text = record["abstractText"]
        else:
            text = ""
        filename = record["filenameUploadedAnnotated"] if "filenameUploadedAnnotated" in record else ""
        title_and_text = record["title"] + ". " + text
        #get the methods for the file name from the method folder
        method = get_methods(filename, method_path)
        title_and_text_and_method = title_and_text +'\n\n' + method

        annotations = {}
        for annotation in record["papers_annotations"]:
            annotations[annotation["annotationVariable"]] = annotation["annotationContent"]

        pmid = record["pubmedId"] if "pubmedId" in record else "NA"
        #split method and text into chunks and append for the same pmid

        for piece in splitter(split, title_and_text_and_method):
            new_record = {"pmid": pmid,
                        "paper": filename,
                        "text": piece,
                        "annotations": annotations}

                
            clean_records.append(new_record)
    return clean_records


def read_sentence_anno(json_file):
    with open(json_file) as f:
        annos = json.load(f)
    return annos


def normalize(text):
    return re.sub(r'[^\w\s]', '', text).lower() # remove any character that isnt a word and the resulting text should be lower case


def read_swt_cond_annotations_as_dict(file_path):
    """ deprecated"""
    with open(file_path, "r") as f:
        lines = f.readlines()
    annos = {line.split(":")[0]: line.split(":")[1].strip() for line in lines}

    return annos


def clean_and_add_cond_annotation_to_swt_records(annos, records):
    """ deprecated"""
    clean_records = []

    for record in records:
        if "filenameUploadedAnnotated" not in record or "abstractText" not in record:
            continue
        if record["filenameUploadedAnnotated"] in annos:
            record["swt_annotation"] = annos[record["filenameUploadedAnnotated"]]
            clean_records.append(record)
    return clean_records


def count_annos_in_abstract(records, anno):
    found = []
    total = 0
    for r in records:
        if anno in r["annotations"]:
            total += 1
            if normalize(r["annotations"][anno]) in normalize(r["text"]):
                found.append(r["annotations"][anno])
    return found, total


# def filter_records_by_labels(records, labels, in_abstract=False):
#     if not isinstance(labels, list):
#         labels = [labels]

#     new_records = []

#     for r in records:
#         for l in labels:
#             if l in r["annotations"]:
#                 if in_abstract:
#                     if normalize(r["annotations"][l]) in normalize(r["text"]):
#                         new_records.append(r)
#                 else:
#                     new_records.append(r)

#     return new_records



##################################################################### NEW CODES ########################################################
import re

#create any lenght of zeros
def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros

# clean the string a little
def clean_text(string): ### dont have to replace
    punc = '''
    !";:,.<>\/?@*+_[]=
    '''
    
    for ele in string: 
        if ele in ["’","'","(", ")"]:
            string = string.replace(ele, "").strip() 

        elif ele in punc: 
            string = string.replace(ele, " ").strip()
        
    
    return string

def add_spaces(text):
    updated_text = ""
    punc = '''
    !";:,.<>\/?@*+_[]=(%)&+
    '''
    for char in text:
        if char in punc:
            updated_text += ' ' + char + ' '
        else:
            updated_text += char
    return updated_text.lower()

def clean_string(input_string):
    normalized_str = normalize(input_string.lower())
     
    # Define the regular expression pattern to match round brackets with capital letter words inside
    round_bracket_pattern =  r"\s\([A-Z][a-zA-Z0-9]{1,5}\)" 
    cleaned_string = re.sub(round_bracket_pattern, ' ', normalized_str)

    round_bracket_pattern =  r"\([A-Z][a-zA-Z0-9]{1,5}\)" 
    cleaned_string = re.sub(round_bracket_pattern, ' ', cleaned_string)


    # Define the regular expression pattern to match square brackets with any digit inside
    square_bracket_pattern = r'\[\d]'
    cleaned_string = re.sub(square_bracket_pattern, '', cleaned_string)

    # Define the regular expression pattern to match square brackets with any double digit inside
    square_bracket_pattern = r'\[\d\d]'
    cleaned_string = re.sub(square_bracket_pattern, '', cleaned_string)

     # Use the `replace()` method to replace double spaces with a single space
    cleaned_string = cleaned_string.replace('  ', ' ')

    cleaned_string = clean_text(cleaned_string)

    # if remove_punctuation: 
    #     cleaned_string = clean_text(cleaned_string)
    # else: 
    #     cleaned_string = cleaned_string

    return cleaned_string.strip()

def find_phrase_indices(sentence, phrase):
    words = sentence.split()
    phrase_words = phrase.split()
    
    indices = []
    for i in range(len(words) - len(phrase_words) + 1):
        if words[i:i+len(phrase_words)] == phrase_words:
            indices.extend(range(i, i+len(phrase_words)))
    
    return indices
def remove_first_last_word(sentence):
    # Split the sentence into words
    words = sentence.split()

    # Remove the first and last word
    if len(words) >= 3:  # Ensure the sentence has at least three words
        words = words[1:-1]

    # Join the remaining words back into a sentence
    result = ' '.join(words)

    return result

# def tokenize_align_labels(example, label_all_tokens = True):
#     # tokenized_input = tokenizer(example['tokens'], truncation = True, is_split_into_words=True, max_length = 450)
#     tokenized_input = tokenizer(example['tokens'], truncation = True, is_split_into_words=True)

#     labels = []
#     for i , label in enumerate(example['ner_tags']):
#         word_ids = tokenized_input.word_ids(batch_index=i)
#         previous_word_idx = None

#         label_ids = []
#         for word_idx in word_ids:
#             if word_idx is None: 
#                 label_ids.append(-100)
#             elif word_ids!= previous_word_idx:
#                 label_ids.append(label[word_idx])
#             else: 
#                 label_ids.append(label[word_idx] if label_all_tokens else -100) 
#             previous_word_idx = word_idx
#         labels.append(label_ids)
#     tokenized_input['labels'] = labels
#     return tokenized_input

from collections import Counter

def get_key(val, label_dict):
    for key, value in label_dict.items():
        if val == value:
            return key
    return "key doesn't exist"




def count_values(lst):
    # Use Counter to count occurrences of each value in the list
    value_counts = Counter(lst)
    
    # Convert the Counter to a dictionary for a more readable output
    count_dict = dict(value_counts)
    
    return count_dict

def explore_annotations(dataset, label_dict):
    all_annotations = []

    for records in dataset: 
        temp_tag = records['ner_tags']
        all_annotations.extend(temp_tag)
    print(f'There are {len(all_annotations)} annotations in the dataset')
     
    return [get_key(x, label_dict) for x in all_annotations] 

def normalize_tag_name(tag):
    if tag in [ 'condition', 'condition_1', 'condition_2', 'condition_3', 'condition_4', 'condition_5', 'condition_6', 'condition_7']: 
        tag= 'condition'
    elif tag in ['design', 'design_1', 'design_2', 'design_3', 'design_4', 'design_5']:
        tag = 'design'
    elif tag in ['subject_1', 'subject_2', 'subjects', 'subjects_1', 'subjects_2', 'subjects_3', 'subjects_4', 'subjects_5', 'subjekts', 'sujects']:
        tag = 'subjects'
    elif tag in [ 'group_A', 'group_A_1', 'group_A_2', 'group_A_3', 'group_A_4']:
        tag = 'group_A'
    elif tag in ['groub_B_1', 'group_B', 'group_B _2', 'group_B_1', 'group_B_2', 'group_B_3', 'group_B_4' ]:
        tag = 'group_B'
    elif tag in [ 'group_C', 'group_C_1', 'group_C_2', 'group_C_3' ]:
        tag = 'group_C'
    elif tag in [ 'group_D', 'group_D_1', 'group_D_2', 'group_D_3']:
        tag = 'group_D'
    elif tag in  ['therapy','therapy_1', 'therapy_2', 'therapy_3', 'therapy_4', 'therapy_5', 'therapy_6', 'therapy_7']:
        tag ='therapy'
    elif tag in ['procedure', 'procedure_1', 'procedure_2', 'procedure_3']:
        tag = 'procedure'
    elif tag in ['N_A', 'N_A_1', 'N_A_2', 'N_A_3']:
        tag = 'N_A'
    elif tag in [ 'N_B', 'N_B_1', 'N_B_2', 'N_B_3']:
        tag = 'N_B'
    

    return tag



'''
Finds the phrases indices in a given sentence (sentence needs to contain the phrases)
'''

HYPHENS = {
    '-',  # \u002d Hyphen-minus
    '‐',  # \u2010 Hyphen
    # ' ',  # \u2011 Non-breaking hyphen
    '⁃',  # \u2043 Hyphen bullet
    '‒',  # \u2012 figure dash
    '–',  # \u2013 en dash
    '—',  # \u2014 em dash
    '―',  # \u2015 horizontal bar
}

#: Minus characters.
MINUSES = {
    '-',  # \u002d Hyphen-minus
    '−',  # \u2212 Minus
    '－',  # \uff0d Full-width Hyphen-minus
    '⁻',  # \u207b Superscript minus
}

#: Plus characters.
PLUSES = {
    '+',  # \u002b Plus
    '＋',  # \uff0b Full-width Plus
    '⁺',  # \u207a Superscript plus
}

#: Slash characters.
SLASHES = {
    '/',  # \u002f Solidus
    '⁄',  # \u2044 Fraction slash
    '∕',  # \u2215 Division slash
}

#: Tilde characters.
TILDES = {
    '~',  # \u007e Tilde
    '˜',  # \u02dc Small tilde
    '⁓',  # \u2053 Swung dash
    '∼',  # \u223c Tilde operator
    '∽',  # \u223d Reversed tilde
    '∿',  # \u223f Sine wave
    '〜',  # \u301c Wave dash
    '～',  # \uff5e Full-width tilde
}

#: Apostrophe characters.
APOSTROPHES = {
    "'",  # \u0027
    '’',  # \u2019
    '՚',  # \u055a
    'Ꞌ',  # \ua78b
    'ꞌ',  # \ua78c
    '＇',  # \uff07
}

#: Single quote characters.
SINGLE_QUOTES = {
    "'",  # \u0027
    '‘',  # \u2018
    '’',  # \u2019
    '‚',  # \u201a
    '‛',  # \u201b
}

ACCENTS = {
    '`',  # \u0060
    '´',  # \u00b4
}

DOUBLE_QUOTES = {
    '"',  # \u0022
    '“',  # \u201c
    '”',  # \u201d
    '„',  # \u201e
    '‟',  # \u201f
}

def normalize(text):
    for hyphen in DOUBLE_QUOTES:
        text = text.replace(hyphen, '"')
    for hyphen in PLUSES:
        text = text.replace(hyphen, '+')
    for hyphen in PLUSES:
        text = text.replace(hyphen, '+')
    for hyphen in APOSTROPHES | SINGLE_QUOTES | ACCENTS:
        text = text.replace(hyphen, '\'')
    for hyphen in PLUSES:
        text = text.replace(hyphen, '+')
    for hyphen in HYPHENS | MINUSES:
        text = text.replace(hyphen, '-')

    return text


def create_dataset_dictionary(doc, focus_labels, label_dict, use_context= True, add__only_more_one_tag =True, use_punctuation = True):
    record_dict = []

    for document in doc: 
        used_annotation = []
        
        #get pmid for the document
        pmid = document['pmid']

        # get annotations
        annotations = document['annotations']

        # get the text of the document(could be abstract, abstract + mehtod, or splitted abstract + method)
        if use_punctuation: 
            text = add_spaces(document['text'])
            split_text = text.split()

        else: 
            text = clean_string(document['text'])
            split_text = text.split()

        # get empty labels for the len of the document
        labels_list  = zerolistmaker(len(split_text))


        # get all the annotations in the document clean it and split into words
        for anno_class in annotations.keys():
            normalized_anno = normalize_tag_name(anno_class)# match the annotation into groups
            if anno_class in focus_labels:# focusing on some of the annotation groups
            
                annotation = annotations[anno_class]
                if use_punctuation: 
                    annotation = add_spaces(str(annotation))
           
                else: 
                    annotation = clean_string(str(annotation))

                # try: 
                #     annotation = clean_string(str(annotation))
                # except TypeError: 
                #     print(pmid, annotation, anno_class)
                split_anno = annotation.split()

                # check if the annotation is in context
                if use_context == True: 
                    if anno_class in document['context'].keys() and document['context'] != 'N\A':
                        if use_punctuation:
                            context = add_spaces(document["context"][anno_class]) # get the context
                        else: 
                            context = clean_string(document["context"][anno_class])

                        context_indices = find_phrase_indices(text, context) # find the index of the context in the text(abstract, method)
                        annotation_index_in_phrase = find_phrase_indices(context, annotation) # find the index of the annotation in teh context
                        if context_indices != []:

                            for annotation_index in annotation_index_in_phrase: # label only the annotation in the context
                                index = context_indices[annotation_index]
                                if split_text[index] == split_anno[0]:
                                    temp_key = 'B-'+ normalized_anno
                                else: 
                                    temp_key = 'I-'+ normalized_anno

                                labels_list[index] = label_dict[temp_key]
                                used_annotation.append(annotation)
                            else: 
                                continue
      
                    else: # if annotation not in context find all occurrence in the text (abstract, method) and label them
                        indices = find_phrase_indices(text, annotation)
                        if annotation not in used_annotation: # to avoid reusing the annotation for different tags
                            for index in indices: 
                                # if indices.index(index) == 0: 
                                if split_text[index] == split_anno[0]:
                                    temp_key = 'B-'+ normalized_anno
                                else: 
                                    temp_key = 'I-'+ normalized_anno
                                
                                
                                labels_list[index] = label_dict[temp_key]
                                used_annotation.append(annotation)
                        else: 
                            continue
                else: 
                    indices = find_phrase_indices(text, annotation)
                    if annotation not in used_annotation: # to avoid reusing the annotation for different tags
                        for index in indices: 
                            # if indices.index(index) == 0: 
                            if split_text[index] == split_anno[0]:
                                temp_key = 'B-'+ normalized_anno
                            else: 
                                temp_key = 'I-'+ normalized_anno
                            
                            
                            labels_list[index] = label_dict[temp_key]
                            used_annotation.append(annotation)
                        else: 
                            continue


        # create dictionary
        if add__only_more_one_tag ==True: 

            if len(set(labels_list)) > 1: # only use labels that have more than one tag in them. 

                temp_dict={'pmid':pmid,
                            "ner_tags": labels_list,
                            "tokens": split_text
                                   
                                
                    }
                record_dict.append(temp_dict)
            else: 
                continue
        else: 
            temp_dict={'pmid':pmid,
                        "ner_tags": labels_list,
                        "tokens": split_text
                                  
                                
                    }
            record_dict.append(temp_dict)

    return record_dict
    
    
    
    





