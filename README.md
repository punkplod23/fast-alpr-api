fast-alpr-api
===============

This small FastAPI example runs the `ALPR` detector from `fast-alpr` and exposes a single endpoint to process base64-encoded images.

Docker
------

Build the image (from the project root where this `README.md` lives):

PowerShell (Windows):

```powershell
docker build -t fast-alpr-api .
```

Linux / macOS / WSL / cmd.exe:

```bash
docker build -t fast-alpr-api .
```

Run the container and publish port 80:

PowerShell (Windows):

```powershell
docker run --rm -p 8000:80 --name fast-alpr-api fast-alpr-api
```

Linux / macOS / WSL / cmd.exe:

```bash
docker run --rm -p 8000:80 --name fast-alpr-api fast-alpr-api
```

Then open http://localhost:8000/docs to see the interactive Swagger UI.

Notes
-----
- The container uses Python 3.13 slim and installs the required Python packages directly. If you prefer to install from the local `pyproject.toml`, update the Dockerfile to run `pip install -e .` and ensure a PEP 517 backend is available.
- If your ALPR runtime requires GPU support or additional native libraries, you'll need a different base image and runtime options (nvidia/amd GPU runtimes) and to install the corresponding drivers/toolkit on the host.
