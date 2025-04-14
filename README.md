# Pomodoro Discord Bot

This is a Discord bot that helps you manage Pomodoro timers. It uses slash commands for a cleaner and more integrated experience.

## Prerequisites

-   Python 3.8 or higher
-   Discord bot token

## Setup

1.  **Clone the repository (if applicable):**

    ```bash
    git clone <repository_url>
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```

3.  **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set your Discord bot token:**

    -   **Using environment variables (recommended):**
        -   **macOS/Linux:**
            ```bash
            export DISCORD_TOKEN='YOUR_BOT_TOKEN'
            ```
            (Add this line to your `.bashrc` or `.zshrc` file to make it permanent.)
        -   **Windows:**
            ```powershell
            setx DISCORD_TOKEN "YOUR_BOT_TOKEN"
            ```
            (Use `setx /M` for system-wide variables.)
    -   **Using a `.env` file:**
        1.  Create a `.env` file in the same directory as `bot.py`.
        2.  Add the following line to the `.env` file:
            ```
            DISCORD_TOKEN=YOUR_BOT_TOKEN
            ```
        3.  Make sure you have `python-dotenv` in your requirements.txt.
        4.  Add `load_dotenv()` to the start of your bot.py.

5.  **Run the bot:**

    ```bash
    python bot.py
    ```

## Usage

Use the following slash commands in your Discord server:

-   `/pomodoro [minutes]`: Starts a Pomodoro timer with optional minutes (default 25).
-   `/stop`: Stops the currently running timer.
-   `/pause`: Pauses the timer.
-   `/resume`: Resumes the paused timer.
-   `/skip`: Skips to the next timer.
-   `/clear <amount>`: Clears the specified number of messages.
-   `/help`: Displays this help message.

## Contributing

Feel free to contribute to this project by submitting pull requests.

