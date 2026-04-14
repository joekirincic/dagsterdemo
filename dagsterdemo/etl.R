library(dagsterpipes)
library(DBI)

with_dagster_pipes(
  function(ctx) {
    ctx$log("Starting ETL process.")

    ctx$log("Fetching data from DB.")

    con <- dbConnect(
      drv = RPostgres::Postgres(),
      dbname = ctx$get_extra("DB_NAME"),
      host = ctx$get_extra("DB_HOST"),
      port = ctx$get_extra("DB_PORT") |> as.integer(),
      user = ctx$get_extra("DB_USER"),
      password = ctx$get_extra("DB_PASSWORD")
    )

    df <- mtcars

    ctx$log("Fetched data from DB.")

    dbWriteTable(con, name = "mtcars", value = df, overwrite = TRUE)

    ctx$log("Finished ETL process.")

    ctx$report_asset_materialization(
      metadata = list(
        row_count = pipes_metadata_value(nrow(df), "int")
      )
    )

    ctx$log("Process completed.")
  }
)
