while true
do
   echo "Starting CD"
   gunicorn main:app -w 1 -k uvicorn.workers.UvicornWorker --name=amarillo-cd --bind=0.0.0.0:8888

   echo "CD exited"

   git pull

   pip install -r requirements.txt
done