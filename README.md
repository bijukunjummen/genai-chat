## Chat application using Streamlit and Vertex AI Text Bison

### Get python env with right deps pulled in

Create a new virtual environment, and pull in the dependencies
```shell
python3 -m venv ~/pythonenvs/streamlit-genai
source ~/pythonenvs/streamlit-genai/bin/activate
pip install poetry

poetry install
```

Set the OpenAI key:
```sh
export OPENAI_API_KEY=<mykey>
```

### Start the application

```sh
poetry run streamlit run app.py
```
