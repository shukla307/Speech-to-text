
#C:\Users\shiva\Desktop\Flask\venv\Lib\site-packages\ffmpeg

import os
import subprocess
import uuid
from flask import Flask, request, jsonify, render_template
import speech_recognition as sr
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Specify the full path to your FFmpeg executable
FFMPEG_PATH = r"C:\Users\shiva\Desktop\Flask\venv\Lib\site-packages\ffmpeg"  # Update this path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['audio']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file:
        filename = str(uuid.uuid4())
        original_file_path = os.path.join('uploads', filename + ".webm")
        wav_file_path = os.path.join('uploads', filename + ".wav")
        file.save(original_file_path)

        # Convert webm to wav using ffmpeg subprocess
        try:
            logging.info(f"Converting {original_file_path} to {wav_file_path}")
            result = subprocess.run([FFMPEG_PATH, '-i', original_file_path, wav_file_path], 
                                    capture_output=True, text=True, check=True)
            logging.info("Conversion completed successfully")
            logging.debug(f"FFmpeg output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            logging.error(f"FFmpeg error: {e.stderr}")
            return jsonify({"error": f"Error converting audio: {e.stderr}"}), 500
        except Exception as e:
            logging.error(f"Unexpected error during conversion: {str(e)}")
            return jsonify({"error": f"Unexpected error during conversion: {str(e)}"}), 500

        recognizer = sr.Recognizer()

        try:
            logging.info(f"Opening audio file: {wav_file_path}")
            with sr.AudioFile(wav_file_path) as source:
                logging.info("Recording audio from file")
                audio = recognizer.record(source)
            
            logging.info("Recognizing speech")
            text = recognizer.recognize_google(audio)
            logging.info(f"Speech recognized: {text}")
            return jsonify({"transcription": text})

        except sr.UnknownValueError:
            logging.error("Speech recognition could not understand the audio")
            return jsonify({"error": "Speech recognition could not understand the audio"}), 400
        except sr.RequestError as e:
            logging.error(f"Could not request results from speech recognition service: {str(e)}")
            return jsonify({"error": f"Could not request results from speech recognition service; {e}"}), 500
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
        finally:
            if os.path.exists(original_file_path):
                os.remove(original_file_path)
            if os.path.exists(wav_file_path):
                os.remove(wav_file_path)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)









# from flask import Flask, request, jsonify, render_template
# import speech_recognition as sr
# import os
# import uuid
# import subprocess
# import logging

# app = Flask(__name__)

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/transcribe', methods=['POST'])
# def transcribe_audio():
#     if 'audio' not in request.files:
#         return jsonify({"error": "No file provided"}), 400

#     file = request.files['audio']
#     if file.filename == '':
#         return jsonify({"error": "No file selected"}), 400

#     if file:
#         filename = str(uuid.uuid4())
#         original_file_path = os.path.join('uploads', filename + ".webm")
#         wav_file_path = os.path.join('uploads', filename + ".wav")
#         file.save(original_file_path)

#         # Convert webm to wav using ffmpeg subprocess
#         try:
#             logging.info(f"Converting {original_file_path} to {wav_file_path}")
#             result = subprocess.run(['ffmpeg', '-i', original_file_path, wav_file_path], 
#                                     capture_output=True, text=True, check=True)
#             logging.info("Conversion completed successfully")
#             logging.debug(f"FFmpeg output: {result.stdout}")
#         except subprocess.CalledProcessError as e:
#             logging.error(f"FFmpeg error: {e.stderr}")
#             return jsonify({"error": f"Error converting audio: {e.stderr}"}), 500
#         except Exception as e:
#             logging.error(f"Unexpected error during conversion: {str(e)}")
#             return jsonify({"error": f"Unexpected error during conversion: {str(e)}"}), 500

#         recognizer = sr.Recognizer()

#         try:
#             logging.info(f"Opening audio file: {wav_file_path}")
#             with sr.AudioFile(wav_file_path) as source:
#                 logging.info("Recording audio from file")
#                 audio = recognizer.record(source)
            
#             logging.info("Recognizing speech")
#             text = recognizer.recognize_google(audio)
#             logging.info(f"Speech recognized: {text}")
#             return jsonify({"transcription": text})

#         except sr.UnknownValueError:
#             logging.error("Speech recognition could not understand the audio")
#             return jsonify({"error": "Speech recognition could not understand the audio"}), 400
#         except sr.RequestError as e:
#             logging.error(f"Could not request results from speech recognition service: {str(e)}")
#             return jsonify({"error": f"Could not request results from speech recognition service; {e}"}), 500
#         except Exception as e:
#             logging.error(f"An unexpected error occurred: {str(e)}")
#             return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
#         finally:
#             if os.path.exists(original_file_path):
#                 os.remove(original_file_path)
#             if os.path.exists(wav_file_path):
#                 os.remove(wav_file_path)

