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
* Google cloud sdk
* pytorch

#### **Installation**

1. clone this repository

   ```bash
   git clone https://github.com/yinghao1019/imdb_prac.git
   ```
2. download this dataset from http://ai.stanford.edu/~amaas/data/sentiment/ and move to project dir
3. Create bucket on your cloud project
4. set ENV for training
   ```CMD
   set BUCKET_NAME=${your storage bucket}
   set PROJECT_ID=${project id}
   set CLOUD_TRAINDATA_PATH=gs//:${your train data path}
   set CLOUD_TESTDATA_PATH=gs//:${your test data path}
   set CLOUD_TOKENIZER_PATH=gs//:${your tokenizer data path}
   set AIP_MODEL_DIR=gs://${your model path}
   set PYTHONPATH=.
   ```

### **Usage**
1.  Before use training application.Confirm you have clean csv data & tokenizer.
    Please clean data and run below command if you don't.

    ```bash
    python generate.py data ${your_data_path} ${cloud_data_path} -n 12500
    ```

    And then useing clean data to train tokenizer

    ```bash
    python generate.py token ${your_data_path} ${cloud_token_path} -ms 25000
    ```

2.  Run the main program to training NLP model

    ```bash
    python task.py  --ep 10 --warm_ep 3 --batch_size 64 --max_sentN 5
    ```

## **Start with Vertex Ai**
If you training models's resource is limited,it's  highly recommended that you can use the GCP
service-Vertex ai to create custom training.PLease click this link to know more :
[Vertex AI custom training documentation.](https://cloud.google.com/vertex-ai/docs/training/custom-training)

1. You should use docker to buid container for custom training,So must run below command:
    ```bash
    docker build -t={your_image_name_in_Artifact_registry_Repo} .
    ```

2. Before let Vertex Ai to use your customized container,you should create repository in Artifact registry.
    Please read [Artifact Registry documentation](https://cloud.google.com/artifact-registry/docs/manage-repos) to create.

3. Then set up your authentication to allow docker access cloud service.
    Please read [Work with container Image](https://cloud.google.com/artifact-registry/docs/docker) to know how to use.

## **Learn More**
After you training ,if you want to serve for other application,please follow below link.
[Deploy trained model service with Vertex Ai]()

## **Contact**
Ying Hao Hung-1104137203@gmail.com
Project link : https://github.com/yinghao1019/imdb_prac



