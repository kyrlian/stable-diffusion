import sys
from streamlit.web import cli

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0 :
        args[0] = "app.py"
    cli.main_run(args)

# Run with:
# python streamlit_runner.py streamlit_app.py