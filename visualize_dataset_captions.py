import os
import re
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import threading

# Global variables
directory_path = r"<your path here>"
exclude_list = [
    'a', 'an', 'and', 'the', 'of', 'in', 'on', 'is', 'it', 'to', 'for', 'by', 
    'with', 'about', 'at', 'as', 'but', 'if', 'or', 'nor', 'so', 'yet', 
    'from', 'that', 'this', 'these', 'those', 'then', 'than', 'because', 
    'since', 'through', 'during', 'before', 'after', 'above', 'below', 
    'between', 'among', 'against', 'over', 'under', 'again', 'further', 
    'more', 'most', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 
    'same', 'so', 'too', 'very', 'can', 'will', 'just', 'should', 'now'
]
num_loaders = 2
top_n = 10
output_file = "token_counts.txt"

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

    # Plot the graphs
    fig, axes = plt.subplots(2, 3, figsize=(20, 10))

    # First graph: relative frequency with respect to the top N tokens
    axes[0, 0].bar(tokens, normalized_top_n_counts)
    axes[0, 0].set_xlabel('Tokens')
    axes[0, 0].set_ylabel('Relative Frequency (Top N)')
    axes[0, 0].set_title('Top N Most Common Tokens (Normalized to Top N)')
    axes[0, 0].set_xticks(range(len(tokens)))
    axes[0, 0].set_xticklabels(tokens, rotation=45)

    # Second graph: relative frequency with respect to all tokens
    axes[0, 1].bar(tokens, normalized_all_counts)
    axes[0, 1].set_xlabel('Tokens')
    axes[0, 1].set_ylabel('Relative Frequency (All Tokens)')
    axes[0, 1].set_title('Top N Most Common Tokens (Normalized to All Tokens)')
    axes[0, 1].set_xticks(range(len(tokens)))
    axes[0, 1].set_xticklabels(tokens, rotation=45)
    
    # Third graph: pie chart of the top N tokens, normalized to all tokens
    axes[0, 2].pie(normalized_all_counts, labels=tokens, autopct='%1.1f%%', startangle=140)
    axes[0, 2].set_title('Top N Most Common Tokens (Pie Chart, Normalized to Top N)')

    # Fourth graph: word cloud of the top N tokens
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(zip(tokens, counts)))
    axes[1, 0].imshow(wordcloud, interpolation='bilinear')
    axes[1, 0].axis('off')
    axes[1, 0].set_title('Top N Most Common Tokens (Word Cloud)')

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

if __name__ == '__main__':
    main()
