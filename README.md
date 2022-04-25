![img](./static/logo.png)
# IT-710-Project-Video-QnA-System

## About:
* The aim of our project is that we want to perform a semantic search on videos in a computationally efficient manner with the help of the URL provided by the user and to solve all the problems identified by making a simple tool. This project focuses on new techniques and approaches to develop a video question answering system.

* You can find an introductory video up [here](https://youtu.be/LwHQm7HycLo).

* You can watch a demo video up [here](https://youtu.be/6brrLMMggT0) 

* You can find the project report up [here](https://docs.google.com/document/d/1enCMVpbb-w6UhvvcZaBCS29bSEqQ0XkKK6aGNR9PjGI/edit?usp=sharing).

## How to setup:
>Currently we only support Linux and MacOS.

```bash
# Clone our repository
$ git clone https://github.com/programmer290399/IT-710-Project-Video-QnA-System.git

# Navigate to the project root
$ cd IT-710-Project-Video-QnA-System

# Create a virtual env
$ python3 -m venv .venv

# Activate the virtual env
$ . .venv/bin/activate 

# Install the dependencies
$ pip install -r requirements.txt

# Run the server
$ python manage.py runserver
```


## Citation:
```
@article{Seo2017BidirectionalAF,
    author = {Minjoon Seo and Aniruddha Kembhavi and Ali Farhadi and Hannaneh Hajishirzi},
    journal = {ArXiv},
    title = {Bidirectional Attention Flow for Machine Comprehension},
    volume = {abs/1611.01603},
    year = {2017}
}
```
