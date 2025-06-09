import pandas as pd

# Read CSV
df = pd.read_csv(r'C:\Users\uprightness.eziukwu\Documents\phed\TradeBot\feederoracle.csv')
# Exclude non-numeric FEEDERID (to avoid issues with FEEDERID = '9999')
df = df[df['FEEDERID'].apply(lambda x: str(x).isdigit())]

# Generate INSERT statements
insert_statements = []
for _, row in df.iterrows():
    feederid = row['FEEDERID']
    description = f"'{str(row['DESCRIPTION']).replace('\'', '\'\'')}'"
    location = f"'{str(row['LOCATION']).replace('\'', '\'\'')}'"
    lat = f"'{row['LAT']}'"
    lon = f"'{row['LON']}'"
    routelenght = f"'{row['ROUTELENGHT']}'"
    feederzoneid = f"'{row['FEEDERZONEID']}'"
    substationid = row['SUBSTATIONID']
    description2 = f"'{str(row['DESCRIPTION2']).replace('\'', '\'\'')}'"
    createdby = f"'{row['CREATEDBY']}'"
    # Parse CREATEDON with explicit format
    createdon = f"'{pd.to_datetime(row['CREATEDON'], format='%d-%b-%y %I.%M.%S.%f %p').strftime('%Y-%m-%d %H:%M:%S.%f')}'"
    recid = row['RECID']
    insert_statements.append(f"({feederid}, {description}, {location}, {lat}, {lon}, {routelenght}, {feederzoneid}, {substationid}, {description2}, {createdby}, {createdon}, {recid})")

# Write to SQL file
with open('insert_statements.sql', 'w') as f:
    f.write('INSERT INTO OracleFeederImportedTable (FEEDERID, DESCRIPTION, LOCATION, LAT, LON, ROUTELENGHT, FEEDERZONEID, SUBSTATIONID, DESCRIPTION2, CREATEDBY, CREATEDON, RECID) VALUES\n')
    f.write(',\n'.join(insert_statements) + ';')