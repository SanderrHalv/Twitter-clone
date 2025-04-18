from dotenv import load_dotenv
import os
import psycopg2

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

print(f"Testing connection to: {DATABASE_URL}")

# Parse the connection string
if DATABASE_URL.startswith("postgresql://"):
    # Extract components from the URL
    parts = DATABASE_URL.replace("postgresql://", "").split("/")
    auth_host = parts[0].split("@")
    
    if len(auth_host) > 1:
        auth = auth_host[0]
        host_port = auth_host[1]
        
        if ":" in auth:
            username, password = auth.split(":")
        else:
            username = auth
            password = ""
            
        if ":" in host_port:
            host, port = host_port.split(":")
        else:
            host = host_port
            port = "5432"
        
        dbname = parts[1]
        
        # Try direct connection with psycopg2
        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=username,
                password=password,
                host=host,
                port=port
            )
            print("✅ Connection successful with psycopg2!")
            conn.close()
        except Exception as e:
            print(f"❌ Connection failed with psycopg2: {str(e)}")
else:
    print("URL doesn't start with postgresql://")