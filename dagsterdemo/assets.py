

import dagster as dg
from pathlib import Path
import os

R_ETL_SCRIPT = Path(__file__).parent.joinpath("etl.R")

@dg.asset()
def r_asset(context: dg.AssetExecutionContext, pipes_subprocess_client: dg.PipesSubprocessClient):
    return pipes_subprocess_client.run(
        command=["Rscript", str(R_ETL_SCRIPT)],
        context=context,
        extras={
            "DB_HOST": os.getenv("DB_HOST"),
            "DB_PORT": os.getenv("DB_PORT"),
            "DB_NAME": os.getenv("DB_NAME"),
            "DB_USER": os.getenv("DB_USER"),
            "DB_PASSWORD": os.getenv("DB_PASSWORD")
        }
    ).get_materialize_result()
