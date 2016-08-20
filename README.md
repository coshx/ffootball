## Getting Started
### Serve up the Frontend

### Setup the Backend Data Service

1. Clone this repo using `git clone https://github.com/coshx/ffootball.git`.
1. Build the Anaconda environment.
  * Install [Anaconda](http://conda.pydata.org/docs/installation.html). If you would like a lighter installation, follow the instructions to install [Miniconda](http://conda.pydata.org/docs/install/quick.html) instead.
  * `cd` into the application root, `./ffootball/`
  * Use `conda env create -f ./ffootball.yml` to install the Python dependencies for the backend. This will create a `conda` environment called `ffootball`.
  * Activate the `stocks` environment using `source activate ffootball` on Linux/OS X or `activate ffootball` on Windows. You can deactivate the conda environment using `source deactivate` on Linux/OS X or `deactivate` on Windows.
1. With the `ffootball` environment activated, run `python backend.py` from `./ffootball/backend`.
1. Navigate to [http://localhost:8000](http://localhost:8000) to verify that you see the "Success!" message.
  * By default, the server runs on port 8000, you can specify the port by including a command line flag: `python app.py --port=5678`.
