from fastapi import FastAPI
import obd

app = FastAPI()
connection = obd.OBD()  # Auto-connect to OBD adapter

@app.get("/")
def root():
    return {"message": "Hello World"}
  

@app.get("/data")
def get_obd_data():
    if connection.is_connected():  # Check OBD connection
        cmd = obd.commands.SPEED  # Select speed command
        response = connection.query(cmd)  # Query the OBD adapter

        if response.value is None:  # Ensure there's a valid response
            return {"error": "Unable to get value"}
        
        return {"speed": response.value.to("mph")}  # Convert speed to mph
    else:
        return {"error": "Not connected to OBD adapter"}
