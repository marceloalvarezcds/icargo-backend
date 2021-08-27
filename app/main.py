import uvicorn

from app import app

# Run Server
if __name__ == '__main__':
    uvicorn.run(app)
    # app.run(host="0.0.0.0", debug=True)
