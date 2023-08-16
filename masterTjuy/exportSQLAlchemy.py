import pandas as pd
from sqlalchemy import create_engine

def export_to_csv():
    db_connection = create_engine("mysql+pymysql://root:@localhost/flightestdb")

    query1 = "SELECT * FROM android;"
    query2 = "SELECT * FROM arduino;"

    df1 = pd.read_sql_query(query1, db_connection)
    df2 = pd.read_sql_query(query2, db_connection)

    df1.to_csv('./EXPORT CSV DB/android7.csv', index=False)
    df2.to_csv('./EXPORT CSV DB/arduino7.csv', index=False)

    print("Data telah diekspor ke android7.csv dan arduino7.csv")

export_to_csv()