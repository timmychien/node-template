import os
import subprocess
import json

def setup_express(project_dir):
    server_dir = os.path.join(project_dir, "server")
    os.makedirs(server_dir, exist_ok=True)

    package_json_path = os.path.join(server_dir, "package.json")
    if not os.path.exists(package_json_path):
        # Create minimal package.json
        pkg = {
            "name": "{{ cookiecutter.project_name }}-server",
            "version": "1.0.0",
            "main": "index.js",
            "scripts": {
                "start": "node index.js"
            },
            "dependencies": {}
        }
        with open(package_json_path, "w") as f:
            json.dump(pkg, f, indent=2)

    # Install express
    subprocess.run(["npm", "install", "express"], cwd=server_dir)

    index_file = os.path.join(server_dir, "index.js")
    if not os.path.exists(index_file):
        with open(index_file, "w") as f:
            f.write("""\
const express = require("express");
const app = express();
const port = process.env.PORT || 3000;

app.get("/", (req, res) => {
  res.send("Hello from {{ cookiecutter.project_name }} backend!");
});

app.listen(port, () => console.log(`Server running at http://localhost:${port}`));
""")


def setup_react(project_dir):
    client_dir = os.path.join(project_dir, "client")
    os.makedirs(client_dir, exist_ok=True)

    # Init npm if not done
    if not os.path.exists(os.path.join(client_dir, "package.json")):
        subprocess.run(["npm", "init", "-y"], cwd=client_dir)

    # Install React + Vite
    subprocess.run(["npm", "install", "react", "react-dom"], cwd=client_dir)
    subprocess.run(["npm", "install", "-D", "vite", "@vitejs/plugin-react"], cwd=client_dir)

    # Update scripts
    package_json_path = os.path.join(client_dir, "package.json")
    with open(package_json_path, "r") as f:
        pkg = json.load(f)

    pkg.setdefault("scripts", {})
    pkg["scripts"].update({
        "dev": "vite",
        "build": "vite build",
        "preview": "vite preview"
    })

    with open(package_json_path, "w") as f:
        json.dump(pkg, f, indent=2)

    # Create index.html + src if missing
    src_dir = os.path.join(client_dir, "src")
    os.makedirs(src_dir, exist_ok=True)

    index_html = os.path.join(client_dir, "index.html")
    if not os.path.exists(index_html):
        with open(index_html, "w") as f:
            f.write("""\
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{ cookiecutter.project_name }} Client</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
""")

    main_jsx = os.path.join(src_dir, "main.jsx")
    if not os.path.exists(main_jsx):
        with open(main_jsx, "w") as f:
            f.write("""\
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
""")

    app_jsx = os.path.join(src_dir, "App.jsx")
    if not os.path.exists(app_jsx):
        with open(app_jsx, "w") as f:
            f.write("""\
export default function App() {
  return <h1>Hello from {{ cookiecutter.project_name }} frontend 🚀</h1>
}
""")

    vite_config = os.path.join(client_dir, "vite.config.js")
    if not os.path.exists(vite_config):
        with open(vite_config, "w") as f:
            f.write("""\
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()]
})
""")


def main():
    project_dir = os.getcwd()
    framework = "{{ cookiecutter.framework }}"  # comes from cookiecutter.json

    if framework == "react":
        setup_react(project_dir)
    elif framework == "express":
        setup_express(project_dir)
    elif framework == "fullstack":
        setup_react(project_dir)
        setup_express(project_dir)
        print("✅ Fullstack project created (client + server)")
    else:
        print("⚠️ Unknown framework option")

if __name__ == "__main__":
    main()
