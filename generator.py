from faker import Faker
import random
import math
import pandas as pd
import numpy as np
import calendar
import datetime
from dateutil.relativedelta import relativedelta
import csv
import json

# fake = Faker()


def randomPick(df, column, fake):
    # Returns a random value from a column/list
    if isinstance(df, pd.DataFrame):
        return df.iloc[fake.pyint(0, len(df)-1)][column] 
    else:
        return df[fake.pyint(0, len(df)-1)][column]
    
def correspondingValue(df, lookupCol, lookupVal, returnCol):
    # xlookup with dfs and lists
    if isinstance(df, pd.DataFrame):
        return df[df[lookupCol]==lookupVal][returnCol].to_string(index=False)
    else:
        for i in df:
            if i[lookupCol]==lookupVal:
                return i[returnCol]

def export_json(filename, data):
  with open(filename, 'w+', encoding='utf-8') as ofile:
      json.dump(data, ofile, indent=2, default=str)

def generate_patients(fake, export=True):
  patients = [{
    'mrn': 900000000 + fake.unique.pyint(11111,99999), 
    'first_name': fake.first_name(), 
    'last_name': fake.last_name()
    } for _ in range(9587)]

  if export:
    export_json('data/patients.json', patients)

  return patients

def generate_auditors(fake, export=True):
    auditors = [{
      'auditor_id': 2000000 + fake.unique.pyint(11111,99999),
      'auditor_name': fake.first_name() + ' ' + fake.last_name(), 
      } for _ in range(8)]
    
    if export:
      export_json('data/auditors.json', auditors)

    return auditors

def generate_facilities(fake, export=True):
    dlids = [fake.unique.pyint(1000, 9999) for _ in range(254)]
    facilities = []
    for dlid in dlids:
        facilities.append({
          'global_id': 100000 + dlid,
          'dl_id': dlid,
          'dl_name': fake.unique.city(),
          'mac': random.choice(['NOVITAS', 'NORIDIAN', 'PALMETTO']),
          "npi": 1000000000 + dlid,
          "revenue_center": random.choice(['NORTH', 'SOUTH', 'EAST', 'WEST']),
        })

    if export:
        export_json('data/facilities.json', facilities)
    
    return facilities

def generate_claims(facilities, patients, fake, total_size=10000, export=True):
    claims = []
    adr_id = total_size*100 + fake.unique.pyint(1,total_size*10),
    while len(claims) < total_size:
        ## Generate a random set of ~30 claims with the same facility
        nClaims = round(np.random.normal(30, 1.5))
        facility = randomPick(facilities, 'global_id', fake)
        # patient = randomPick(patients, 'mrn', fake)
        notification_date = fake.date_between(
            start_date=datetime.date.today() - relativedelta(months=36),
            end_date=datetime.date.today() + relativedelta(months=2)
        )
        s = np.random.poisson(2, 1)
        month = notification_date - relativedelta(months=s)
        
        ## 
        for _ in range(0, nClaims):
            claims.append({
                # 'id': adr_id, ## Added afterward
                'notification_date': notification_date,
                'from_date': month.replace(day=1),
                'to_date': month.replace(day= calendar.monthrange(month.year, month.month)[1]),
                'expected_reimbursement': round(np.random.normal(3000, 244), 2),
                # 'mrn': patient, ## Add unique patient
                'global_id': facility,
                'active': False if np.random.binomial(1, 0.2) == 0 else True,
                 # 'mcr_status': 'denied', ## Let's impute this from the end
            })

    # Generate a unique ID for each claim
    for claim in claims:
        zeroes = math.floor(math.log(1040, 10))
        patient = randomPick(patients, 'mrn', fake)
        
        claim['adr_id'] = pow(10, zeroes+1) + fake.unique.pyint(1, total_size*10)
        claim['mrn'] = patient
        
    # Export data
    if export:
        export_json('data/claims.json', claims)
        
    # Return data
    return claims

################################ 45 GENERATORS ################################
    
