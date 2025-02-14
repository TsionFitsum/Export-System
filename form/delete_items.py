from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
from app import FormData  # Ensure this correctly imports the model

# Define the correct database path
DATABASE_URL = "sqlite:///instance/formdatum.db"
engine = create_engine(DATABASE_URL)

# Debugging: Print database connection info
print(f"Using database: {engine.url}")

Session = sessionmaker(bind=engine)
session = Session()

try:
    # Step 2: Check if the table exists before trying to delete records
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    
    if "form_data" in table_names:
        # Step 3: Delete all records from the form_data table
        deleted_rows = session.query(FormData).delete()

        # Step 4: Commit the changes
        session.commit()
        print(f"Deleted {deleted_rows} records successfully from the form_data table.")
    else:
        print("Error: The table 'form_data' does not exist in the database.")

except Exception as e:
    session.rollback()  # Rollback in case of error
    print(f"Error occurred: {e}")

finally:
    # Step 5: Close the session
    session.close()

