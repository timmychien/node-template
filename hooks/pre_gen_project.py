# hooks/pre_gen_project.py
import sys

framework = '{{ cookiecutter.framework }}'

if framework == 'react':
    # Skip backend port by setting default
    print("Skipping backend port prompt for React-only project.")
    sys.stdout.write('\n')  # default empty
elif framework == 'express':
    # Skip frontend port by setting default
    print("Skipping frontend port prompt for Express-only project.")
    sys.stdout.write('\n')  # default empty
# For fullstack, both prompts remain