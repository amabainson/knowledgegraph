# Solution to Option A: Tabular Data to KG Matching Exercise

Based on the provided context, this repository provides the solution to the "Tabular Data to KG Matching Exercise". The `world_data.py` script is used to implement Tasks A.1 to A.3. To run it,

```
cd lab-session3
python3 world_data.py
```

Its output contains the columns dataset name, the isub similarity score, place(city/column), the predicted type (as requested in Task A.3), its actual type and finally the URI.

Using this system, the given tabular data were annotated as required in Task A.4. To perform the annotation, run the following command:

```
python3 CEA_Annotator.py
```

The script outputs the results as csv files in the `sem-tab-evaluator/system_example` directory. To evaluate the results again the ground truth, run the following command:

```
python3 sem-tab-evaluator/CEA_Evaluator.py
```

