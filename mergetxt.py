import os

def merge_text_files(source_folder, output_filename="input.txt"):
    # Ensure the output file is empty before starting
    if os.path.exists(output_filename):
        os.remove(output_filename)

    # Get all .txt files in the folder
    files = [f for f in os.listdir(source_folder) if f.endswith('.txt')]
    files.sort()  # Optional: sorts files alphabetically

    with open(output_filename, 'a', encoding='utf-8') as outfile:
        for filename in files:
            file_path = os.path.join(source_folder, filename)
            
            # Avoid reading the output file if it's in the same folder
            if filename == output_filename:
                continue
                
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                content = infile.read()
                outfile.write(content)
                
                # Add a newline between files to prevent words from merging
                if not content.endswith('\n'):
                    outfile.write('\n')
            
            print(f"Appended: {filename}")

    print(f"\nDone! All files merged into '{output_filename}'.")

# --- Usage ---
# Replace '.' with the path to your folder if it's not the current directory
merge_text_files(source_folder='vin.dynalias.com')