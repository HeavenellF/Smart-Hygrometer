from fastapi import FastAPI
from datetime import datetime
import random
import time
import threading



from data import HygrometerReading, Event
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Smart Hygrometer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# In-memory storage (MVP)
# -------------------------
readings: list[HygrometerReading] = []


# -------------------------
# Fake data generator
# (replace later with Govee sensor)
# -------------------------
def generate_fake_reading():
    return HygrometerReading(
        timestamp=datetime.utcnow(),
        temperature=21 + random.uniform(-1.5, 1.5),
        humidity=45 + random.uniform(-10, 10),
        events=[]
    )


def background_generator():
    while True:
        reading = generate_fake_reading()
        readings.append(reading)

        # keep memory small (last 200 entries)
        if len(readings) > 200:
            readings.pop(0)

        time.sleep(5)  # simulate sensor every 5 seconds


# start background thread
threading.Thread(target=background_generator, daemon=True).start()


# -------------------------
# API routes
# -------------------------

@app.get("/")
def root():
    return {"message": "Smart Hygrometer API running"}


@app.get("/latest")
def latest():
    if not readings:
        return None
    return readings[-1].to_dict()


@app.get("/readings")
def get_readings(limit: int = 50):
    return [r.to_dict() for r in readings[-limit:]]