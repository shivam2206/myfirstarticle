# My First Article 
## A simple blogging application developed in Python with the following tech stack.
### Flask + MySQL + Nginx + Gunicorn + Celery + Docker + Automated Testing

[![screen1.png](https://i.postimg.cc/dVGd4wpP/screen1.png)](https://postimg.cc/fVTJbnMB)

It's just a result of the motivation to sharpen my as well as other's skills in Flask. The intention behind making this an open-source project is just to hear about the possible improvements from the brilliant minds of the rest of the world.
I am trying my best to make this project production-ready not only from the deployment perspective but more from a robust & scalable code perspective. During my learning days, I really couldn't find any single place helping in understanding different Flask features/extensions altogether. Flask is not alone, it comes with its vast ecosystem.

I will keep adding stuff to make this one place for most of the developers who are in the early stages of learning Python &amp; Flask-based production-ready applications.

I'll appreciate any feedback. I am very active on the following platforms - 
- <a href="https://github.com/shivam2206">Github</a>
- <a href="https://www.linkedin.com/in/shivam2206/">Linkedin</a>

## Screenshots

[![screen2.png](https://i.postimg.cc/YCNGQ8Lt/screen2.png)](https://postimg.cc/yDd8HmTG)

[![screen3.png](https://i.postimg.cc/Hn7jntCD/screen3.png)](https://postimg.cc/Lg2m0LXN)

[![screen4.png](https://i.postimg.cc/BvQT6RYr/screen4.png)](https://postimg.cc/CRXBrrV7)


### Run Using Docker
- Step 1: Clone the repo.<br>
  ```git clone https://github.com/shivam2206/myfirstarticle.git```


- Step 2: Install docker and docker-compose. <a href="https://docs.docker.com/get-docker/">Get Docker</a>


- Step 3: Change working directory to myfirstarticle. <br>
  ```cd myfirstarticle```


- Step 4: Run using docker-compose <br>
    ```sudo docker-compose up --build```

  
- Step 5: Visit the following URL to access the application homepage.
  <a href="http://localhost/"> http://localhost/ </a>
  

### Install & Run (Local)
- Step 1: Clone the repo.<br>
  ```git clone https://github.com/shivam2206/myfirstarticle.git```


- Step 2: Create & Activate Python3 virtual environment. <br>
  ```sudo apt install python3-venv``` <br>
  ```python3 -m venv venv``` <br>
  ```source venv/bin/activate```


- Step 3: Change working directory to myfirstarticle. <br>
  ```cd myfirstarticle```
  

- Step 4: Install dependencies <br>
    ```sudo apt-get install build-essential libssl-dev libffi-dev python3-dev cargo``` <br>
    ```pip install -r requirements.txt```


- Step 5: Run migrations <br>
  Assuming you already have MySQL installed.
  ```export DATABASE_URI=mysql+pymysql://username:password@localhost/master_db``` <br>
  ```flask db upgrade```


- Step 6: Run test cases (Optional) <br>
    ```pytest . tests/```


- Step 7: Run using Flask <br>
    ```flask run```
  

- Step 8: Visit the following URL to access the application homepage.
  <a href="http://127.0.0.1:5000/"> http://127.0.0.1:5000/ </a>
  
### Enjoy!!