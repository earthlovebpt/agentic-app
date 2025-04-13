import io
import contextlib
import matplotlib.pyplot as plt
import pandas as pd
import traceback

def execute_python_code(code: str, dataframes: dict):
    exec_env = {**dataframes, "pd": pd, "plt": plt}
    stdout = io.StringIO()
    error = None
    chart_path = None

    try:
        with contextlib.redirect_stdout(stdout):
            exec(code, exec_env)
            fig = plt.gcf()
            if fig.get_axes():
                chart_path = f"/tmp/chart_{hash(code)}.png"
                fig.savefig(chart_path)
                plt.close(fig)
    except Exception as e:
        error = traceback.format_exc()

    return stdout.getvalue().strip(), error, chart_path
