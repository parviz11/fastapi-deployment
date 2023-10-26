import os
import logging
import json
import numpy
import pandas as pd
import joblib
from pathlib import Path


def init():
    
    #Parent path
    BASE_DIR = Path(__file__).resolve(strict=True).parent
    
    #Open the model from pickle file
    with open(f"{BASE_DIR}/lg_pipeline.pkl", "rb") as f:
        model = pickle.load(f)
    
    logging.debug("Init complete")

'''
data_types = {'uuid': 'object',
 'default': 'float64',
 'account_amount_added_12_24m': 'int64',
 'account_days_in_dc_12_24m': 'float64',
 'account_days_in_rem_12_24m': 'float64',
 'account_days_in_term_12_24m': 'float64',
 'account_incoming_debt_vs_paid_0_24m': 'float64',
 'account_status': 'float64',
 'account_worst_status_0_3m': 'float64',
 'account_worst_status_12_24m': 'float64',
 'account_worst_status_3_6m': 'float64',
 'account_worst_status_6_12m': 'float64',
 'age': 'int64',
 'avg_payment_span_0_12m': 'float64',
 'avg_payment_span_0_3m': 'float64',
 'merchant_category': 'object',
 'merchant_group': 'object',
 'has_paid': 'bool',
 'max_paid_inv_0_12m': 'float64',
 'max_paid_inv_0_24m': 'float64',
 'name_in_email': 'object',
 'num_active_div_by_paid_inv_0_12m': 'float64',
 'num_active_inv': 'int64',
 'num_arch_dc_0_12m': 'int64',
 'num_arch_dc_12_24m': 'int64',
 'num_arch_ok_0_12m': 'int64',
 'num_arch_ok_12_24m': 'int64',
 'num_arch_rem_0_12m': 'int64',
 'num_arch_written_off_0_12m': 'float64',
 'num_arch_written_off_12_24m': 'float64',
 'num_unpaid_bills': 'int64',
 'status_last_archived_0_24m': 'int64',
 'status_2nd_last_archived_0_24m': 'int64',
 'status_3rd_last_archived_0_24m': 'int64',
 'status_max_archived_0_6_months': 'int64',
 'status_max_archived_0_12_months': 'int64',
 'status_max_archived_0_24_months': 'int64',
 'recovery_debt': 'int64',
 'sum_capital_paid_account_0_12m': 'int64',
 'sum_capital_paid_account_12_24m': 'int64',
 'sum_paid_inv_0_12m': 'int64',
 'time_hours': 'float64',
 'worst_status_active_inv': 'float64'}

'''


def run(raw_data):
    """
    This function is called for every invocation of the endpoint to perform the actual scoring/prediction.
    In the example we extract the data from the json input and call the scikit-learn model's predict()
    method and return the result back
    """
    logging.info("model: request received")
    data1 = json.loads(json.loads(raw_data)["data"][0])
    #data = numpy.array(data)

    columns = [key for key,val in data1.items()]
    vals = [[val] for key,val in data1.items()]
    
    for i in range(len(vals)):
        if vals[i] == [None]:
            vals[i] = [numpy.nan]

    data = pd.DataFrame(numpy.array(vals).T,columns=columns)
    data = data.astype(data_types)

    result = model.predict_proba(data)
    logging.info("Request processed")
    return result.tolist()