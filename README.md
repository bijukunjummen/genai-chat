## Chat application using Streamlit and Vertex AI Text Bison

### Get python env with right deps pulled in

Create a new virtual environment, and pull in the dependencies
```shell
python3 -m venv ~/pythonenvs/streamlit-genai
source ~/pythonenvs/streamlit-genai/bin/activate
pip install -r requirements.txt
```

### Connect to the right project in GCP

The instructions are here - https://cloud.google.com/sdk/gcloud/reference/auth/application-default

### Start the application

```sh
streamlit run app.py
```
