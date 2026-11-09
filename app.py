import streamlit as st
import subprocess
import tempfile
import os
import csv
from text2qti.qti import QTI

st.set_page_config(page_title="Canvas QTI Converter", page_icon="📝")

st.title("Canvas QTI Quiz Converter")
st.markdown("Upload a **text2qti** formatted `.txt` file or a structured `.csv` file to generate a Canvas-ready QTI `.zip` package.")

# Tab Selection for File Type
tab1, tab2 = st.tabs(["text2qti (.txt)", "Structured CSV (.csv)"])

with tab1:
    st.subheader("Upload text2qti Format File")
    txt_file = st.file_uploader("Choose a .txt file", type=["txt"], key="txt")
    
    if txt_file is not None:
        raw_text = txt_file.read().decode("utf-8")
        
        if st.button("Convert text2qti File", type="primary"):
            with tempfile.TemporaryDirectory() as tmpdir:
                input_path = os.path.join(tmpdir, "quiz.txt")
                with open(input_path, "w", encoding="utf-8") as f:
                    f.write(raw_text)
                
                # Execute text2qti CLI directly via subprocess
                result = subprocess.run(["text2qti", input_path], capture_output=True, text=True)
                
                zip_path = os.path.join(tmpdir, "quiz.zip")
                if os.path.exists(zip_path):
                    with open(zip_path, "rb") as zf:
                        st.success("Conversion successful!")
                        st.download_button(
                            label="Download QTI Zip",
                            data=zf.read(),
                            file_name=f"{os.path.splitext(txt_file.name)[0]}.zip",
                            mime="application/zip"
                        )
                else:
                    st.error(f"Error parsing text2qti file:\n{result.stderr}")

with tab2:
    st.subheader("Upload CSV File")
    st.info("Format: Col 1 = Question, Col 2 = Correct Index (1-based), Col 3+ = Choices")
    csv_file = st.file_uploader("Choose a .csv or tab-delimited .txt file", type=["csv", "txt"], key="csv")
    
    if csv_file is not None:
        raw_content = csv_file.read().decode("utf-8").splitlines()
        delimiter = "\t" if csv_file.name.endswith(".txt") else ","
        reader = csv.reader(raw_content, delimiter=delimiter)
        
        converted_text2qti = []
        for idx, row in enumerate(reader):
            if not row or len(row) < 3:
                continue
            question = row[0]
            try:
                correct_idx = int(row[1]) - 1
            except ValueError:
                continue
            choices = row[2:]
            
            converted_text2qti.append(f"{idx+1}. {question}")
            for c_idx, choice in enumerate(choices):
                prefix = "*" if c_idx == correct_idx else ""
                letter = chr(65 + c_idx).lower()
                converted_text2qti.append(f"{prefix}{letter}) {choice}")
            converted_text2qti.append("") # Blank line between questions
            
        final_text2qti_str = "\n".join(converted_text2qti)
        
        if st.button("Convert CSV File", type="primary"):
            with tempfile.TemporaryDirectory() as tmpdir:
                input_path = os.path.join(tmpdir, "converted_csv.txt")
                with open(input_path, "w", encoding="utf-8") as f:
                    f.write(final_text2qti_str)
                
                subprocess.run(["text2qti", input_path], capture_output=True, text=True)
                zip_path = os.path.join(tmpdir, "converted_csv.zip")
                
                if os.path.exists(zip_path):
                    with open(zip_path, "rb") as zf:
                        st.success("CSV converted to QTI package successfully!")
                        st.download_button(
                            label="Download QTI Zip",
                            data=zf.read(),
                            file_name=f"{os.path.splitext(csv_file.name)[0]}.zip",
                            mime="application/zip"
                        )