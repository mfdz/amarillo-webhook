while true
do

   git pull

   pip install -r requirements.txt

   echo "Starting CD"
   gunicorn main:app -w 1 -k uvicorn.workers.UvicornWorker --name=amarillo-cd --bind=0.0.0.0:8888
   echo "CD exited"

done