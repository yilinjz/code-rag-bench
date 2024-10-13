#!/bin/sh
python eval_beir_pyserini_repo.py \
  --dataset repoeval \
  --output_metadir repo_retrieval/repoeval/post_ast/project-x-corpora/ \
  --index_path repo_retrieval/repoeval/post_ast/bm25_indices/ \
  --top_k 10 \
  --k1 1.2 \
  --b 0.75 \
  --output_file repo_retrieval/repoeval/post_ast/eval.json \
  --results_file repo_retrieval/repoeval/post_ast/results.json
