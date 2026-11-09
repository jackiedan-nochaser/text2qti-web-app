import streamlit as st
import subprocess
import tempfile
import os
import csv

st.set_page_config(page_title="USTGS Canvas QTI Converter", page_icon="📝")

st.title("USTGS Canvas QTI Quiz Converter")
st.caption("By Jackson J. Tan, PhD")
st.markdown("Upload a **text2qti** formatted `.txt` file or a structured `.csv` file to generate a Canvas-ready QTI `.zip` package.")

# Tab Selection for File Type
tab1, tab2 = st.tabs(["text2qti (.txt)", "Structured CSV (.csv)"])

with tab1:
    st.subheader("Upload text2qti Format File")
    
    with st.expander("ℹ️ View text2qti Format Example", expanded=False):
        st.markdown("Text files must follow standard `text2qti` format:")
        st.code(
            "Quiz title: Sample Quiz\n\n"
            "1. What is 2 + 2?\n"
            "a) 3\n"
            "*b) 4\n"
            "c) 5",
            language="text"
        )
        
    txt_file = st.file_uploader("Choose a .txt file", type=["txt"], key="txt")
    
    if txt_file is not None:
        raw_text = txt_file.read().decode("utf-8")
        
        with st.expander("📄 Preview Uploaded Content", expanded=False):
            st.code(raw_text, language="text")
            
        if st.button("Convert text2qti File", type="primary"):
            with tempfile.TemporaryDirectory() as tmpdir:
                input_path = os.path.join(tmpdir, "quiz.txt")
                with open(input_path, "w", encoding="utf-8") as f:
                    f.write(raw_text)
                
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
    
    with st.expander("ℹ️ View CSV Format Guidelines", expanded=False):
        st.markdown("""
- **Column 1:** Question text
- **Column 2:** 1-based index of correct answer (`1` for Choice A, `2` for Choice B, etc.)
- **Columns 3+:** Answer choices
""")
        st.code(
            "What is 2 + 2?,2,3,4,5\n"
            "What is the capital of France?,1,Paris,Rome,Berlin",
            language="csv"
        )
        st.caption("*(Header rows are automatically skipped if Column 2 is not a number)*")

    csv_file = st.file_uploader("Choose a .csv or tab-delimited .txt file", type=["csv", "txt"], key="csv")
    
    if csv_file is not None:
        raw_content = csv_file.read().decode("utf-8").splitlines()
        delimiter = "\t" if csv_file.name.endswith(".txt") else ","
        reader = csv.reader(raw_content, delimiter=delimiter)
        
        quiz_title = os.path.splitext(csv_file.name)[0].replace("_", " ").title()
        converted_text2qti = [f"Quiz title: {quiz_title}\n"]
        
        q_num = 1
        for row in reader:
            if not row or len(row) < 3:
                continue
            question = row[0].strip()
            try:
                correct_idx = int(row[1].strip()) - 1
            except ValueError:
                # Skips header row
                continue
            choices = [c.strip() for c in row[2:] if c.strip()]
            if not choices or correct_idx < 0 or correct_idx >= len(choices):
                continue
            
            converted_text2qti.append(f"{q_num}. {question}")
            for c_idx, choice in enumerate(choices):
                prefix = "*" if c_idx == correct_idx else ""
                letter = chr(65 + c_idx).lower()
                converted_text2qti.append(f"{prefix}{letter}) {choice}")
            converted_text2qti.append("")  # Blank line between questions
            q_num += 1
            
        final_text2qti_str = "\n".join(converted_text2qti)
        
        total_questions = q_num - 1
        if total_questions > 0:
            st.info(f"✅ Detected **{total_questions}** question(s).")
            with st.expander("📄 Preview Converted text2qti Format", expanded=False):
                st.code(final_text2qti_str, language="text")
        else:
            st.warning("No valid questions detected. Please verify your CSV columns.")
        
        if st.button("Convert CSV File", type="primary", disabled=(total_questions == 0)):
            with tempfile.TemporaryDirectory() as tmpdir:
                input_path = os.path.join(tmpdir, "converted_csv.txt")
                with open(input_path, "w", encoding="utf-8") as f:
                    f.write(final_text2qti_str)
                
                result = subprocess.run(["text2qti", input_path], capture_output=True, text=True)
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
                else:
                    st.error(f"Error converting CSV to QTI:\n{result.stderr}")