while true
do

   git pull > git.log
   [ $? -eq 0 ] && git log -1 || cat git.log

   pip install --upgrade -r requirements.txt > pip.log
   [ $? -eq 0 ] && pip list || cat pip.log

   echo "Starting CD"
   gunicorn main:app -w 1 -k uvicorn.workers.UvicornWorker --name=amarillo-cd --bind=0.0.0.0:8888
   echo "CD exited"

done