# Airflow – Local Instance (Docker Compose)

This repository provides a ready-to-use **Apache Airflow** instance for **local usage** with **Docker Compose**.

## 🗂️ Project Structure

```text
airflow-demo-instance/
├── .env                  # Environment variables (UID, GID, Compose options, etc.)
├── Dockerfile            # Custom Airflow image build (optional)
├── compose.yml           # Main Docker Compose stack
├── compose.override.yml  # Local overrides (ports, extra mounts, etc.)
├── requirements.txt      # Additional Python dependencies installed at startup
├── dags/                 # Your Airflow DAGs (.py files go here)
├── plugins/              # Airflow plugins (custom operators/hooks/providers)
├── logs/                 # Airflow logs (mounted as a volume for persistence)
├── config/               # Airflow configs (default airflow.cfg)
├── data/                 # Data/artifacts used by DAGs (mounted inside containers)
└── run-airflow.sh        # Launch script
```

## 🚀 Quick Start

Prerequisites:

- Docker (Engine) + Docker Compose (either the `docker compose` plugin or `docker-compose` binary)
- Linux/macOS/WSL2
- Run Airflow

```bash
./run-airflow.sh
```

The script:

- initializes `AIRFLOW_UID` and `AIRFLOW_GID` with your current user/group IDs,
- performs a `pull`/`build` if needed,
- starts the services in detached mode (`up -d`),
- shows the status and reminds you of useful commands.

- stop Airflow

```bash
./stop-airflow.sh
```

### Web Access

Once running, the Airflow web interface is usually available at:

- <http://localhost:8080>

(The exact port depends on your `compose.yml`.)

## ⚙️ Decoder processing chain with Airflow

The decoder tasks rely on the MATLAB Runtime.
With this local Airflow setup, you can run the processing chain in **two different modes** depending on how the MATLAB Runtime is made available:

### 1. MATLAB Runtime available on the host

If MATLAB Runtime is already installed locally on your machine, Airflow can directly access it through a **bind mount** from the host into the Airflow containers.  
In this case, the `compose.override.yml` mounts the host path (e.g. `/opt/matlab/runtime`) into `/opt/matlab/runtime` inside the containers.

To launch in this mode, simply run:

```bash
./run-airflow-local-matlab.sh /absolute-path-to/matlab-runtime
```

### Decoder Web Access

Once running, the Airflow decoder DAG is usually available at:

- <http://localhost:8080/dags/argo-decoder-data-processing-chain>

Trigger it to run the decoder on a demonstration Dataset (one cycle of float `6904182`)

### 2. MATLAB Runtime provided by a dedicated container

/!\ The Docker image containing MATLAB is 15 GB /!\

If MATLAB Runtime is **not available on the host**, an additional container can be started.  
This container embeds the official MATLAB Runtime image and exposes it through a Docker volume.  
Airflow services then reuse this volume, so the DAGs see exactly the same path (`/opt/matlab/runtime`) as in the host-based mode.

To launch in this mode, use:

```bash
./run-airflow-external-matlab.sh
```

This script enables the `runtime-matlab` service, which pulls the MATLAB Runtime container image and makes it accessible to Airflow.

---

### DAG usage

From the point of view of your Airflow DAGs, there is **no difference** between the two modes:  
the runtime is always mounted at `/opt/matlab/runtime`.  
This means the same DAG code works whether you rely on MATLAB installed locally or on the containerized runtime.

---

👉 **Summary:**

- Use `./run-airflow-local-matlab.sh` if MATLAB Runtime is installed on your host.
- Use `run-airflow-matlab.sh` if you don't have MATLAB Runtime this will run in background in a container.
- In both cases, your DAGs remain unchanged.

## 🔧 Useful Commands

Depending on your environment, replace `docker compose` with `docker-compose` if needed.

```bash
# Check services
docker compose ps

# Follow logs
docker compose logs -f

# Restart after modifications
docker compose up -d --build

# Stop services (keep volumes)
docker compose down

# Stop AND remove volumes (⚠️ deletes Airflow metadata)
docker compose down -v
```

## ❓ Troubleshooting (FAQ)

- **Permission denied on logs or Airflow home**  
  Ensure `AIRFLOW_UID`/`AIRFLOW_GID` match your current user. Re-run `./run-airflow.sh`.

- **`docker: command not found` or Compose not found**  
  Install Docker and the Compose plugin (or the `docker-compose` binary), then try again.

- **Port 8080 already in use**  
  Change the port mapping in `compose.override.yml`.

---

Happy flying ✈️ with Airflow!
