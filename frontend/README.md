# Cyber Risk Underwriting Workbench — Frontend

Static HTML/CSS/JavaScript frontend for the capstone prototype.

## Run

Start the FastAPI backend first:

```bash
uvicorn backend.app.main:app --reload
```

Then serve this folder with any static HTTP server, for example:

```bash
python -m http.server 5500 --directory frontend
```

Open `http://127.0.0.1:5500`.

The frontend calls:

`POST http://127.0.0.1:8000/api/v1/assessments`

The "Generate AI analysis" control currently provides a deterministic prototype narrative. It is intentionally not presented as an LLM-generated result until the AI service is added.
