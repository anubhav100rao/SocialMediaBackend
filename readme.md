# Social Media backend
build using python, fastapi, postgres database, jwt authetication

# getting started
fork the repo <br>
clone the repository <br>
run pip3 install -r requirements.txt <br>
configurations for postgresql database, you may change as per your need
DATABASE_HOSTNAME=localhost<br>
DATABASE_PORT=5432<br>
DATABASE_PASSWORD=<br>
DATABASE_NAME=fastapi<br>
DATABASE_USERNAME=postgres<br>
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7<br>
ALGORITHM=HS256<br>
ACCESS_TOKEN_EXPIRE_MINUTES=30<br>

then you are ready <br>
just run uvicorn app.main:app --reload <br>
to start the development server