# gentar_distribution_id_updater
gentar_distribution_id_updater is a Python application designed to facilitate the process of adding RRIDs to the distribution tables in a GenTaR database using an API. 
The application allows users to download it from GitHub and run it locally

This project was written using python 3.9.0
and has been tested on OSX

## 1. Check your python installation:

```
python --version
or
python3 --version
```

## 2. Create a virtual environment for the project (requires Python 3.4+)

```
cd <name_of_cloned_github_repository>
python -m venv venv
or
python3 -m venv venv
```

## 3. To begin using the virtual environment, it needs to be activated:

```
source venv/bin/activate
```

## 4. Install the packages required for the project

```
pip install -r requirements.txt
```
---
## 5. Prepare to run the program.

### A) Export environment variable with your user credential.
```
export GENTAR_USER=<username>
export GENTAR_PASSWORD=<gentar_password>
```
### B) Specify the service to update.
```
export GENTAR_ENV=SANDBOX
```
Note: You can use the <a href="https://www.gentar.org/production-tracker-sandbox/#/">SANDBOX</a> to test the update.
Use "export GENTAR_ENV=PRODUCTION" to update the main service.
## 6. Invoke the program
## For Colony RRId Updater
Users are required to provide a list of colony names and corresponding RRIDs in a tab-separated format.
The primary purpose is to identify the colony ID associated with each colony name, and then use this colony ID to update the distribution table with the new RRID.

### A) Edit the rr_ids.txt file.

Add  colony name and rr ids tab(\t) seperated to be inserted on a separate line and save the file.
RRid has to start with "RRID:" e.g.

```
jr34077\tRRID:MMRRC_048962-UCD
jr34078\tRRID:MMRRC_048963-UCD
```


```
python insert_rrid_by_colony.py
or
python3 insert_rrid_by_colony.py
```
This will produce the following sort of output
```
Processing jr34077\tRRID_MMRRC_048962-UCD
Successfully Updated: jr34077\tRRID_MMRRC_048962-UCD
```
If the distribution cannot be updated  you will only see the line stating that the  404 Client Error In this case, edit the colonies file to correct the name or remove the problematic line and then restart the program.
.If you see 401 Client Error please check your credential.
## For TargRep EsCell RRId Updater
Users are required to provide a list of es cell names,distribution Network Names, start dates, end dates and corresponding RRIDs in a tab-separated format.
The primary purpose is to identify the es cell name, and then use this name to update the distribution table with the new RRID.

### A) Edit the targ_rep_es_cell_rr_ids.txt file.

Add  es cell names ,distribution Network Names, start dates, end dates and rr ids tab(\t) seperated to be inserted on a separate line and save the file.
RRid has to start with "RRID:" e.g.

```
EPD0840_2_E0\tMMRRC\t2022-01-01\t2022-01-01\tRRID:MMRRC_048962-UCDT
```
```
python targ_rep_es_cell_rr_ids.py
or
python3 targ_rep_es_cell_rr_ids.py
```
This will produce the following sort of output
```
Processing ['EPD0840_2_E01', 'MMRRC', '2022-01-01', '2022-01-01', 'RRID:MMRRC_048962-UCDT']
Successfully Updated: ['EPD0840_2_E02', 'MMRRC', '2022-01-01', '2022-01-01', 'RRID:MMRRC_048962-UCDTT']
```

If the distribution  cannot be updated  you will only see the line stating that the  404 Client Error In this case, edit the file to correct the name or remove the problematic line and then restart the program.
.If you see 401 Client Error please check your credential.
## For TargRep Targeting Vector RRId Updater
Users are required to provide a list of targeting vector names,distribution Network Names, start dates, end dates and corresponding RRIDs in a tab-separated format.
The primary purpose is to identify the targeting vector name, and then use this name to update the distribution table with the new RRID.

### A) Edit the targ_rep_targeting_vector_rr_ids.txt file.

Add  targeting vector names,distribution Network Names, start dates and rr ids tab(\t) seperated to be inserted on a separate line and save the file.
and RRid has to start with "RRID:" e.g.

```
PG00174_Z_3_E07\tMMRRC\t2022-01-01\t2022-01-01\tRRID:MMRRC_048962-UCDT
```


```
python targ_rep_targeting_vector_rr_ids.py
or
python3 targ_rep_targeting_vector_rr_ids.py
```
This will produce the following sort of output
```
Processing ['PG00174_Z_3_E07', 'MMRRC', '2022-01-01', '2022-01-01', 'RRID:MMRRC_048962-UCDT']Successfully Updated: jr34077\tRRID_MMRRC_048962-UCD
Successfully Updated: ['PG00174_Z_3_E07', 'MMRRC', '2022-01-01', '2022-01-01', 'RRID:MMRRC_048962-UCDT']

```


If the distribution cannot be updated  you will only see the line stating that the  404 Client Error In this case, edit the colonies file to correct the name or remove the problematic line and then restart the program.
.If you see 401 Client Error please check your credential.
## 7. Once you have finished working in the virtual environment clean up

```
deactivate
```

This puts you back to the system’s default Python interpreter
with all its installed libraries.


