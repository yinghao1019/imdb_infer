<h1 aling="left">Imdb_infer</h1>
<p >Imdb_infer is a nlp ai project for deploy to torch model server.</p>

## **Project Articture**
### **torchserve user guide**
 ![Repo](https://i.imgur.com/FeYw5Y0.jpg)

Before you create your model prediction API on torch server.you should prepare three files :
imdb_handler,trained Model,Model handler.  And run **torch-model-archiver** to packaging three
files to **"*.mar"** file.Finally, put TorchServe in the .mar file and deploy it after registration!
If you want to know more,please follow this [link](https://pytorch.org/serve/)!

* imdb_handler : use to handle data to model's input format for server recieved request.
                 Need text process fun in text module

* Trained Model : the model file for get request predictions.

* Model handler : The maintain model compute arcticture.


### **Built with**
* pytorch
* GCP Vertex api
* torchserve

<h1 aling="left">Getting started</h1>

#### **Prerequisites**
* Trained model
* Google cloud sdk(Vertex Ai service)
* pytorch
* Docker
#### **Installation**

1. clone this repository

   ```bash
   git clone https://github.com/yinghao1019/imdb_infer.git
   ```
2. Install [Docker](https://www.docker.com/products/docker-desktop)

3. prepare [google service account credentials](https://cloud.google.com/docs/authentication/production)

4. Prepare your repo in Google cloud artifact registry.

5. modified Environment variable in Dockerfile & put your credential in project

### **Usage**
1.  Before create your model service,confirm you already have model instance file.
    If not,run this command to donwload

    ```bash
    python ./imdb_infer/downloads.py
    ```

2.  And then in order to deploy to Vertex Ai endpoint for serve predicition,
    Run command to build your custom container image.

    ```bash
    docker build -t="${your image name}" .
    ```

3. Run your image and use curl to test server.
    ```bash
    docker run -d -p 8080:8080 -p 8081:8081 -p 8082:8082 ${your image name}
    curl http://localhost:8080/ping
    ```
4. set up docker access artifact premisson and upload to cloud repo by following
    [this documentation](https://cloud.google.com/artifact-registry/docs/docker)


## **Learn More**
If you don't have trained model,you can click this project link to see how to training.
[Training model with Vertex Ai](https://github.com/yinghao1019/imdb_prac)

## **Contact**
Ying Hao Hung-1104137203@gmail.com
Project link : https://github.com/yinghao1019/imdb_prac



