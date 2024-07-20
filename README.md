# Visualize-DataSet-Captions
A simple Python script I wrote to test my regularization dataset captions -- built with the help of GPT-4o -- which combs through a dataset folder and analyzes the caption TXT files therein. Information about the distribution/frequency of the words/tokens is then diplayed using bar charts, a pie chart, word cloud, length histogram, and a frequency distribution. An output TXT with listed token counts is also generated during the process. Feel free to use, share, and modify this script to suit your needs. 
<(˶ᵔᵕᵔ˶)>

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Installation

1. Please have Python 3.7, or later, installed. You can download it from [python.org](https://www.python.org/downloads/).

2. Clone the repository and go into the created folder:
    ```sh
    git clone https://github.com/klromans557/Visualize-DataSet-Captions.git
    cd Visualize-DataSet-Captions
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
    
4. The script can handle the images and captions being in the same folder, feel free to keep them together.

## Usage

To run the script and visualize the captions, follow these steps:

1. Update the variables at the top of the script:
   - Change `directory_path` to the path of your dataset folder.
     * e.g directory_path = r"C:Users\YOU\Desktop\DataSet_Folder"
   - The `exlude_list` has been populated with common words, but feel free to change these.
   - Set the `num_loaders` based on number of CPU cores/threads to use in parallel processing.
   - Set the `top_n` value to change the number of top N tokens used in graph calculations.
   - Change `output_file` text for the name of the output TXT file with token counts
     * note: this file is created in the same directory as the script when run.

3. Run the script using the included BAT file.

4. If the `token_counts.txt` file already exists, the script will skip the token counting step and proceed to the graphs.

5. The script will display the following graphs:
    - Two bar charts showing the relative frequency of the top N tokens.
        * normalized to: i. top N tokens & ii. all tokens
    - A pie chart showing the relative frequency of the top N tokens.
    - A word cloud generated from the top N tokens.
    - A histogram of token lengths.
    - A frequency distribution plot of token frequencies.

6. Press any key or close the graph window to exit the script.

## Contributing

(NOTE: I'm new to sharing through GitHub, and this is just the standard template for this section)

Contributions are welcome! If you have any suggestions, improvements, or bug fixes, please follow these steps:

1. Fork the repository.
2. Create a new branch with a descriptive name (`git checkout -b my-feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin my-feature-branch`).
5. Open a pull request.

Please ensure your code adheres to the existing style and includes appropriate tests.

### Reporting Issues

If you find a bug or have a feature request, please create an issue [here](https://github.com/klromans557/Visualize-DataSet-Captions/issues).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenAI](https://www.openai.com) for providing guidance and assistance in developing this project.
- [GitHub](https://github.com) for hosting the repository.
- [Dr. Furkan Gözükara](https://www.patreon.com/SECourses/posts) for sharing his scripts through the SECourses Patron, associated Discord server, and YouTube channel.
  These resources were invaluable to me during the development of this project and served as guides/templates for creating such scripts.
