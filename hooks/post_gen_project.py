import os
import subprocess
import json

def setup_express(project_dir, back_end_port):
    server_dir = os.path.join(project_dir, "server")
    os.makedirs(server_dir, exist_ok=True)

    subprocess.run(["npm", "init", "-y"], cwd=server_dir)
    subprocess.run(["npm", "install", "express"], cwd=server_dir)

    index_file = os.path.join(server_dir, "index.js")
    if not os.path.exists(index_file):
        with open(index_file, "w") as f:
            f.write(f"""\
const express = require("express");
const app = express();
const port = process.env.PORT || {back_end_port};

app.get("/", (req, res) => {{
  res.send("Hello from {{ cookiecutter.project_name }} backend!");
}});

app.listen(port, () => console.log(`Server running at http://localhost:${{port}}`));
""")


def setup_react(project_dir, front_end_port):
    client_dir = os.path.join(project_dir, "client")
    os.makedirs(client_dir, exist_ok=True)

    subprocess.run(["npm", "init", "-y"], cwd=client_dir)
    subprocess.run(["npm", "install", "react", "react-dom"], cwd=client_dir)
    subprocess.run(["npm", "install", "-D", "vite", "@vitejs/plugin-react"], cwd=client_dir)

    vite_config = os.path.join(client_dir, "vite.config.js")
    if not os.path.exists(vite_config):
        with open(vite_config, "w") as f:
            f.write(f"""\
import {{ defineConfig }} from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({{
  plugins: [react()],
  server: {{
    port: {front_end_port},
    host: true
  }}
}})
""")



def main():
    project_dir = os.getcwd()
    framework = "{{ cookiecutter.framework }}"
    front_end_port = "{{ cookiecutter.front_end_port }}"
    back_end_port = "{{ cookiecutter.back_end_port }}"

    if framework == "react":
        print(f"⚡ Setting up React app on port {front_end_port}")
        setup_react(project_dir, front_end_port)

    elif framework == "express":
        print(f"🚀 Setting up Express app on port {back_end_port}")
        setup_express(project_dir, back_end_port)

    elif framework == "fullstack":
        print(f"⚡ React on {front_end_port}, 🚀 Express on {back_end_port}")
        setup_react(project_dir, front_end_port)
        setup_express(project_dir, back_end_port)

    else:
        print("⚠️ Unknown framework option")


if __name__ == "__main__":
    main()
