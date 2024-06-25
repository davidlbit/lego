#!/usr/bin/env python3
######################################################################
# Authors: David Anthony Parham
#
# Module Description: This script loads the environment variables
# and establishes a connection to the database.
######################################################################

import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables from .env file
load_dotenv()

# Fetch database connection details from environment variables
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# Ensure all necessary environment variables are set
if not all([db_user, db_password, db_host, db_name]):
    raise OSError("Database environment variables are not fully set.")

# Ensure db_password is a string or handle the case where it's None
if db_password is None:
    raise ValueError("DB_PASSWORD environment variable must be set")

# Handle special characters in the password variable
encoded_password = quote_plus(db_password)

# Construct the database URL
database_url = f"postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"

# Create the SQLAlchemy engine
engine = create_engine(database_url)
