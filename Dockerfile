FROM continuumio/anaconda3:latest

ENV HOME '/home/pokebot'

# RUN apt-get update -y && \
#     apt-get install -y 

WORKDIR ${HOME}

COPY ./pokebot-env.yml ${HOME}

RUN cd ${HOME} \
    && conda env create -f pokebot-env.yml

SHELL ["conda", "run", "-n", "pb_env", "/bin/bash", "-c"]

# Make sure the environment is activated:
RUN echo "Make sure keras is installed:"
RUN python -c "import tensorflow.keras as keras"

# Copy the rest of the application
COPY . ${HOME}

#Install pokebot
RUN cd ${HOME} \
    && mkdir models \
    && pip install -e .

# TODO: Fetch latest model using wandb

ENTRYPOINT [ "conda", "run", "--no-capture-output", "-n", "pb_env", "python" ]
CMD [ "scripts/train.py", "scripts/hparams.json", "${HOME}/models" ]
