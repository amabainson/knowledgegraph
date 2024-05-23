import pandas as pd
import json
import os


class CTA_Evaluator:
  def __init__(self):
      pass

  def _evaluate(self, system_file, gt_file):

    cols, col_type = set(), dict()
    gt = pd.read_csv(gt_file, delimiter=',', names=['tab_id', 'col_id', 'type'],
                     dtype={'tab_id': str, 'col_id': str, 'type': str}, keep_default_na=False)

    for index, row in gt.iterrows():
        col = '%s %s' % (row['tab_id'], row['col_id'])
        gt_type = row['type']
        col_type[col] = gt_type
        cols.add(col)

    annotated_cols = set()
    TP = 0
    valid_annotations = 0
    sub = pd.read_csv(system_file, delimiter=',', names=['tab_id', 'col_id', 'annotation'],
                      dtype={'tab_id': str, 'col_id': str, 'annotation': str}, keep_default_na=False)
    for index, row in sub.iterrows():
        col = '%s %s' % (row['tab_id'], row['col_id'])
        if col in annotated_cols:
            # continue
            raise Exception("Duplicate columns in the submission file")
        else:
            annotated_cols.add(col)
        annotation = row['annotation']
        
        #if not (annotation.startswith('http://dbpedia.org/ontology/') or annotation.startswith('http://www.w3.org/2002/07/owl#')):
        #    if annotation == 'thing' or annotation == 'Thing':
        #        annotation = 'http://www.w3.org/2002/07/owl#Thing'
        #    elif not annotation == 'nil':
        #        annotation = 'http://dbpedia.org/ontology/' + annotation

        if col in cols:
            valid_annotations += 1
            gt = col_type[col]
            if gt.lower() == annotation.lower():
                TP = TP + 1

    precision = TP / valid_annotations if valid_annotations > 0 else 0
    recall = TP / len(cols)
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    main_score = f1
    secondary_score = precision

    print('%.3f %.3f %.3f' % (f1, precision, recall))

    _result_object = {
        "score": main_score,
        "score_secondary": secondary_score
    }
    return _result_object


if __name__ == "__main__":
    dir_gt = 'sem-tab-evaluator/gt'
    dir_output = 'sem-tab-evaluator/system_example'

    #read files and evaluate against the GT 
    for gt_file in os.listdir(dir_gt):
        if gt_file.endswith("_cta_gt.csv"):
            system_file = os.path.join(dir_output, gt_file.replace("_cta_gt.csv", "_cta_output.csv"))
            print(f"Evaluating: {gt_file} and {os.path.basename(system_file)}")
            if os.path.exists(system_file):
                evaluator = CTA_Evaluator()   # Instantiate an evaluator
                result = evaluator._evaluate(system_file, os.path.join(dir_gt, gt_file))#Evaluate
                print(result)
            else:
                print(f"System file {system_file} not found.")
    #gt_file = "gt/CWI64CIY_cta_gt.csv"
    #system_file = "system_example/CWI64CIY_cta_output.csv"
    
    # Instantiate an evaluator
    #evaluator = CTA_Evaluator()
    # Evaluate
    #result = evaluator._evaluate(system_file, gt_file)
    #print(result)
