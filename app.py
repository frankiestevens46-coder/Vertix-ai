from flask import Flask, render_template_string, request, jsonify
import requests
import subprocess
import urllib.parse
import random

app = Flask(__name__)

# --- STABLE AI ENGINE (New High-Speed Endpoint) ---
def get_ai_reply(prompt):
    url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
    params = {
        "model": "openai",
        "system": "You are Vertix AI, a pro coder. Be brief, chill, and use code blocks for code.",
        "seed": random.randint(1, 1000000)
    }
    try:
        r = requests.get(url, params=params, timeout=20) # High timeout for coding
        if r.status_code == 200 and r.text.strip():
            return r.text.strip()
    except:
        pass
    return "Connection blip. Please try sending that again! ⚡"

# --- NEON BLUE CHAT UI ---
CHAT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Vertix AI</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #0a0b0d; color: #e0e0e0; font-family: sans-serif; height: 100dvh; display: flex; flex-direction: column; overflow: hidden; }
        header { padding: 15px; background: #111418; text-align: center; border-bottom: 2px solid #007bff; color: #007bff; font-weight: bold; box-shadow: 0 0 15px rgba(0,123,255,0.2); }
        #chat { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 12px; }
        .msg { max-width: 85%; padding: 12px 16px; border-radius: 18px; font-size: 16px; line-height: 1.4; word-wrap: break-word; }
        .user { align-self: flex-end; background: #007bff; color: white; border-bottom-right-radius: 2px; }
        .bot { align-self: flex-start; background: #1c1f24; border-bottom-left-radius: 2px; border-left: 3px solid #007bff; white-space: pre-wrap; font-size: 14px; }
        footer { padding: 10px 10px calc(25px + env(safe-area-inset-bottom)); background: #111418; display: flex; gap: 10px; border-top: 1px solid #333; }
        input { flex: 1; background: #1c1f24; border: 1px solid #333; color: white; padding: 12px; border-radius: 25px; outline: none; font-size: 16px; }
        button { background: #007bff; border: none; color: white; padding: 0 20px; border-radius: 25px; font-weight: bold; }
    </style>
</head>
<body>
    <header>VERTIX AI</header>
    <div id="chat"><div class="msg bot">Connected & Stable. ⚡ Ready to code.</div></div>
    <footer>
        <input type="text" id="inp" placeholder="Type here..." autocomplete="off">
        <button onclick="send()">SEND</button>
    </footer>
    <script>
        const chat = document.getElementById('chat');
        const inp = document.getElementById('inp');
        inp.addEventListener("keypress", (e) => { if(e.key === "Enter") send(); });
        async function send() {
            const val = inp.value.trim();
            if(!val) return;
            const u = document.createElement('div'); u.className='msg user'; u.innerText=val;
            chat.appendChild(u); inp.value=""; chat.scrollTop = chat.scrollHeight;
            const bId = 'b'+Date.now();
            const b = document.createElement('div'); b.className='msg bot'; b.id=bId; b.innerText="...";
            chat.appendChild(b); chat.scrollTop = chat.scrollHeight;
            try {
                const res = await fetch(`/get?msg=${encodeURIComponent(val)}`);
                const data = await res.json();
                document.getElementById(bId).innerText = data.reply;
            } catch (e) { document.getElementById(bId).innerText = "Error. Try again."; }
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
"""

# --- HACKER GREEN ADMIN UI ---
ADMIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Vertix OS | Admin</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #000; color: #0f0; font-family: monospace; padding: 15px; }
        #o { background: #050505; border: 1px solid #0f0; padding: 10px; height: 350px; overflow: auto; white-space: pre; font-size: 12px; margin-bottom: 10px; }
        input { background: #111; border: 1px solid #0f0; color: #0f0; width: 100%; padding: 12px; margin: 5px 0; outline: none; }
        button { background: #0f0; color: #000; border: none; width: 100%; padding: 12px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <h3 style="color:red">TERMINAL OVERRIDE</h3>
    <div id="o">Ready for commands... (Swipe for wide PM2 tables)</div>
    <input type="password" id="k" placeholder="Admin Key">
    <input type="text" id="c" placeholder="pm2 list, ls, etc.">
    <button onclick="run()">EXECUTE</button>
    <script>
        async function run(){
            const out = document.getElementById('o');
            const cmd = document.getElementById('c').value;
            out.innerText += "\\n$ " + cmd + "\\nRunning...";
            const res = await fetch(`/run_cmd?key=${document.getElementById('k').value}&cmd=${encodeURIComponent(cmd)}`);
            const data = await res.json();
            out.innerText += "\\n" + data.output + "\\n---";
            out.scrollTop = out.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(CHAT_HTML)

@app.route('/admin')
def admin(): return render_template_string(ADMIN_HTML)

@app.route('/get')
def get_ai(): return jsonify({"reply": get_ai_reply(request.args.get('msg'))})

@app.route('/run_cmd')
def run_cmd():
    if request.args.get('key') != "Robbie07!": return jsonify({"output":"ACCESS DENIED"})
    try:
        # Standardize command and execute
        cmd = request.args.get('cmd', '').lower()
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        return jsonify({"output": out if out else "Success (No Output)"})
    except Exception as e: return jsonify({"output": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)


