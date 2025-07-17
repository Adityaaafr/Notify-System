from db.database import Base, engine
from db.models import Employee

# This will create the tables in the database
Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully.")
