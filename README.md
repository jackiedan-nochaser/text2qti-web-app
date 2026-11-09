# USTGS Canvas QTI Quiz Converter

A Streamlit web application that converts plain text (`text2qti` format) or structured CSV files into Canvas-ready QTI `.zip` packages for seamless quiz importing into Canvas LMS.

**Developed by:** Jackson J. Tan, PhD  
**Institution:** University of Santo Tomas Graduate School (USTGS)

---

## Features

- **Direct text2qti Conversion (`.txt`)**: Converts Markdown-style quiz text files directly to QTI `.zip` packages.
- **Structured CSV Conversion (`.csv` / `.txt`)**: Turn spreadsheets and tabular questions into Canvas quizzes automatically.
- **In-App Previews**: Inspect raw files and converted quiz structures before generating packages.
- **Automated Validation**: Skips invalid rows/headers and provides error diagnostics if parsing issues occur.

---

## Quick Start

### 1. Requirements

Ensure you have Python 3.9+ installed. Install required packages:

```bash
pip install -r requirements.txt
```

### 2. Run the App

From the `canvas-qti-app` directory:

```bash
streamlit run app.py
```

---

## File Formats

### 1. `text2qti` Format (`.txt`)
```text
Quiz title: Sample Quiz

1. What is 2 + 2?
a) 3
*b) 4
c) 5

2. What is the capital of the Philippines?
*a) Manila
b) Cebu
c) Davao
```
* Asterisk (`*`) denotes the correct answer.

### 2. Structured CSV Format (`.csv`)
Columns:
- **Column 1:** Question text
- **Column 2:** 1-based index of the correct answer (`1` for Choice A, `2` for Choice B, etc.)
- **Columns 3+:** Answer choices

Example:
```csv
What is 2 + 2?,2,3,4,5
What is the capital of the Philippines?,1,Manila,Cebu,Davao
```

---

## How to Import into Canvas LMS

1. Go to your Canvas course and click **Settings** (in the left-hand navigation).
2. Click **Import Course Content** on the right sidebar.
3. Under **Content Type**, select **QTI .zip file**.
4. Choose the generated `.zip` file from this app.
5. (Optional) Select or create a **Default Question Bank**.
6. Click **Import**. Canvas will process the file and populate the quiz in your **Quizzes** section.
