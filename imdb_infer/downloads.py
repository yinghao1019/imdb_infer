from google.cloud.storage import Client,Blob
import os

project_id=os.environ.get("PROJECT_ID")
model_dir=os.environ.get("MODEL_PATH")
model_uri=os.environ.get("MODEL_URI")


def main():
    client=Client(project_id)
    save_path=os.path.join(model_dir,"model.pt")

    if not os.path.isfile(save_path):
        src=Blob.from_string(model_uri,client)
        src.download_to_filename(save_path)
    

if __name__=="__main__":
    main()
