while true
do
   echo "Starting CD"
   uvicorn main:app --host 0.0.0.0 --port 8888
   echo "CD exited"

   git pull

   pip install -r requirements.txt
done