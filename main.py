import os
import pdfplumber
import csv
import difflib

def compare_pdfs(source_folder, target_folder, csv_file, log_file):
    # Read CSV file
    with open(csv_file, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            source_filename = row.get("Source_FileName", "")
            target_filename = row.get("Traget file name", "")

            source_path = os.path.join(source_folder, source_filename + ".pdf")
            target_path = os.path.join(target_folder, target_filename + ".pdf")

            print(f"Processing files: {source_path}, {target_path}")

            if not os.path.isfile(source_path):
                print(f"Source file does not exist: {source_path}")
            if not os.path.isfile(target_path):
                print(f"Target file does not exist: {target_path}")

            if os.path.isfile(source_path) and os.path.isfile(target_path):
                source_size = os.path.getsize(source_path)
                target_size = os.path.getsize(target_path)

                source_content = extract_content_from_pdf(source_path)
                target_content = extract_content_from_pdf(target_path)

                match_percentage = calculate_content_match_percentage(source_content, target_content)

                if source_content == target_content:
                    with open(log_file, 'a') as log:
                        log.write(f"Files {source_filename} and {target_filename} are identical.\n")
                        log.write(f"File sizes: Source {source_size} bytes, Target {target_size} bytes.\n")
                        log.write(f"Content match percentage: {match_percentage:.2f}%\n\n")
                        print(f"Files {source_filename} and {target_filename} are identical.")
                        print(f"File sizes: Source {source_size} bytes, Target {target_size} bytes.")
                        print(f"Content match percentage: {match_percentage:.2f}%")
                else:
                    differences = get_content_differences(source_content, target_content)

                    with open(log_file, 'a') as log:
                        log.write(f"Files {source_filename} and {target_filename} are different.\n")
                        log.write(f"Changes:\n")
                        log.write(differences)
                        log.write(f"File sizes: Source {source_size} bytes, Target {target_size} bytes.\n")
                        log.write(f"Content match percentage: {match_percentage:.2f}%\n\n")
                        print(f"Files {source_filename} and {target_filename} are different.")
                        print(f"File sizes: Source {source_size} bytes, Target {target_size} bytes.")
                        print(f"Content match percentage: {match_percentage:.2f}%")
            else:
                with open(log_file, 'a') as log:
                    log.write(f"Files {source_filename} or {target_filename} do not exist.\n\n")
                    print(f"Files {source_filename} or {target_filename} do not exist.")

def extract_content_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
            # You can include other content extraction logic here (e.g., images, values)

        return text

def get_content_differences(source_content, target_content):
    d = difflib.Differ()
    diff = list(d.compare(source_content.splitlines(), target_content.splitlines()))
    return '\n'.join(diff)

def calculate_content_match_percentage(source_content, target_content):
    match_percentage = difflib.SequenceMatcher(None, source_content, target_content).ratio() * 100
    return match_percentage

if __name__ == "__main__":
    source_folder = "source/"
    target_folder = "target/"
    csv_file = "file_list.csv"
    log_file = "comparison_log.txt"

    # Clear log file before running the comparison
    open(log_file, 'w').close()

    compare_pdfs(source_folder, target_folder, csv_file, log_file)
