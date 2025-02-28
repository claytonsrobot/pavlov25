# __main__.py
from shell import main

def cli_entry():
    try:
        # Launch the cmd2 terminal
        main()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    cli_entry()
