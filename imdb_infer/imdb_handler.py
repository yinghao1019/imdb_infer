from google.cloud.storage.client import Client, Blob
from torch.nn.utils.rnn import pad_sequence
from tokenizers import Tokenizer
from collections import defaultdict
import configparser
import logging
import torch
import json
import os

import text
import imdb_model

text.init_logger()

logger = logging.getLogger(__name__)

# load etc file
config = configparser.ConfigParser()
config.read("imdb.ini")


# get tokenizer param with env
proejct_id = os.environ.get("PROJECT_ID")
token_uri = os.environ.get("TOKEN_URI")

# get preprocess param
max_sent = config["inference"].getint("max_sent")
max_tok = config["inference"].getint("max_tok")

# create model & tokenizer
idx_to_label = {0: "negative", 1: "positive"}
outputs = defaultdict(list)
client = Client(proejct_id)


class ModelHandler(object):
    """
    A custom model handler implementation.
    """

    def __init__(self):
        self._context = None
        self.initialized = False
        self.model = None
        self.device = None
        self.tokenizer = None

    def initialize(self, context):
        """
        Invoke by torchserve for loading a model
        :param context: context contains model server system properties
        :return:
        """
        logger.info("start to load model & tokenizer...")
        #  load the model
        self.manifest = context.manifest

        properties = context.system_properties
        model_dir = properties.get("model_dir")
        self.device = torch.device(
            "cuda:" + str(properties.get("gpu_id")) if torch.cuda.is_available() else "cpu")

        # Read model serialize/pt file
        serialized_file = self.manifest['model']['serializedFile']
        model_pt_path = os.path.join(model_dir, serialized_file)
        if not os.path.isfile(model_pt_path):
            raise RuntimeError("Missing the model.pt file")
        # loading model
        model = imdb_model.HierAttentionRNN(
            **{k: int(v) for k, v in config["model"].items()})
        model.load_state_dict(torch.load(
            model_pt_path, map_location=self.device))
        model.to(self.device)
        self.model = model
        logger.info("loading Model success!")

        # load tokenizer param
        blob = Blob.from_string(token_uri, client)
        tokenizer = Tokenizer.from_str(blob.download_as_text(encoding="utf-8"))
        self.tokenizer = tokenizer
        logger.info("loading Tokenizer success!")

        self.initialized = True

    def handle(self, data, context):
        """
        Invoke by TorchServe for prediction request.
        Do pre-processing of data, prediction using model and postprocessing of prediciton output
        :param data: Input data for prediction
        :param context: Initial context contains model server system properties.
        :return: prediction output
        """
        # extract from request body
        line = data[0]
        texts = line.get("data") or line.get("body")
        if isinstance(texts, bytearray):
            texts = texts.decode("utf-8")

        logger.info("Begin to inference from request data!")
        logger.info("Start raw clean & preprocess!")
        # clean raw data
        texts = text.rm_punct(text.strip_html(texts))

        #preprocess inference data to tensor
        texts,text_ents=self.preprocess(texts)
        texts.to(self.device)
        text_ents.to(self.device)

        # get model prediction
        logger.info("Get predictions by running model!")
        prob, _ = self.model(texts,text_ents)
        prob = torch.sigmoid(prob)
        labels = torch.where(prob >= 0.5, 1, 0)

        # create jspn format for predicition

        for idx, v in enumerate(labels):
            info = {
                "class num":2,
                "negative threshold":0.5,
                "positive probability": prob[idx].item(),
                "predicitions": idx_to_label[labels[idx].item()],
            }
            outputs["predictions"].append(info)

        logger.info("Inference Success!")

        return [outputs]

    def preprocess(self, raw_text):
        # preprocess
        doc = []
        doc_ents = []
        # split text to sent
        for s_id, s in enumerate(text.en_nlp(raw_text).sents):

            if s_id > max_sent:
                break

            tokens, ents = text.nlp_preprocess(s.text, self.tokenizer)
            tokens, ents = text.nlp_potsprocess(
                tokens[:max_tok], ents[:max_tok], self.tokenizer)

            #padding sequence
            tokens=list(tokens)+([0]*(max_tok-len(tokens)))
            ents=list(ents)+([0]*(max_tok-len(ents)))

            doc.append(tokens)
            doc_ents.append(ents)

        doc=torch.tensor(doc,dtype=torch.long,device=self.device).unsqueeze(dim=0)
        doc_ents=torch.tensor(doc_ents,dtype=torch.long,device=self.device).unsqueeze(dim=0)

        return doc,doc_ents
