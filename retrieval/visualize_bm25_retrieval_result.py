import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LinearRegression


# path to retrieval results
results_file_path = "bm25_retrieval_data/repoeval/results.json"

# Load the JSON data
def load_json_data(path):
    '''
    Load json data from file path {path}
    '''
    data = []
    with open(path, 'r') as f:
        for line in f:
            json_object = json.loads(line.strip())
            data.append(json_object)
    return data

# Compute TF-IDF Cosine Similarity
def compute_tfidf_similarity(prompt, docs):
    texts = [prompt] + [doc['text'] for doc in docs]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)

    # Compute cosine similarity between prompt and each doc
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    return similarities

# Prepare dataset for visualization
def prepare_dataset(data):
    all_similarities = []
    all_labels = []
    indices = []  # To keep track of the JSON object index

    for idx, item in enumerate(data):
        prompt = item['prompt']
        reference = item['reference']
        docs = item['docs']

        # Compute similarities
        similarities = compute_tfidf_similarity(prompt, docs)

        # Create binary labels (1 if reference in doc, else 0)
        labels = [1 if reference in doc['text'] else 0 for doc in docs]

        all_similarities.extend(similarities)
        all_labels.extend(labels)

        # Store the index for each similarity score
        indices.extend([idx] * len(similarities))

    return np.array(all_similarities), np.array(all_labels), np.array(indices)

# Visualization 1: Scatter Plot of TF-IDF Similarity vs. Relevance
def visualize_similarity_vs_relevance(similarities, labels):
    plt.figure(figsize=(8, 6))
    plt.scatter(similarities, labels, alpha=0.5)
    plt.xlabel("TF-IDF Cosine Similarity")
    plt.ylabel("Relevance (1 = Relevant, 0 = Not Relevant)")
    plt.title("TF-IDF Similarity vs. Relevance")
    plt.show()

# Visualization 2: Line Plot with Linear Fit for TF-IDF Similarity vs. Index
def visualize_similarity_vs_index(indices, similarities):
    # Reshape data for linear regression
    indices_reshaped = indices.reshape(-1, 1)
    
    # Fit a linear regression model
    model = LinearRegression()
    model.fit(indices_reshaped, similarities)

    # Predict values for the linear fit line
    predicted_similarities = model.predict(indices_reshaped)

    # Plot the original data and the linear fit line
    plt.figure(figsize=(8, 6))
    plt.scatter(indices, similarities, alpha=0.5, label="TF-IDF Similarity", color="blue")
    plt.plot(indices, predicted_similarities, color="red", label="Linear Fit")
    plt.xlabel("JSON Object Index")
    plt.ylabel("TF-IDF Cosine Similarity")
    plt.title("TF-IDF Similarity vs. JSON Object Index")
    plt.legend()
    plt.show()

# Main
if __name__ == "__main__":
    results_data = load_json_data(results_file_path)
    similarities, labels, indices = prepare_dataset(results_data)

    # Plot 1: TF-IDF Similarity vs. Relevance
    visualize_similarity_vs_relevance(similarities, labels)
    # Plot 2: TF-IDF Similarity vs. JSON Object Index with Linear Fit
    visualize_similarity_vs_index(indices, similarities)
