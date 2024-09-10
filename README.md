# Superhero Comparison Tool

## Introduction
The Superhero Comparison Tool is an interactive web application built with Streamlit that allows users to compare different superheroes based on their attributes and powers. This tool provides a fun and engaging way to explore the vast world of superheroes and their capabilities.

## Features
- Interactive superhero selection from a comprehensive database
- Side-by-side comparison of two superheroes
- Detailed display of superhero attributes including power stats, biography, and appearance
- Visual representation of power stats using interactive charts
- Responsive layout for easy viewing on different devices

## Technologies Used
- Python
- Streamlit
- SQLite
- Pandas
- Altair

## Installation

### Prerequisites
- Python 3.7+
- pip

### Steps
1. Clone the repository: `git clone https://github.com/yourusername/superhero-comparison-tool.git` and `cd superhero-comparison-tool`
2. Create a virtual environment: `python -m venv venv source venv/bin/activate` (On Windows use `venv\Scripts\activate`)
3. Install the required packages: `pip install -r requirements.txt`

## Usage
1. Ensure you have a populated SQLite database named `superheroes.db` in the same directory as the script.
2. Run the Streamlit app: streamlit run superhero_comparison.py
3. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).
4. Use the sidebar to select two superheroes for comparison.
5. Click the "Compare" button to view the detailed comparison and charts.

## Data Source
The superhero data is sourced from the [Superhero API](https://superheroapi.com/). Please refer to their terms of use for any restrictions on data usage.

## Contributing
Contributions to improve the Superhero Comparison Tool are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
Hunter Hines - hunter@hineslabs.org

Project Link: [https://github.com/yourusername/superhero-comparison-tool](https://github.com/yourusername/superhero-comparison-tool)

## Acknowledgements
- [Superhero API](https://superheroapi.com/)
- [Streamlit](https://streamlit.io/)
- [Altair](https://altair-viz.github.io/)
