import os
import shutil
import uuid
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
from werkzeug.utils import secure_filename
import subprocess
import sys # For sys.executable
import logging

# --- Configuration ---
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER_NAME = "uploads"
SEPARATED_BASE_FOLDER_NAME = "separated"
MODEL_NAME = "htdemucs" # The Demucs model (htdemucs is a good default)

UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLDER_NAME)
DEMUCS_OUTPUT_ROOT = os.path.join(APP_ROOT, SEPARATED_BASE_FOLDER_NAME)
# This is the specific folder for the chosen model's outputs
SEPARATED_MODEL_OUTPUT_FOLDER = os.path.join(DEMUCS_OUTPUT_ROOT, MODEL_NAME)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "a_super_secret_key_for_flashing_messages" # IMPORTANT: Change this for production!
# Optional: Limit upload size, e.g., 100MB
# app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s [%(pathname)s:%(lineno)d]')
# Flask's built-in logger can also be used:
# logger = app.logger

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DEMUCS_OUTPUT_ROOT, exist_ok=True)
# Demucs will create the model-specific subfolder (e.g., htdemucs)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("Oops! No file part in the request. Please select a file.", "error")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("Please select a file to upload. 🎶", "error")
            return redirect(request.url)

        if file:
            original_filename = secure_filename(file.filename)
            unique_id = uuid.uuid4().hex
            filename_base, file_ext = os.path.splitext(original_filename)
            
            if not file_ext.lower() in ['.mp3', '.wav', '.flac', '.ogg', '.m4a']:
                flash("Unsupported file type. Please upload an MP3, WAV, FLAC, OGG, or M4A file. 🎧", "error")
                return redirect(request.url)

            new_filename_with_ext = f"{unique_id}_{filename_base}{file_ext}"
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], new_filename_with_ext)
            
            track_folder_name_for_demucs = f"{unique_id}_{filename_base}"

            try:
                file.save(filepath)
                app.logger.info(f"File saved to: {filepath}")
            except Exception as e:
                app.logger.error(f"Error saving file: {e}")
                flash(f"Could not save uploaded file: {e}", "error")
                return redirect(request.url)

            flash(f"Processing '{original_filename}'... This might take a few minutes! ⏳", "info")
            # The flash message might not display before the redirect if demucs is very fast or very slow.
            # A true loading indicator would need JavaScript.

            demucs_cmd = [
                sys.executable, "-m", "demucs",
                "-n", MODEL_NAME,
                "-o", DEMUCS_OUTPUT_ROOT,
                "--two-stems", "vocals", # Output vocals.wav and no_vocals.wav
                filepath
            ]
            
            app.logger.info(f"Running Demucs command: {' '.join(demucs_cmd)}")

            try:
                # Increased timeout as Demucs can be slow
                process = subprocess.run(demucs_cmd, check=True, capture_output=True, text=True, timeout=1200) # 20 minutes
                app.logger.info(f"Demucs stdout: {process.stdout}")
                if process.stderr: # Demucs often outputs info to stderr
                    app.logger.info(f"Demucs stderr (info/warnings): {process.stderr}")
            except subprocess.CalledProcessError as e:
                app.logger.error(f"Demucs failed with exit code {e.returncode}")
                app.logger.error(f"Demucs stdout: {e.stdout}")
                app.logger.error(f"Demucs stderr: {e.stderr}")
                if os.path.exists(filepath): os.remove(filepath)
                flash(f"Demucs processing failed. Uh oh! 😥 Check server logs. Error: {e.stderr[:250]}...", "error")
                return redirect(request.url)
            except subprocess.TimeoutExpired:
                app.logger.error("Demucs process timed out.")
                if os.path.exists(filepath): os.remove(filepath)
                flash("Demucs processing took too long and was stopped. Maybe try a shorter song? 🐢", "error")
                return redirect(request.url)
            except Exception as e:
                app.logger.error(f"An unexpected error occurred during Demucs processing: {e}")
                if os.path.exists(filepath): os.remove(filepath)
                flash("An unexpected error occurred. Please check the server logs. 💥", "error")
                return redirect(request.url)

            expected_separated_track_path = os.path.join(SEPARATED_MODEL_OUTPUT_FOLDER, track_folder_name_for_demucs)
            app.logger.info(f"Expecting Demucs output in: {expected_separated_track_path}")

            if not os.path.exists(expected_separated_track_path):
                app.logger.error(f"Separation output folder NOT FOUND: {expected_separated_track_path}")
                if os.path.exists(SEPARATED_MODEL_OUTPUT_FOLDER):
                    app.logger.info(f"Contents of {SEPARATED_MODEL_OUTPUT_FOLDER}: {os.listdir(SEPARATED_MODEL_OUTPUT_FOLDER)}")
                if os.path.exists(filepath): os.remove(filepath)
                flash("Separation seemed to finish, but the output folder is missing. Spooky! 👻 Check logs.", "error")
                return redirect(request.url)

            # Stems expected with --two-stems vocals
            stems_to_check = ["vocals.wav", "no_vocals.wav"]
            found_stems = []
            for stem_file in stems_to_check:
                full_stem_path = os.path.join(expected_separated_track_path, stem_file)
                if os.path.exists(full_stem_path) and os.path.getsize(full_stem_path) > 0: # Check if file is not empty
                    found_stems.append(stem_file)
                else:
                    app.logger.warning(f"Expected stem file NOT found or is empty: {full_stem_path}")
            
            if not found_stems:
                app.logger.error(f"Output folder {expected_separated_track_path} exists, but NO valid stem files (vocals.wav, no_vocals.wav) found.")
                app.logger.info(f"Actual contents of {expected_separated_track_path}: {os.listdir(expected_separated_track_path)}")
                if os.path.exists(filepath): os.remove(filepath)
                flash("Output folder created, but no usable stem files were found. Something went wrong during separation. 😕", "error")
                return redirect(request.url)
            
            # Optional: Clean up original uploaded file after successful processing
            # if os.path.exists(filepath):
            #    try:
            #        os.remove(filepath)
            #        app.logger.info(f"Cleaned up uploaded file: {filepath}")
            #    except Exception as e:
            #        app.logger.error(f"Error cleaning up uploaded file {filepath}: {e}")


            flash("Woohoo! Separation complete! 🎉", "success")
            return render_template("index.html", 
                                   track_id=track_folder_name_for_demucs, 
                                   available_stems=found_stems,
                                   original_display_name=original_filename,
                                   model_name=MODEL_NAME)

    return render_template("index.html", model_name=MODEL_NAME)

@app.route("/separated/<track_id>/<stem_filename>")
def download_file(track_id, stem_filename):
    directory_for_stems = os.path.join(SEPARATED_MODEL_OUTPUT_FOLDER, track_id)
    file_to_send_path = os.path.join(directory_for_stems, stem_filename)
    
    app.logger.info(f"Download request for track '{track_id}', stem '{stem_filename}'")
    app.logger.info(f"Serving from directory: '{directory_for_stems}', file: '{stem_filename}'")
    app.logger.info(f"Full path: '{file_to_send_path}'")

    if os.path.exists(file_to_send_path):
        return send_from_directory(directory_for_stems, stem_filename, as_attachment=True)
    else:
        app.logger.error(f"File not found for download: '{file_to_send_path}'")
        flash("Sorry, that file couldn't be found. It might have expired or there was an issue. 🤷", "error")
        # Redirect to home or show a custom 404 page
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)