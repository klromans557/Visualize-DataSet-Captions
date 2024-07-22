import os
import re
from collections import Counter
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import networkx as nx

# Global variables - USER DEFINED ===================================================================

directory_path = r"<your dataset path here>" # e.g.: = r"C:\Users\YOU\Desktop\dataset_folder_name"
exclude_list = [
    'a', 'an', 'and', 'the', 'of', 'in', 'on', 'is', 'it', 'to', 'for', 'by', 
    'with', 'about', 'at', 'as', 'but', 'if', 'or', 'nor', 'so', 'yet', 
    'from', 'that', 'this', 'these', 'those', 'then', 'than', 'because', 
    'since', 'through', 'during', 'before', 'after', 'above', 'below', 
    'between', 'among', 'against', 'over', 'under', 'again', 'further', 
    'more', 'most', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 
    'same', 'so', 'too', 'very', 'can', 'will', 'just', 'should', 'now'
] # These are common words I wanted to ignore. Feel free to change this list, or to leave it empty simply use: = []
num_loaders = 2 # Number of cpu threads/cores to use in parallel processing
top_n = 10 # Top N most common tokens from full dataset 
network_index = 1  # Select which of the top N tokens to emphasize in Network Graph, i.e. most common: = 1, least common: = top_n
output_file = "token_counts.txt" # Holds raw token list and associated counts needed for calculations

# Global variables - USER DEFINED ===================================================================

# Function to clean and tokenize text
def tokenize(text, exclude_list):
    # Convert to lowercase
    text = text.lower()
    # Remove numbers and non-alphabetic characters and tokenize
    tokens = re.findall(r'\b[a-z]+\b', text)
    # Exclude specified tokens
    tokens = [token for token in tokens if token not in exclude_list]
    return tokens

# Function to process a single file
def process_file(file_path, exclude_list):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
        tokens = tokenize(text, exclude_list)
    return tokens

def main():
    if os.path.exists(output_file):
        print(f"{output_file} already exists. Skipping token counting and proceeding to graph generation.")
        # Load token counts from the file
        token_counts = Counter()
        with open(output_file, 'r', encoding='utf-8') as f:
            for line in f:
                token, count = line.strip().split(': ')
                token_counts[token] = int(count)
    else:
        # List to store the names of TXT files
        txt_files = []

        # Iterate through the files in the specified directory
        for file_name in os.listdir(directory_path):
            if file_name.endswith(".txt"):
                txt_files.append(file_name)

        # Dictionary to store the token counts
        token_counts = Counter()

        # Process files in parallel
        with ProcessPoolExecutor(max_workers=num_loaders) as executor:
            futures = {executor.submit(process_file, os.path.join(directory_path, txt_file), exclude_list): txt_file for txt_file in txt_files}
            
            for future in as_completed(futures):
                tokens = future.result()
                token_counts.update(tokens)

        # Write the token counts to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            for token, count in token_counts.items():
                f.write(f"{token}: {count}\n")

        print(f"Token counts written to {output_file}")

    # Visualize the distribution of the top N tokens
    most_common_tokens = token_counts.most_common(top_n)

    tokens, counts = zip(*most_common_tokens)

    # Normalize the counts with respect to the top N tokens
    total_top_n_counts = sum(counts)
    normalized_top_n_counts = [count / total_top_n_counts for count in counts]

    # Normalize the counts with respect to all tokens
    total_counts = sum(token_counts.values())
    normalized_all_counts = [count / total_counts for count in counts]

    # Plot the graphs ============================================================================================================================
    
    fig, axes = plt.subplots(2, 3, figsize=(20, 10))

    # First graph: relative frequency with respect to all tokens
    axes[0, 0].bar(tokens, normalized_all_counts)
    axes[0, 0].set_xlabel('Tokens')
    axes[0, 0].set_ylabel('Relative Frequency (All Tokens)')
    axes[0, 0].set_title('Top N Most Common Tokens (Normalized to All Tokens)')
    axes[0, 0].set_xticks(range(len(tokens)))
    axes[0, 0].set_xticklabels(tokens, rotation=45)
    
    # Second graph: pie chart of the top N tokens, normalized to Top N
    axes[0, 1].pie(normalized_top_n_counts, labels=tokens, autopct='%1.1f%%', startangle=140)
    axes[0, 1].set_title('Top N Most Common Tokens (Pie Chart, Normalized to Top N)')

    # Third graph: word cloud of the top N tokens
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(zip(tokens, counts)))
    axes[0, 2].imshow(wordcloud, interpolation='bilinear')
    axes[0, 2].axis('off')
    axes[0, 2].set_title('Top N Most Common Tokens (Word Cloud)')

    # Fourth graph: network graph of the top N tokens
    # Calculate pairwise co-occurrences of tokens
    pair_counts = defaultdict(int)
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".txt"):
            with open(os.path.join(directory_path, file_name), 'r', encoding='utf-8') as f:
                text = f.read()
                tokens_in_file = tokenize(text, exclude_list)
                unique_tokens = set(tokens_in_file)
                for token1 in unique_tokens:
                    for token2 in unique_tokens:
                        if token1 != token2:
                            pair_counts[(token1, token2)] += 1

    # Filter pair_counts to only include top N tokens
    top_n_tokens = set(tokens)
    filtered_pair_counts = {pair: weight for pair, weight in pair_counts.items() if pair[0] in top_n_tokens and pair[1] in top_n_tokens}

    # Create the graph
    G = nx.Graph()
    for (token1, token2), weight in filtered_pair_counts.items():
        G.add_edge(token1, token2, weight=weight)

    # Normalize edge weights for thickness
    max_weight = 1.2 * max(nx.get_edge_attributes(G, 'weight').values())
    min_weight = 1.2 * min(nx.get_edge_attributes(G, 'weight').values())
    edge_widths = [1 + 4 * (G[u][v]['weight'] - min_weight) / (max_weight - min_weight) for u, v in G.edges()]

    # Determine which node to emphasize based on user-specified index
    selected_node = tokens[network_index - 1] if 1 <= network_index <= len(tokens) else None

    edge_colors = []
    for u, v in G.edges():
        if selected_node and (u == selected_node or v == selected_node):
            edge_colors.append('red')
        else:
            edge_colors.append('grey')

    pos = nx.spring_layout(G, k=0.5, seed=42)
    nx.draw(G, pos, ax=axes[1, 0], with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold", edge_color=edge_colors, width=edge_widths)
    axes[1, 0].set_title('Network Graph of the Top N Tokens')

    # Fifth graph: histogram of token lengths
    token_lengths = [len(token) for token in token_counts.keys()]
    sns.histplot(token_lengths, bins=range(min(token_lengths), max(token_lengths) + 2), ax=axes[1, 1], kde=False, discrete=True)
    axes[1, 1].set_xticks(range(min(token_lengths), max(token_lengths) + 1))
    axes[1, 1].set_xlabel('Token Length')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].set_title('Distribution of Token Lengths')

    # Sixth graph: frequency distribution plot
    token_frequencies = list(token_counts.values())
    sns.histplot(token_frequencies, bins=50, log_scale=(True, True), ax=axes[1, 2])
    axes[1, 2].set_xlabel('Token Frequency')
    axes[1, 2].set_ylabel('Number of Tokens')
    axes[1, 2].set_title('Frequency Distribution of Tokens')

    plt.tight_layout()
    plt.show()
    
    # Plot the graphs ============================================================================================================================

if __name__ == '__main__':
    main()
