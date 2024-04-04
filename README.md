### Ensure the following before you run the program:
You are on the student server *(to run with python3.11)*.
You have *nltk*, *gensim*, *numpy*, and *datasets* in your system or venv. If not, install them through *pip*:
- *pip install nltk*
- *pip install gensim*
- *pip install numpy*
- *pip install datasets*


# Running the program
### w/Basic Cards
To run the program with basic cards, navigate to the location of the makefile, then in the Terminal execute: 
- *make run*

This will run the program using the basic green and red cards included in *src/*

### w/Extensions
To run the program with extension cards, execute the following command:
- *./src/main.py [args like in agent specification]*

Or if you are in *src/* folder:
- *./main.py [args like in agent specification]*


# Files
### agent.py
- The main bulk of the program. This is where the agent(s) decide their card choices.
- The training function is found here
### card.py
- Card object
### decks.py
- Deck object
### game.py
- Game loop is found here
### main.py
- Starts the program when called with sufficient arguments
### tournamentSim.py
- Simulation of tournament between agents


# Important Note
When running *main.py*, the WikiText Corpus (~750MB) will be downloaded in *~/.cache/huggingface/datasets/wikitext* **unless** the corpus is included in *src/corpora*, which will only be included when submitting the final implementation.

Please expect to download ~750MB worth of data when running the program if the corpus is not included.

Once the model is trained, *a2a.wordvectors* and *a2a.wordvectors.vectors.npy* will ***appear in the same location your terminal is currently focused in***. If this exists, running the program will use the trained model vectors, meaning it will not run as long as the first time.

If you would like to retrain the model, delete both *a2a.wordvectors* and *a2a.wordvectors.vectors.npy*, and if you would also like to change the training corpus or play with model training variables, please modify the code in *src/agent.py* in the *train_model()* function.

*Approximate training time is around 45 - 60 minutes **at most** (tested on student server)*
