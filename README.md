# NOTE
When running *main.py*, the WikiText Corpus (~750MB) will be downloaded in */.cache/huggingface/datasets/wikitext* **unless** the corpus is included in *src/corpora*, which will only be included when submitting the final implementation.

Please expect to download ~750MB worth of data when running the program if the corpus is not included.

Once the model is trained, *a2a.wordvectors* and *a2a.wordvectors.vectors.npy* will show up in the folder somewhere. If this exists, running the program will use the trained model vectors, meaning it will not run as long as the first time.

If you would like to retrain the model, delete both *a2a.wordvectors* and *a2a.wordvectors.vectors.npy*, and if you would like to change the training corpus or play with model training variables, please modify the code in *src/agent.py* in the *train_model()* function.
