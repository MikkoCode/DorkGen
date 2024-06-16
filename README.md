
# DorkGen

DorkGen is a GUI application for generating and searching Google dorks from a given website's HTML source. It uses the Zyte API to fetch the HTML content and then processes it to generate dorks. The application is built using Python's Tkinter library for the GUI and supports dark mode.

## Features

- Generate Google dorks from a website's HTML source.
- Filter generated dorks based on user-defined criteria.
- Search Google using the generated dorks.
- Save dorks and search results to text files.
- Remove duplicate and invalid dorks.
- Remove selected dorks and search results.

## Installation

### Prerequisites

- Python 3.x
- Required Python libraries:
  - `tkinter`
  - `requests`
  - `beautifulsoup4`
  - `lxml`

### Install the required libraries

```bash
pip install requests beautifulsoup4 lxml
```

### Clone the repository

```bash
git clone https://github.com/MikkoCode/DorkGen.git
cd DorkGen
```

## Usage

1. **Run the application:**

    ```bash
    python main.py
    ```

2. **Generate Dorks:**
    - Enter the website URL in the "Enter Site URL" field.
    - Click "Generate Dorks" to fetch the HTML source and generate dorks.

3. **Filter Dorks:**
    - Enter the filter criteria in the "Filter Dorks" field.
    - Click "Apply Filter" to filter the generated dorks.
    - Click "Remove Filter" to remove the applied filter and show all dorks.
    - Click "Remove Duplicates" in the "Dorks" section to remove duplicate dorks.
    - Click "Cleanup" to remove invalid dorks.
   
4. **Search Dorks:**
    - Click "Run Search" to start searching Google with the generated dorks.
    - Click "Pause" to pause the search.
    - Click "Continue Search" to resume the paused search.

5. **Save Dorks and Results:**
    - Click "Save to File" in the "Dorks" section to save the generated dorks.
    - Click "Save to File" in the "Search Results" section to save the search results.

6. **Remove Duplicates and Clean Up:**
    - Click "Remove Duplicates" in the "Search Results" section to remove duplicate results.

7. **API Key Management:**
    - Enter your Zyte API key in the "Zyte API Key" field.
    - Click "Save API Key" to save the API key for future use.

## Files

- app.py: Main application file containing the application logic.
- ui_setup.py: Module for setting up the GUI components.
- dork_generation.py: Module for generating dorks from the HTML source.
- main.py: Entry point of the application
- zyte_api_key.txt: Zyte API key is stored here 