from flask import Flask, render_template, request, send_file, send_from_directory, make_response
import pandas as pd
import google.generativeai as genai
from flask import make_response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io


genai.configure(api_key="AIzaSyAruQMUEX0SWQJtsMZtAJbw-aRLURyUDw8")
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)



@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    response_text = request.form.get("response_text", "No response available")

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Split long text into lines that fit the page width
    lines = response_text.splitlines()
    y = height - 40
    for line in lines:
        if y < 40:
            p.showPage()
            y = height - 40
        p.drawString(40, y, line[:100])  # Limiting line width
        y -= 15

    p.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="gemini_response.pdf",
        mimetype="application/pdf"
    )
    
    
@app.route("/gemini", methods=["GET", "POST"])
def gemini():
    result = None
    if request.method == "POST":
        file = request.files.get("file")
        prompt = request.form.get("prompt")

        if not file or not prompt:
            result = "Please upload a file and enter a prompt."
        else:
            try:
                if file.filename.endswith(".csv"):
                    df = pd.read_csv(file)
                elif file.filename.endswith((".xls", ".xlsx")):
                    df = pd.read_excel(file)
                else:
                    result = "Unsupported file type."

                file_text = df.to_string(index=False)
                full_prompt = f"Data from file:\n{file_text}\n\nPrompt: {prompt}"
                response = model.generate_content(full_prompt)
                result = response.text
            except Exception as e:
                result = f"Error: {str(e)}"

    return render_template("gemini_tool.html", gemini_result=result)

# Serve static HTML (admin page)
@app.route("/")
def admin_page():
    return send_from_directory(".", "club_admin_home.html")

if __name__ == "__main__":
    app.run(debug=True)
