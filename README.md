# Batch Creation Automation Tool (KW & Oculus)

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Completed-success)

## Overview

The **Batch Creation Automation Tool** is a Python-based automation solution developed to simplify the preparation of operational batch files for Amazon moderation workflows.

The tool eliminates repetitive manual tasks by validating raw CSV files, cleaning and transforming data, applying business rules, generating marketplace-specific URLs, and producing upload-ready batch files for multiple workflows.

---

## Business Problem

The original batch preparation process required analysts to manually:

- Download raw CSV datasets
- Clean product titles
- Remove duplicate records
- Extract values from nested JSON fields
- Generate marketplace-specific Amazon URLs
- Format files according to upload templates
- Save files using standardized naming conventions

These activities were repetitive, time-consuming, and prone to manual errors.

---

## Solution

This automation streamlines the complete workflow by:

- Detecting available CSV files automatically
- Supporting both **Keyword (KW)** and **Oculus** workflows
- Validating mandatory fields
- Cleaning and normalizing product titles
- Extracting values from JSON fields
- Removing duplicate ASINs
- Mapping marketplace codes to Amazon domains
- Generating upload-ready output files
- Handling common processing errors gracefully

---

## Features

- Automatic CSV file detection
- Interactive workflow selection
- Marketplace selection
- Product title normalization
- JSON field extraction
- Duplicate removal
- Mandatory field validation
- Marketplace-specific URL generation
- Standardized output generation
- Error handling for invalid files and unsupported marketplaces

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Core application |
| Pandas | Data processing |
| JSON | Parsing nested fields |
| Regex | Text cleaning |
| Unidecode | Character normalization |
| CSV | Input and output processing |

---

## Workflow

```
Raw CSV Files
        │
        ▼
Scan Input Folder
        │
        ▼
Select Workflow (KW / Oculus)
        │
        ▼
Select Marketplace
        │
        ▼
Read CSV using Pandas
        │
        ▼
Validate Mandatory Fields
        │
        ▼
Extract & Clean Data
        │
        ▼
Apply Business Rules
        │
        ▼
Generate Output CSV
```

> **Tip:** Replace the workflow section above with the workflow image from your design document after uploading it to the repository.

Example:

```markdown
![Workflow](images/workflow.png)
```

---

## Supported Workflows

### Keyword (KW)

- Cleans product titles
- Extracts image URLs
- Removes duplicate ASINs
- Generates Amazon product URLs
- Produces upload-ready KW batch files

### Oculus

- Validates mandatory fields
- Removes duplicate ASINs
- Maps marketplace URLs
- Generates Oculus upload template

---

## Business Rules

The automation follows several business validation rules:

- Mandatory fields must not be empty
- Duplicate ASINs are removed while retaining the first occurrence
- Product titles are normalized by removing unsupported characters
- JSON fields are parsed automatically
- Marketplace codes are validated
- Marketplace-specific Amazon URLs are generated
- Separate outputs are generated for KW and Oculus workflows

---

## Error Handling

The tool validates common operational issues including:

- Missing input files
- Invalid file selections
- Unsupported marketplace codes
- Character encoding differences
- Missing mandatory fields

Meaningful error messages are displayed to help users resolve issues quickly.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/nithinck-data/batch-creation-automation.git
```

Navigate into the project:

```bash
cd batch-creation-automation
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Project Structure

```
batch-creation-automation/
│
├── automation.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── Batch_Creation_Automation_Design_Document.pdf
```

---

## Running the Tool

Run the application:

```bash
python automation.py
```

The application will:

1. Scan the input directory
2. Display available CSV files
3. Allow workflow selection
4. Ask for marketplace selection
5. Process the selected files
6. Generate upload-ready output CSVs

---

## Example Output

```
Files found in input folder:

1. TR_US.csv
2. Oculus_UK.csv

Select workflow...

Processing...

✓ KW Created:
output_kw/US/final_asker_TR_US.csv

✓ Oculus Created:
output_oculus/UK/final_oculus_Oculus_UK.csv

All selected files processed successfully.
```

---

## Future Improvements

Planned enhancements include:

- Graphical User Interface (GUI)
- Configuration file support
- Logging framework
- Unit testing
- Docker support
- Batch scheduling
- Automated report generation
- Support for additional marketplaces

---

## Documentation

The complete project design, workflow, solution components, business rules, and implementation details are available in:

**Batch_Creation_Automation_Design_Document.pdf**

---

## About the Project

This project was developed to demonstrate how Python automation can simplify operational workflows by reducing manual effort, improving consistency, and producing standardized outputs for business users.

The design emphasizes modularity, maintainability, and reusable data-processing components that can be extended for additional workflows in the future.

---

## Author

**Nithin C K**

Business Analyst | Data Analytics | Process Automation

**Skills**

- Python
- SQL
- Excel
- Power BI
- Pandas
- Process Automation

---

## License

This project is licensed under the MIT License.
