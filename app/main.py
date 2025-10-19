from app.init_server import init_server
import uvicorn

# Initialize the FastAPI app
app = init_server()

if __name__ == "__main__":
    # Run the server with auto-reload (like nodemon in Node.js)
    uvicorn.run("app.main:app", host="127.0.0.1", port=3000, reload=True)