def generate_45_stages(claims, stages, submissions, decisions):
    # 45: For each claim, generate a Stage
    nStages = len(stages)
    for c, claim in enumerate(claims):
        due_date = claim['notification_date'] + relativedelta(days=45)
    #     submitted = True if datetime.date.today()>=due_date else False
    #     decided = True if submitted<=datetime.date.today()-relativedelta(days=30) else False
    #     active = True if decided else False
        stages.append({
            'adr_id': claim['adr_id'],
            'stage_id': nStages + c,
            'stage': '45',
            'notification_date': claim['notification_date'],
            'due_date': due_date,
        })
        
def generate_45_submissions(claims, stages, submissions, decisions, auditors, fake):
    # 45 For each Stage, generate a Submission
    nSubmissions = len(submissions)
    for s, stage in enumerate(stages):
        if stage['stage'] == '45':
    #         print(stage['due_date'], stage['due_date']>datetime.date.today())
            if stage['due_date'] <= datetime.date.today():
                submission_date = stage['due_date'] - relativedelta(days=fake.pyint(1, 10))
                submissions.append({
                    'adr_id': stage['adr_id'],
                    'stage_id': stage['stage_id'],
                    'stage': '45',
                    'submission_id': nSubmissions + s,
                    'submission_date': submission_date,
                    'auditor_id': randomPick(auditors, 'auditor_id', fake)
                })

def generate_45_decisions(claims, stages, submissions, decisions, fake, paid_rate = 0.9, part_rate = 0.3):
    # 45: For each Submission, generate a Decision
    nDecisions = len(decisions)
    for s, submission in enumerate(submissions):
        # If submission was over 30 days ago
        if submission['submission_date'] <= datetime.date.today()-relativedelta(days=30):
            # Generate random decision
            if random.random() <= paid_rate:
                decision = 'PAID IN FULL'
            elif random.random() <= part_rate:
                decision = 'PARTIALLY DENIED'
            else:
                decision = 'DENIED'

            decisions.append({
                'adr_id': submission['adr_id'],
                'stage_id': submission['stage_id'],
                'stage': '45',
                'submission_id': submission['stage_id'],
                'decision_id': nDecisions + s,
                'decision': decision,
                'decision_date': submission['submission_date'] + relativedelta(days=15+fake.pyint(-2, 2))
            })

################################ 120 GENERATORS ################################

def generate_120_stages(claims, stages, submissions, decisions):
    # For each 45 non-PAID IN FULL decision, generate a 120 stage
    denied = list(filter( lambda x: x['decision']!='PAID IN FULL' and x['stage']=='45', decisions ))
    nStages = len(stages)
    for d, decision in enumerate(denied):
        stages.append({
            'adr_id': decision['adr_id'],
            'stage_id': nStages + d,
            'stage': '120',
            'notification_date': decision['decision_date'],
            'due_date': decision['decision_date'] + relativedelta(days=120),
        })
        
def generate_120_submissions(claims, stages, submissions, decisions, auditors, fake):
    # 120 For each Stage, generate a Submission
    nSubmissions = len(submissions)
    for s, stage in enumerate(stages):
        if stage['stage'] == '120':
            if stage['due_date'] <= datetime.date.today():
                submission_date = stage['due_date'] - relativedelta(days=fake.pyint(1, 10))
                submissions.append({
                    'adr_id': stage['adr_id'],
                    'stage_id': stage['stage_id'],
                    'stage': '120',
                    'submission_id': nSubmissions + s,
                    'submission_date': submission_date,
                    'auditor_id': randomPick(auditors, 'auditor_id', fake)
                })

def generate_120_decisions(claims, stages, submissions, decisions, fake, paid_rate = 0.9, part_rate = 0.3):
    # 120: For each Submission, generate a Decision
    nDecisions = len(decisions)
    for s, submission in enumerate(submissions):
        if submission['stage']=='120':
            # If submission was over 30 days ago
            if submission['submission_date'] <= datetime.date.today()-relativedelta(days=30):
                # Generate random decision
                if random.random() <= paid_rate:
                    decision = 'PAID IN FULL'
                elif random.random() <= part_rate:
                    decision = 'PARTIALLY DENIED'
                else:
                    decision = 'DENIED'

                decisions.append({
                    'adr_id': submission['adr_id'],
                    'stage_id': submission['stage_id'],
                    'stage': '120',
                    'submission_id': submission['stage_id'],
                    'decision_id': nDecisions + s,
                    'decision': decision,
                    'decision_date': submission['submission_date'] + relativedelta(days=15+fake.pyint(-2, 2))
                })


