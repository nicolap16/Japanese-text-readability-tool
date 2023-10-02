import pandas as pd
from readability import app, db
from sqlalchemy import create_engine

# Transferring data from excel spreadsheets to MySQL database using pandas library. Adapted from https://www.youtube.com/watch?v=oN0koUt3SXQ, accessed 18th July 2023

def create_tables():
    with app.app_context():
        db.create_all()
        db.session.commit()
        print("database tables created")

def transfer_data(excel_file, table_name):
    
    df = pd.read_excel(f'{excel_file}') # read excel file into pandas dataframe
    engine = create_engine('mysql+pymysql://c21016073:Vilanova2020@csmysql.cs.cf.ac.uk:3306/c21016073_jrt') # set up connection
    df.to_sql(f'{table_name}', con=engine, if_exists='append', index=False)

    print(f"Excel transfer of {table_name} complete")

# create_tables()
transfer_data('/Users/nicolaphillips/Library/CloudStorage/OneDrive-CardiffUniversity/1. Cardiff/0. Dissertation/JLPT Excel/goi/Goi N5.xlsx', 'word')