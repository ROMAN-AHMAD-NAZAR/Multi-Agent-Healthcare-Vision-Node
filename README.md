# 🧠 Vision Agent Node: 2.5D Dual-Stream Brain Tumor Detection

## 📌 Project Overview
This repository contains a specialized **Computer Vision Agent** designed to function as a node within a larger Multi-Agent System. Unlike standard 2D CNNs, this system utilizes a **2.5D Attention Mechanism** processing MRI slices as pseudo-volumetric data to detect brain tumors with high confidence.

The system is encapsulated as a callable agent (`Vision Agent Node`) that returns structured JSON payloads, making it ready for integration with LLM Orchestrators (e.g., LangChain, AutoGen).

## 🚀 Key Features
* **2.5D Slicer Logic**: Converts sequential MRI slices into 3-channel depth volumes to capture spatial context.
* **Dual-Stream Architecture**:
    * *Stream A*: U-Net Lite for precise segmentation
    * *Stream B*: CNN classifier for tumor detection
* **Explainable AI (XAI)**: Integrated Grad-CAM and Saliency Maps for every diagnosis.
* **Test-Time Augmentation (TTA)**: Stability scoring via prediction variance analysis.
* **Agent API**: A discrete `run_vision_agent()` function that outputs JSON for downstream agents.

## 📂 Repository Structure
```text
├── Vision_Agent_2.5D_Attention.ipynb   # Main Agent Logic & Training
├── requirements.txt                    # Dependencies
├── .gitignore                          # Excludes data/model files
└── README.md                           # Documentation
```

## ⚙️ Setup & Usage

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Data Setup

*Note: The dataset is not included due to size constraints.*

1. Create a folder named `data` in the root directory.
2. Download datasets from Kaggle:
   - [LGG MRI Segmentation](https://www.kaggle.com/datasets/mateuszbuda/lgg-mri-segmentation)
   - [BraTS 2021](https://www.kaggle.com/datasets/dschettler8845/brats-2021-task1)
3. Place in the following structure:
```text
data/
├── lgg-mri-segmentation/
│   └── kaggle_3m/
└── brats-2021-task1/
    └── BraTS2021_Training_Data.tar
```

### 3. Running the Agent

Open the Jupyter Notebook. The final cell exposes the API:

```python
# Example Usage of the Agent Node
response_payload = run_vision_agent("./data/test/tumor_sample_01.jpg")

print(response_payload)
# Output:
# {
#   "agent_id": "vision_expert_01",
#   "agent_type": "2.5D_Attention_UNet",
#   "diagnosis": "Tumor Detected",
#   "confidence_score": 0.9234,
#   "stability_check": "PASSED",
#   "stability_score": 0.9812,
#   "tumor_size_cm": 2.45,
#   "explanation_path": "./outputs/gradcam_heatmap.png",
#   "model_version": "v1.0.0"
# }
```

## 🧠 Model Architecture

The model uses a custom **Dual-Stream Network**:

1. **Ingestion**: 3 consecutive slices (N-1, N, N+1) for 2.5D context
2. **Stream A (Segmentation)**: U-Net Lite with skip connections
3. **Stream B (Classification)**: CNN with Global Average Pooling
4. **Output**: Dual heads for segmentation mask + tumor probability

### Inference Pipeline
```
Input MRI → 2.5D Preprocessing → Dual-Stream Model → TTA Stability Check → JSON Output
```

## 📊 Agent Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `agent_id` | string | Unique identifier for this vision node |
| `agent_type` | string | Model architecture identifier |
| `diagnosis` | string | Classification result |
| `confidence_score` | float | Model confidence (0-1) |
| `stability_check` | string | PASSED/FAILED based on TTA variance |
| `stability_score` | float | Prediction consistency score |
| `tumor_size_cm` | float | Estimated tumor diameter (RECIST) |
| `explanation_path` | string | Path to Grad-CAM visualization |

## 🔗 Multi-Agent Integration

This Vision Agent is designed to communicate with:
- **Validation Agent**: Cross-references diagnosis with medical knowledge graphs (Neo4j)
- **Report Generator**: Produces clinical summaries from structured outputs
- **Orchestrator**: LLM-based coordinator for multi-modal analysis

---

**Author:** Roman  
**Context:** Multi-Agent Medical Diagnosis System Research
