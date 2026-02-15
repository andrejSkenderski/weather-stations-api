import uvicorn

from app import create_app

app = create_app()


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8080, workers=1, http="httptools")


if __name__ == "__main__":
    main()
