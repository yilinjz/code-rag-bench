#!/bin/sh
python eval_beir_sbert_canonical.py \
    --model BAAI/bge-base-en-v1.5 \
    --dataset repoeval \
    --output_file dense_retrieval_data/repoeval/post_ast/outputs.json \
    --results_file dense_retrieval_data/repoeval/post_ast/results.json