from flask import request,g,Blueprint
from db import get_db

bp = Blueprint('bp',__name__)

@app.route('/',method=['GET','POST'])
def index():
    if request.method == 'POST':


