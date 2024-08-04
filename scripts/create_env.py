import os
import re

# ANSI escape sequences for colors
COLOR_RESET = "\033[0m"
COLOR_PROMPT = "\033[1;34m"
COLOR_HINT = "\033[1;33m"
COLOR_ERROR = "\033[1;31m"
COLOR_SUCCESS = "\033[1;32m"

def ask_for_input(prompt, example=None, hint=None, validation_regex=None):
    while True:
        if hint:
            print(f"{COLOR_HINT}Hint: {hint}{COLOR_RESET}")
        if example:
            print(f"{COLOR_HINT}Example: {example}{COLOR_RESET}")
        value = input(f"{COLOR_PROMPT}{prompt}: {COLOR_RESET}").strip()

        if validation_regex:
            if not re.match(validation_regex, value):
                print(f"{COLOR_ERROR}Error: '{value}' is not valid. Please try again.{COLOR_RESET}")
                continue

        if value:
            return value
        else:
            print(f"{COLOR_ERROR}Error: Value cannot be empty. Please try again.{COLOR_RESET}")

def create_env(template_file, output_file):
    if not os.path.exists(template_file):
        print(f"{COLOR_ERROR}Template file '{template_file}' does not exist.{COLOR_RESET}")
        return

    env_vars = {}

    with open(template_file, 'r') as template:
        for line in template:
            if line.strip().startswith("#") or not line.strip():
                continue  # Skip comments and empty lines

            key, value = line.strip().split('=', 1)

            # Ask for input only for variables that require user input
            if key == "DISCORD_TOKEN":
                env_vars[key] = ask_for_input(
                    f"Enter {key}",
                    example=value,
                    hint="You can get this value from the Discord Developer Portal under 'Bot' > 'Token'",
                    validation_regex=r"^[a-zA-Z0-9_\.\-]{20,}$"
                )
            elif key == "DISCORD_CHANNEL_ID":
                env_vars[key] = ask_for_input(
                    f"Enter {key}",
                    example=value,
                    hint="To find your Discord Channel ID, enable Developer Mode in Discord, right-click on the channel, and select 'Copy ID'",
                    validation_regex=r"^\d{19}$"
                )
            elif key == "KEYWORDS":
                env_vars[key] = ask_for_input(
                    f"Enter {key}",
                    example=value,
                    hint="Enter the keywords for jobs you're interested in, separated by commas.",
                    validation_regex=r"^[a-zA-Z0-9,\s]+$"
                )
            elif key == "UPWORK_RSS_URL":
                env_vars[key] = ask_for_input(
                    f"Enter {key}",
                    example=value,
                    hint="Enter the URL of the RSS feed you want to monitor. For custom searches, modify the query in the URL.",
                    validation_regex=r"^https?://\S+$"
                )
            else:
                env_vars[key] = value

    with open(output_file, 'w') as env_file:
        for key, value in env_vars.items():
            env_file.write(f"{key}={value}\n")

if __name__ == "__main__":
    template_path = ".env.template"
    output_path = ".env"
    create_env(template_path, output_path)