# if __name__ == '__main__':
#     os.makedirs('uploads', exist_ok=True)
#     app.run(debug=True)

#del above



# from flask import Flask, request, jsonify, render_template
# import speech_recognition as sr
# import os
# import uuid
# import ffmpeg
# import logging

# app = Flask(__name__)

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/transcribe', methods=['POST'])
# def transcribe_audio():
#     if 'audio' not in request.files:
#         return jsonify({"error": "No file provided"}), 400

#     file = request.files['audio']
#     if file.filename == '':
#         return jsonify({"error": "No file selected"}), 400

#     if file:
#         filename = str(uuid.uuid4())
#         original_file_path = os.path.join('uploads', filename + ".webm")
#         wav_file_path = os.path.join('uploads', filename + ".wav")
#         file.save(original_file_path)

#         # Convert webm to wav using ffmpeg
#         try:
#             logging.info(f"Converting {original_file_path} to {wav_file_path}")
#             stream = ffmpeg.input(original_file_path)
#             stream = ffmpeg.output(stream, wav_file_path)
#             ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
#             logging.info("Conversion completed successfully")
#         except ffmpeg.Error as e:
#             logging.error(f"FFmpeg error: {e.stderr.decode()}")
#             return jsonify({"error": f"Error converting audio: {e.stderr.decode()}"}), 500
#         except Exception as e:
#             logging.error(f"Unexpected error during conversion: {str(e)}")
#             return jsonify({"error": f"Unexpected error during conversion: {str(e)}"}), 500

#         recognizer = sr.Recognizer()

#         try:
#             logging.info(f"Opening audio file: {wav_file_path}")
#             with sr.AudioFile(wav_file_path) as source:
#                 logging.info("Recording audio from file")
#                 audio = recognizer.record(source)
            
#             logging.info("Recognizing speech")
#             text = recognizer.recognize_google(audio)
#             logging.info(f"Speech recognized: {text}")
#             return jsonify({"transcription": text})

#         except sr.UnknownValueError:
#             logging.error("Speech recognition could not understand the audio")
#             return jsonify({"error": "Speech recognition could not understand the audio"}), 400
#         except sr.RequestError as e:
#             logging.error(f"Could not request results from speech recognition service: {str(e)}")
#             return jsonify({"error": f"Could not request results from speech recognition service; {e}"}), 500
#         except Exception as e:
#             logging.error(f"An unexpected error occurred: {str(e)}")
#             return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
#         finally:
#             if os.path.exists(original_file_path):
#                 os.remove(original_file_path)
#             if os.path.exists(wav_file_path):
#                 os.remove(wav_file_path)

# if __name__ == '__main__':
#     os.makedirs('uploads', exist_ok=True)
#     app.run(debug=True)









# # from flask import Flask, request, jsonify, render_template
# # import speech_recognition as sr
# # import os
# # import uuid

# # app = Flask(__name__)

# # @app.route('/')
# # def index():
# #     return render_template('index.html')

# # @app.route('/transcribe', methods=['POST'])
# # def transcribe_audio():
# #     if 'audio' not in request.files:
# #         return jsonify({"error": "No file provided"}), 400

# #     file = request.files['audio']
# #     if file.filename == '':
# #         return jsonify({"error": "No file selected"}), 400

# #     if file:
# #         filename = str(uuid.uuid4()) + ".wav"
# #         file_path = os.path.join('uploads', filename)
# #         file.save(file_path)

# #         recognizer = sr.Recognizer()

# #         try:
# #             with sr.AudioFile(file_path) as source:
# #                 audio = recognizer.record(source)
            
# #             text = recognizer.recognize_google(audio)
# #             os.remove(file_path)  # Clean up the file after processing
# #             return jsonify({"transcription": text})

# #         except sr.UnknownValueError:
# #             return jsonify({"error": "Speech recognition could not understand the audio"}), 400
# #         except sr.RequestError as e:
# #             return jsonify({"error": f"Could not request results from speech recognition service; {e}"}), 500
# #         finally:
# #             if os.path.exists(file_path):
# #                 os.remove(file_path)  # Ensure file is cleaned up even if an error occurs

# # if __name__ == '__main__':
# #     os.makedirs('uploads', exist_ok=True)  # Create uploads directory if it doesn't exist
# #     app.run(debug=True)

