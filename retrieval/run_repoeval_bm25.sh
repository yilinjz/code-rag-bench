#!/bin/sh
python eval_beir_pyserini_repo.py \
  --dataset repoeval \
  --output_metadir bm25_retrieval_data/repoeval/post_ast/project-x-corpora/ \
  --index_path bm25_retrieval_data/repoeval/post_ast/bm25_indices/ \
  --top_k 10 \
  --k1 1.2 \
  --b 0.75 \
  --output_file bm25_retrieval_data/repoeval/post_ast/eval.json \
  --results_file bm25_retrieval_data/repoeval/post_ast/results.json
