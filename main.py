from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys

sys.path.append("topmaf/models/")
sys.path.append("topmaf/")
from lowmaf_request_model import lowmaf_input, lowmaf_output
import lowmaf_calc

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#lowmaf route
@app.post("/api/analyze/0/", response_model = list[lowmaf_output])
def read_data( log: list[lowmaf_input] ):
    print("Received data that fits into model.")
    resp = lowmaf_calc.main(log)
    print("Calculations completed. Responding with scaling data.")
    return resp