################################ 180 GENERATORS ################################

def generate_180_stages(claims, stages, submissions, decisions):
    # 180
    denied = list(filter( lambda x: x['decision']!='PAID IN FULL' and x['stage']=='120', decisions ))
    nStages = len(stages)
    for d, decision in enumerate(denied):
        stages.append({
            'adr_id': decision['adr_id'],
            'stage_id': nStages + d,
            'stage': '180',
            'notification_date': decision['decision_date'],
            'due_date': decision['decision_date'] + relativedelta(days=180),
        })
        
def generate_180_submissions(claims, stages, submissions, decisions, auditors, fake):
    # 180
    nSubmissions = len(submissions)
    for s, stage in enumerate(stages):
        if stage['stage'] == '180':
            if stage['due_date'] <= datetime.date.today():
                submission_date = stage['due_date'] - relativedelta(days=fake.pyint(1, 10))
                submissions.append({
                    'adr_id': stage['adr_id'],
                    'stage_id': stage['stage_id'],
                    'stage': '180',
                    'submission_id': nSubmissions + s,
                    'submission_date': submission_date,
                    'auditor_id': randomPick(auditors, 'auditor_id', fake)
                })
                
def generate_180_decisions(claims, stages, submissions, decisions, fake, paid_rate = 0.1, part_rate = 0.9):
    # 180
    nDecisions = len(decisions)
    for s, submission in enumerate(submissions):
        if submission['stage']=='180':
            # If submission was over 30 days ago
            if submission['submission_date'] <= datetime.date.today()-relativedelta(days=30):
                # Generate random decision
                if random.random() <= paid_rate:
                    decision = 'PAID IN FULL'
                elif random.random() <= part_rate:
                    decision = 'PARTIALLY DENIED'
                else:
                    decision = 'DENIED'

                decisions.append({
                    'adr_id': submission['adr_id'],
                    'stage_id': submission['stage_id'],
                    'stage': '180',
                    'submission_id': submission['stage_id'],
                    'decision_id': nDecisions + s,
                    'decision': decision,
                    'decision_date': submission['submission_date'] + relativedelta(days=15+fake.pyint(-2, 2))
                })




def generate_data(export=True):
  fake = Faker()
    
  # Generate supplemental data
  patients = generate_patients(fake, export=False)
  facilities = generate_facilities(fake, export=False)
  auditors = generate_auditors(fake, export=False)


  # Generate main data
  claims = generate_claims(facilities, patients, fake, export=False)
  stages = []
  submissions = []
  decisions = []

  generate_45_stages(claims, stages, submissions, decisions)
  generate_45_submissions(claims, stages, submissions, decisions, auditors, fake)
  generate_45_decisions(claims, stages, submissions, decisions, fake, paid_rate = 0.9, part_rate = 0.3)

  generate_120_stages(claims, stages, submissions, decisions)
  generate_120_submissions(claims, stages, submissions, decisions, auditors, fake)
  generate_120_decisions(claims, stages, submissions, decisions, fake, paid_rate = 0.2, part_rate = 0.3)

  generate_180_stages(claims, stages, submissions, decisions)
  generate_180_submissions(claims, stages, submissions, decisions, auditors, fake)
  generate_180_decisions(claims, stages, submissions, decisions, fake, paid_rate = 0.8, part_rate = 0.8)

  if export:
    # Export Main Data
    export_json('data/claims.json', claims)
    export_json('data/stages.json', stages)
    export_json('data/submissions.json', submissions)
    export_json('data/decisions.json', decisions)

    # Export Supplemental Data
    export_json('data/patients.json', patients)
    export_json('data/facilities.json', facilities)
    export_json('data/auditors.json', auditors)

  return {
      'claims'      : claims,
      'stages'      : stages,
      'submissions' : submissions,
      'decisions'   : decisions,
      'patients'    : patients,
      'facilities'  : facilities,
      'auditors'    : auditors,
  }


if __name__ == "__main__":
  generate_data(export=True)













