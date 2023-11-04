from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.utils.main_utils import read_yaml_file, write_yaml_file
from sensor.entity.config_entity import DataValidationConfig
from sensor.exception import SensorException
from sensor.logger import logging
import pandas as pd
import sys, os
from scipy.stats import ks_2samp


class DataValidation:

    def __init__(self, data_ingestion_artifact:DataIngestionArtifact, data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e,sys)
    
    def validate_number_of_columns(self, dataframe:pd.DataFrame)->bool:
        """
        Validates if all columns are present in data
        """
        try:
            number_of_columns = len(self._schema_config['columns']) 
            if len(dataframe.columns)==number_of_columns:
                return True
            logging.info(f"number of columns in schema: {number_of_columns}")
            logging.info(f"number of columns in dataframe: {len(dataframe.columns)}")
            return False
        except Exception as e:
            raise SensorException(e, sys)

    def is_numerical_column_exist(self, dataframe:pd.DataFrame)->bool:
        """
        Validates if all numerical columns are present or not
        """
        try:
            numerical_columns = self._schema_config['numerical_columns']
            dataframe_columns = list(dataframe.columns)

            numerical_column_present = True
            missing_numerical_cols = []
            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_column_present=False
                    missing_numerical_cols.append(num_column)
            logging.info(f"Missing numerical columns: {missing_numerical_cols}")
            return numerical_column_present
        except Exception as e:
            raise SensorException(e, sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        """
        Static method that reads data from csv file and returns DataFrame
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys)

    def detect_dataset_drift(self, base_df, current_df, threshold=0.05)->bool:
        """
        Checks if train and test data follows same distribution or not
        """
        try:
            status=True
            report ={}
            for column in base_df.columns:
                d1 = base_df[column]
                d2  = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found = True 
                    status=False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                    
                    }})
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            
            #Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)
            return status
        except Exception as e:
            raise SensorException(e,sys)

    def initiate_data_validation(self)->DataValidationArtifact:
        """
        Starts data validation component
        """
        try:
            error_message = ""
            # Get train test file locations
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            # Read data into train test dataframes
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            # Validate number of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message}Train Dataframe Does not contain all columns"

            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message}Test Dataframe Does not contain all columns"

            # Validate number of numerical columns
            status = self.is_numerical_column_exist(train_dataframe)
            if not status:
                error_message = f"{error_message}Train Dataframe doesn't have all columns"

            status = self.is_numerical_column_exist(test_dataframe)
            if not status:
                error_message = f"{error_message}Test Dataframe doesn't have all columns"

            if len(error_message) > 0 :
                raise Exception(error_message)
            
            logging.info("Data Validation Checks completed")
            
            # Check data drift
            logging.info("Checking data drift")
            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
                
            logging.info(f"Data validation artifact:{data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)