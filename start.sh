#!/bin/bash

# Start PG
PG_BIN="/opt/homebrew/opt/postgresql@14/bin/postgres"
PG_DATA_DIR="/opt/homebrew/var/postgresql@14"
PG_LOG_FILE="/opt/homebrew/var/log/postgresql@14.log"

# Start the PostgreSQL server in the background
$PG_BIN -D $PG_DATA_DIR > $PG_LOG_FILE 2>&1 &
