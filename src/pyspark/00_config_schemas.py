# Configuration and explicit schemas for the crypto pipeline

from pyspark.sql.types import *

CATALOG = "crypto"
BRONZE_SCHEMA, SILVER_SCHEMA, OPS_SCHEMA = "bronze", "silver", "ops"

T_BRONZE = f"{CATALOG}.{BRONZE_SCHEMA}.market_data_raw"
T_SILVER = f"{CATALOG}.{SILVER_SCHEMA}.market_data_clean"
T_QUAR   = f"{CATALOG}.{BRONZE_SCHEMA}.quarantine"
T_LOGS   = f"{CATALOG}.{OPS_SCHEMA}.pipeline_execution_logs"

VOL       = f"/Volumes/{CATALOG}/{BRONZE_SCHEMA}/raw_files"
FULL_DIR  = VOL
INC_DIR   = VOL
FULL_FILE = f"{VOL}/crypto_hourly_full_load_100coins.json"
INC_FILE  = f"{VOL}/crypto_hourly_incremental_load_94coins.json"
for s in (BRONZE_SCHEMA, SILVER_SCHEMA, OPS_SCHEMA):
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{s}")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {CATALOG}.{BRONZE_SCHEMA}.raw_files")
BRONZE_SCHEMA_DEF = StructType([
    StructField("coin_id",        StringType(),    False),
    StructField("ts_ms",          LongType(),      False),
    StructField("price",          DoubleType(),    True),
    StructField("market_cap",     DoubleType(),    True),
    StructField("total_volume",   DoubleType(),    True),
    StructField("source_file",    StringType(),    True),
    StructField("load_type",      StringType(),    True),
    StructField("batch_id",       StringType(),    True),
    StructField("load_timestamp", TimestampType(), False),
])

SILVER_SCHEMA_DEF = StructType([
    StructField("coin_id",        StringType(),    False),
    StructField("event_ts",       TimestampType(), False),
    StructField("price",          DoubleType(),    True),
    StructField("market_cap",     DoubleType(),    True),
    StructField("total_volume",   DoubleType(),    True),
    StructField("event_date",     DateType(),      True),
    StructField("event_hour",     IntegerType(),   True),
    StructField("batch_id",       StringType(),    True),
    StructField("load_timestamp", TimestampType(), False),
])
QUAR_SCHEMA_DEF = StructType([
    StructField("raw_record",     StringType(),    True),
    StructField("reason",         StringType(),    True),
    StructField("source_file",    StringType(),    True),
    StructField("batch_id",       StringType(),    True),
    StructField("load_timestamp", TimestampType(), False),
])

LOG_SCHEMA_DEF = StructType([
    StructField("run_id",         StringType(),    False),
    StructField("layer",          StringType(),    True),
    StructField("file_or_params", StringType(),    True),
    StructField("start_time",     TimestampType(), True),
    StructField("end_time",       TimestampType(), True),
    StructField("status",         StringType(),    True),
    StructField("rows_inserted",  LongType(),      True),
    StructField("rows_updated",   LongType(),      True),
    StructField("error_message",  StringType(),    True),
])

RAW_REC_SCHEMA = StructType([
    StructField("coin_id",      StringType(), True),
    StructField("ts_ms",        LongType(),   True),
    StructField("price",        DoubleType(), True),
    StructField("market_cap",   DoubleType(), True),
    StructField("total_volume", DoubleType(), True),
])
EXP_KEYS = {"coin_id", "timestamp", "price", "market_cap", "total_volume"}

GOLD_SCHEMA = "gold"
G = f"{CATALOG}.{GOLD_SCHEMA}"
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {G}")

T_DIM_COIN     = f"{G}.dim_coin"
T_DIM_DATE     = f"{G}.dim_date"
T_DIM_HOUR     = f"{G}.dim_hour"
T_DIM_SCENARIO = f"{G}.dim_scenario"
T_BRIDGE       = f"{G}.bridge_scenario_coin"
T_FACT_HOURLY  = f"{G}.fact_market_hourly"
T_FACT_DAILY   = f"{G}.fact_coin_daily"
T_FACT_PORTF   = f"{G}.fact_portfolio_daily"



print(G, T_DIM_COIN)
display(spark.sql("SHOW SCHEMAS IN crypto"))