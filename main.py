from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys

sys.path.append("topmaf/models/")
sys.path.append("topmaf/")
from topmaf_api_models import topmaf_input, topmaf_output
import topmaf_calc

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#topmaf route
@app.post("/api/analyze/1/")
def read_data( log: topmaf_input):
    return log