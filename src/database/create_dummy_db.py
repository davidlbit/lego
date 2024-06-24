#!/usr/bin/env python3
######################################################################
# Authors:  David Anthony Parham

# Module Description: This script acts as the main script, for
# creating, a dummy database that follows the intend design layout
# for this project.
######################################################################

from database.config import engine
from mockup.fake_db_data_generation import create_tables, fetch_order_info, populate_tables

if __name__ == "__main__":
    # Create database tables
    create_tables(engine)

    # Populate tables with synthetic data
    populate_tables(engine)

    # Retrieve order information
    fetch_order_info(engine)
