from __future__ import print_function

import os.path
import torch
from classes.utils import read_CoNNL, write_CoNNL
from classes.evaluator import Evaluator

print('Start!')

# Load tagger model
fn_checkpoint = 'tagger_model.txt'
if os.path.isfile(fn_checkpoint):
    tagger = torch.load(fn_checkpoint)
else:
    raise ValueError('Can''t find stored tagger %s. Please, run the main script with non-empty --save_best_path param to create it.')

# We take sequences_indexer from the tagger
sequences_indexer = tagger.sequences_indexer

# GPU device number, -1 by default (CPU)
gpu = 0
if gpu >= 0:
    tagger = tagger.cuda(device=0)

# Create evaluator module to calculate macro scores
evaluator = Evaluator(sequences_indexer)

# Read data in CoNNL-2003 formar
fn = 'data/argument_mining/persuasive_essays/es_paragraph_level_test.txt'
token_sequences, tag_sequences = read_CoNNL(fn)

# Get tags as sequences of strings
output_tag_sequences = tagger.predict_tags_from_tokens(token_sequences)

# Get F1/Precision/Recall macro scores
acc, f1, precision, recall = evaluator.get_macro_scores_tokens_tags(tagger, token_sequences, tag_sequences)

print('Accuracy = %1.3f, MACRO F1 = %1.3f, Precision = %1.3f, Recall = %1.3f.\n' % (acc, f1, precision, recall))

# Write results to text file
write_CoNNL('out.txt', token_sequences, tag_sequences, output_tag_sequences)

print('The end.')