import io
import contextlib

#For execution environment
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sklearn
import scipy

import traceback

NAME_TO_SHORT = {"pandas": "pd", "numpy": "np", "matplotlib.pyplot": "plt", "sklearn": "sklearn", "scipy": "scipy"}

def execute_python_code(code: str, variable_env: dict, expected_outputs: list):
    lib_env = {"pd": pd, "np": np, "sklearn": sklearn, "scipy": scipy, "plt": plt}
    # Create the execution environment and copy the original keys
    exec_env = {**variable_env, **lib_env}
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
    updated_venv = {}
    for key in variable_env.keys():
        updated_venv[key] = exec_env.get(key, variable_env[key])

    for key in expected_outputs:
        tmp = exec_env.get(key, None)
        if tmp is None:
            continue
        updated_venv[key] = tmp
    
    return stdout.getvalue().strip(), error, chart_path, chart_title, updated_venv
