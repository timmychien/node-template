import os
import subprocess
import time
import shutil

def setup_express(project_dir, back_end_port):
    """
    Sets up Express backend in project_dir/server
    """
    server_dir = os.path.join(project_dir, "server")
    os.makedirs(server_dir, exist_ok=True)

    print(f"🚀 Creating Express app in {server_dir} ...")
    subprocess.run(["npm", "init", "-y"], cwd=server_dir, check=True)
    subprocess.run(["npm", "install", "express"], cwd=server_dir, check=True)

    index_file = os.path.join(server_dir, "index.js")
    if not os.path.exists(index_file):
        js_content = (
            'const express = require("express");\n'
            'const app = express();\n'
            f'const port = process.env.PORT || {back_end_port};\n\n'
            'app.get("/", (req, res) => {\n'
            '  res.send("Hello from {{ cookiecutter.project_name }} backend!");\n'
            '});\n\n'
            'app.listen(port, () => console.log(`Server running at http://localhost:${port}`));\n'
        )
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(js_content)
        print(f"✅ Express server created at {server_dir}")


def setup_react(project_dir, front_end_port):
    """
    Sets up React frontend with Vite in project_dir/client
    """
    client_dir = os.path.join(project_dir, "client")

    # Remove partially created folder to avoid nesting issues
    if os.path.exists(client_dir):
        shutil.rmtree(client_dir)
    os.makedirs(client_dir, exist_ok=True)

    print(f"🚀 Creating React app in {client_dir} ...")
    # Run Vite in the empty client directory
    subprocess.run(
        ["npm", "create", "vite@latest", ".", "--", "--template", "react"],
        cwd=client_dir,
        check=True
    )

    vite_config = os.path.join(client_dir, "vite.config.js")

    # Wait for vite.config.js (max 5 seconds)
    for _ in range(10):
        if os.path.exists(vite_config):
            break
        time.sleep(0.5)
    else:
        print(f"⚠️ vite.config.js not found in {client_dir}, skipping patch.")
        return

    # Patch vite.config.js for custom port
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

    # Cookiecutter variables
    framework = "{{ cookiecutter.framework }}"
    front_end_port = int("{{ cookiecutter.front_end_port }}")
    back_end_port = int("{{ cookiecutter.back_end_port }}")

    if framework == "react":
        setup_react(project_dir, front_end_port)

    elif framework == "express":
        setup_express(project_dir, back_end_port)

    elif framework == "fullstack":
        setup_react(project_dir, front_end_port)
        setup_express(project_dir, back_end_port)

    else:
        print("⚠️ Unknown framework option")


if __name__ == "__main__":
    main()