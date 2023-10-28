1. Install mini-conda
2. create an environment with python==3.10
3. pip install using the pip_modules.txt file as input
3.1 install sqlite, mongodb,postgresql backends for your platforms and configure them
3.2 Change the code to point to your backend 
3.3 copy dot-env.template.txt file  to  .env file in each folder to edit it to put the secrets like password etc you use for your postgres user. IT MUST BE CALLED .env so the dot_env package can read it. It's a convention, don't fight it.
4. get hacking!
