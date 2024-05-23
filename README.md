
# Solution to Option A: Tabular Data to KG Matching Exercise

This repository provides the solution to the "Tabular Data to KG Matching Exercise". The `world_data.py` script is used to implement Tasks A.1 to A.3. 

## Running the Scripts

### Tasks A.1 to A.3

To run the script for Tasks A.1 to A.3, use the following commands:

```bash
cd lab-session3
python3 world_data.py
```

### Output

The output csv is in the `data` folder and contains the following columns:
- Source table
- Isub similarity score
- Place (city/country)
- Predicted type provided by the ontology 
- Actual type
- URI

### Task A.4

To annotate the given tabular data as required in Task A.4, run the following command:

```bash
python3 CEA_Annotator.py
```

The script outputs the results as CSV files in the `sem-tab-evaluator/system_example` directory.

### Output

Each output file will contain the following columns:
- Source table
- Row id
- Column id
- URI

## Evaluating the Results

To evaluate the results against the ground truth, run the following command:

```bash
python3 sem-tab-evaluator/CEA_Evaluator.py
```

## Directory Structure

```
lab-session3/
  ├── world_data.py
  ├── CEA_Annotator.py
  └── sem-tab-evaluator/
        ├── system_example/
        └── CEA_Evaluator.py
```

## Summary

- **Task A.1 to A.3**: Implemented in `world_data.py`.
- **Task A.4**: Annotation done using `CEA_Annotator.py`.
- **Evaluation**: Performed using `CEA_Evaluator.py`.

---

