while true
do

   git pull

   pip install --upgrade -r requirements.txt > pip.log
   [ $? -eq 0 ] && echo "Pip updated." || cat pip.log

   echo "CD starting."
   gunicorn main:app -w 1 -k uvicorn.workers.UvicornWorker --name=amarillo-cd --bind=0.0.0.0:8888
   echo "CD terminated."

done