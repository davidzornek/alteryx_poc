# Alteryx Interview POC

This code is a POC to demonstrate competency with Alteryx's interview assignment. The actual deliverable is the code under the `alteryx_poc` directory, which can be imported and used in other software. Also included are various environment-defining artifacts and a very basic dev infrastructure demonstrating competency with best practices and an understanding of basic DevOps. I have also included a notebook `Example.ipynb`, which demonstrates chatbot behavior on my own examples, but users are invited to interact with the chatbot using their own inputs as well.


To run the demo notebook, do the following:
- `git clone git@github.com:davidzornek/alteryx_poc.git`
- `cd alteryx_poc`
- `cp .env.example .env`, and then populate the appropriate API Keys.
- `docker build -t alteryx_poc .`
- `docker run -v <path to your local repo>:/src/ -p 8888:8888 -it --name alteryx_poc alteryx_poc bash`
    - Note that if the `alteryx_poc` container already exists, you will get an error from the above. In that case, do:
    - `docker start alteryx_poc`
    - `docker exec -it alteryx_poc bash`
- Once inside the container:
    - `jupyter notebook --allow-root --no-browser --ip=0.0.0.0 --port=8888`
- Copy-past the url printed into the console and open up `Example.ipynb`