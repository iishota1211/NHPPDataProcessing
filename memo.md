# things to refactor

- convert test data and train data into several classes
  - inspect the structure of culFormatedData 
  - find out which scripts generate the data
- change the specifications for dataset path
  - configurations can be modified inside the main script
  - use .env to set the default config
- create multiple classes 
  - separate dataset by dataType (group data and time data)
  - create base intensity model class
  - create process wise and type wise mean value classes




structure of dataDictionary (dataLoader.py)
```json
{
  "dataType":{
    "predInterval": {
      "datasetName": {
        "culTrainData",
        "culTestData",
        "culFormatedTrainData",
        "culFormatedTestData"
      }
    }
  }
}
```

dataType = ["time","group"]\
predInterval : list (float)\
datasetName : dict()\
culTrainData : list (float)\
culTestData : list (float)\
culFormatedTrainData : list (tuple)\
culFormatedTestData : list (tuple)

The most simple way to operate data is to split data dictionary by data type.\
But, I should also consider that whether I need specific or different functions 
to process train data and test data.\
If so, dividing train data and test data in different classes is one of the option.

# relation of scripts


