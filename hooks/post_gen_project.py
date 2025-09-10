import os
import subprocess
import time
def setup_express(project_dir, back_end_port):
    server_dir = os.path.join(project_dir, "server")
    os.makedirs(server_dir, exist_ok=True)

    # Initialize npm & install express
    subprocess.run(["npm", "init", "-y"], cwd=server_dir)
    subprocess.run(["npm", "install", "express"], cwd=server_dir)

    index_file = os.path.join(server_dir, "index.js")
    if not os.path.exists(index_file):
        # build JS content line by line
        js_content = (
            'const express = require("express");\n'
            'const app = express();\n'
            f'const port = process.env.PORT || {back_end_port};\n\n'
            'app.get("/", (req, res) => {\n'
            '  res.send("Hello from {{ cookiecutter.project_name }} backend!");\n'
            '});\n\n'
            'app.listen(port, () => console.log(`Server running at http://localhost:${port}`));\n'
        )
        with open(index_file, "w") as f:
            f.write(js_content)

import os
import subprocess
import time

def setup_react(project_dir, front_end_port):
    """
    Sets up a React frontend with Vite inside the generated project.
    - project_dir: Root directory of the generated project (from Cookiecutter)
    - front_end_port: Custom port for Vite dev server
    """
    # Ensure client directory is inside the project root
    client_dir = os.path.join(project_dir, "client")

    # 1️⃣ Create Vite React app if it doesn't exist
    if not os.path.exists(client_dir):
        print(f"🚀 Creating React app in {client_dir} ...")
        subprocess.run(
            ["npm", "create", "vite@latest", client_dir, "--", "--template", "react"],
            cwd=project_dir,
            check=True
        )

    # 2️⃣ Path to vite.config.js
    vite_config = os.path.join(client_dir, "vite.config.js")

    # 3️⃣ Wait for vite.config.js to exist (max 5s)
    for _ in range(10):
        if os.path.exists(vite_config):
            break
        time.sleep(0.5)
    else:
        print(f"⚠️ vite.config.js not found in {client_dir}, skipping patch.")
        return

    # 4️⃣ Patch vite.config.js for custom port if not already patched
    with open(vite_config, "r", encoding="utf-8") as f:
        content = f.read()

    if "server:" not in content:
        print(f"🔧 Patching vite.config.js to use port {front_end_port} ...")
        new_content = content.replace(
            "export default defineConfig({",
            (
                "export default defineConfig({\n"
                "  server: {\n"
                f"    port: {front_end_port},\n"
                "    host: true\n"
                "  },"
            ),
            1
        )
        with open(vite_config, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("✅ vite.config.js patched successfully.")
    else:
        print("ℹ️ vite.config.js already contains server config; skipping patch.")

def main():
    project_dir = os.getcwd()
    # these will already be replaced by cookiecutter before the hook runs
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