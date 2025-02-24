from fastapi import FastAPI
import obd
import logging


app = FastAPI()

# Setup in-memory log capture
log_capture = []
class LogHandler(logging.Handler):
    def emit(self, record):
        log_capture.append(self.format(record))
        
# Configure logging
logger = logging.getLogger("obd")
logger.setLevel(logging.DEBUG)
log_handler = LogHandler()
log_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(log_handler)
        
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

@app.get("/logs")
def get_logs():
    """Fetch OBD logs from memory"""
    return {"logs": log_capture}