import io
import contextlib
import matplotlib.pyplot as plt
import pandas as pd
import traceback

def execute_python_code(code: str, dataframes: dict):
    # Create the execution environment and copy the original keys
    exec_env = {**dataframes, "pd": pd, "plt": plt}
    stdout = io.StringIO()
    error = None
    chart_path = None
    chart_title = ""
    
    try:
        with contextlib.redirect_stdout(stdout):
            exec(code, exec_env)
            fig = plt.gcf()
            if fig.get_axes():
                # Try to obtain the first non-empty title from the figure
                for ax in fig.get_axes():
                    title = ax.get_title()
                    if title:
                        chart_title = title
                        break
                chart_path = f"/tmp/chart_{hash(code)}.png"
                fig.savefig(chart_path)
                plt.close(fig)
    except Exception as e:
        error = traceback.format_exc()
    
    # Capture updated dataframes from the execution environment.
    # We assume that the keys in the original 'dataframes' dict remain the same.
    updated_dataframes = {}
    for key in dataframes.keys():
        updated_dataframes[key] = exec_env.get(key, dataframes[key])
    
    return stdout.getvalue().strip(), error, chart_path, chart_title, updated_dataframes
