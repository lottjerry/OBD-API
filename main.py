from fastapi import FastAPI, JSONResponse
import obd

app = FastAPI()
connection = obd.OBD() # auto-connects to serial or bluetooth

@app.get("/")
def root():
  return {"Hello World"}

@app.get("/data")
def get_obd_data():
    if connection.is_connected(): # If there is a connection
        cmd = obd.commands.SPEED # select an OBD command (sensor)
        response = connection.query(cmd) # send the command, and parse the response
        if response.is_null(): # if there is a response
            return {"Error": "Unable to get value"}
        return {"speed": response.value.to("mph")}
    else:
        return {"Error": "Not connected to OBD adapter"}