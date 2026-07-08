from pathlib import Path
import html


with open("summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()


summary = html.escape(summary)

summary = summary.replace(
    "\n",
    "<br>"
)


page = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1">

<title>AI Morning Briefing</title>


<style>

body {{
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: auto;
    padding: 25px;
    background: #f5f5f5;
}}

.card {{
    background:white;
    padding:25px;
    border-radius:15px;
    box-shadow:0 3px 10px #ccc;
}}

h1 {{
    text-align:center;
}}

</style>


</head>


<body>


<div class="card">

<h1>🌅 AI Morning Briefing</h1>


<p>
Frissítve automatikusan.
</p>


<hr>


{summary}


</div>


</body>

</html>
"""


Path("index.html").write_text(
    page,
    encoding="utf-8"
)


print("index.html elkészült")
