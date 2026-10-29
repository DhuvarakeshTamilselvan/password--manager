import os
from flask import Flask, request, redirect, render_template_string, url_for

app = Flask(__name__)
VERSION = os.getenv("APP_VERSION", "v1").lower()
if VERSION not in {"v1", "v2", "v3"}:
    VERSION = "v1"

# Demo-only in-memory storage. Never use for real credentials.
credentials = []

BASE_STYLE = """
<style>
body { font-family: Arial, sans-serif; max-width: 760px; margin: 40px auto; padding: 0 16px; color: #222; }
input { padding: 10px; margin: 5px 4px 5px 0; max-width: 100%; }
button { padding: 9px 14px; cursor: pointer; }
.entry { border: 1px solid #ddd; border-radius: 8px; padding: 12px; margin: 10px 0; }
small { color: #666; }
</style>
"""

@app.route("/")
def home():
    if VERSION == "v1":
        body = """
        <h1>Password Manager V1</h1>
        <p>V1: Add credentials (demo only).</p>
        <form method="post" action="/add">
          <input name="website" placeholder="Website" required>
          <input name="username" placeholder="Username" required>
          <input name="password" type="password" placeholder="Password" required>
          <button type="submit">Add Credentials</button>
        </form>
        <p>Entries added: {{ count }}</p>
        """
        return render_template_string(BASE_STYLE + body, count=len(credentials))

    delete_control = VERSION == "v3"
    body = """
    <h1>Password Manager {{ version|upper }}</h1>
    <form method="post" action="/add">
      <input name="website" placeholder="Website" required>
      <input name="username" placeholder="Username" required>
      <input name="password" type="password" placeholder="Password" required>
      <button type="submit">Add Credentials</button>
    </form>
    <h2>Saved Credentials</h2>
    {% if not credentials %}<p>No credentials added yet.</p>{% endif %}
    {% for c in credentials %}
      <div class="entry">
        <strong>{{ c.website }}</strong><br>
        Username: {{ c.username }}<br>
        Password: <span>{{ "••••••••" }}</span>
        {% if can_delete %}
        <form method="post" action="{{ url_for('delete', index=loop.index0) }}">
          <button type="submit">Delete</button>
        </form>
        {% endif %}
      </div>
    {% endfor %}
    """
    return render_template_string(
        BASE_STYLE + body,
        version=VERSION,
        credentials=credentials,
        can_delete=delete_control
    )

@app.route("/add", methods=["POST"])
def add():
    credentials.append({
        "website": request.form["website"].strip(),
        "username": request.form["username"].strip(),
        "password": request.form["password"]
    })
    return redirect(url_for("home"))

@app.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    if VERSION == "v3" and 0 <= index < len(credentials):
        credentials.pop(index)
    return redirect(url_for("home"))

@app.route("/health")
def health():
    return {"status": "healthy", "version": VERSION}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

