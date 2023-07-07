### Auto ETL contains 3 three services:
<ul>
  <li>Process-Worker: receive, extract, send message to API-Management</li>
  <li>Api-Management: Contains CRUD endpoints, do business</li>
  <li>Fontend: Display Message Data in realtime</li>
</ul>

### Run Project
1. Clone this repo, make sure you have installed Docker and Docker Compose 

2. To run api-managment
 <ul>
  <li>cd into api-management/deploy</li>
  <li>Run the command: <i>docker compose up</i></li>
  <li>It will create 3 container: api-management public at localhost:5000. Feel free if you like postman or just access http://localhost:5000/docs for the Document API </li>
  <li>Two other services are mongodb and mongo-express which is a convenient container UI to manage mongoDB container, public at http://localhost:8081</li>
</ul>

3. To run process-worker
 <ul>
  <li>cd into process-worker/deploy</li>
  <li>Run the command: <i>docker compose up</i></li>
  <li>It will fake some message data and send k requests to API-Management at once. Try to adjust k if you need</li>
</ul>

4. To run font-end service 
 <ul>
  <li>locate into fontend folder. Choose open table.html in your browser (Chrome, FireFox). You will see data is refresh every 5 seconds.</li>
</ul>
