

FROM pytorch/pytorch:1.8.1-cuda11.1-cudnn8-runtime

WORKDIR /home/
RUN mkdir model_store
COPY . /home/imdb_infer/
RUN mv /home/imdb_infer/docker-entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

#set for download model
ENV PROJECT_ID  {your_project_id}
ENV MODEL_PATH /home/imdb_infer/models
ENV TOKEN_URI {your_token_uri}
ENV MODEL_URI {your_model_path}
ENV GOOGLE_APPLICATION_CREDENTIALS {your_credential_path}



#install java11
RUN apt-get update && \
    apt-get -y install openjdk-11-jre-headless && \
    rm -rf /var/lib/apt/lists/*

#install dependencies
RUN pip install torchserve==0.3.0 torch-model-archiver==0.3.0 \
    && pip install -r ./imdb_infer/requirements.txt

#install spacy gpu version package
RUN pip install -U spacy[cuda111]

#download model to dir from cloud
RUN cd imdb_infer/imdb_infer && \
    python downloads.py

#packaging source to mar file
RUN torch-model-archiver \
  --model-name=imdb \
  --version=1.0 \
  --model-file=/home/imdb_infer/imdb_infer/imdb_model.py \
  --serialized-file=/home/imdb_infer/models/model.pt \
  --handler=/home/imdb_infer/imdb_infer/imdb_handler.py \
  --export-path=/home/model_store \
  --extra-files="/home/imdb_infer/imdb_infer/text.py,/home/imdb_infer/imdb_infer/imdb.ini" \
  --requirements-file=/home/imdb_infer/requirements.txt





EXPOSE 8080
EXPOSE 8081
EXPOSE 8082

#severing
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["serve"]








