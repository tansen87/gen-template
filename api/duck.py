"""
Description: 使用duckdb来生成模板
usage: 调用window.pywebview.api.<methodname>(<parameters>)从Javascript执行
"""

import os
import time
import json
import traceback
from typing import Union
from datetime import datetime
from parser import ParserError

import duckdb
import webview
import pandas as pd

from src_py.config.log import Log


class Duck:
    """ duck """
    window = None

    def system_py2js(self, func, info) -> None:
        """ 调用js中挂载到window的函数 """
        infoJson = json.dumps(info)
        Duck.window.evaluate_js(f"{func}('{infoJson}')")

    def duck_open_file(self, sep: str, encoding: str) -> None:
        """ 打开文件 """
        file_types = [
            'All files (*.*)',
            'CSV (*.csv;*.txt;*.dat;*.spec;*.tsv)'
        ]
        directory = ''
        try:
            file_types = tuple(file_types)
            self.result = Duck.window.create_file_dialog(
                dialog_type=webview.OPEN_DIALOG, directory=directory, allow_multiple=True, file_types=file_types)
            file_type = os.path.splitext(self.result[0])[1].lower()
            if file_type in ['.csv', '.tsv', '.dat', '.spext', '.txt']:
                check_df = pd.read_csv(self.result[0], dtype=str, encoding=encoding, sep=sep, nrows=10)
            df_json = check_df.to_json(orient='records', force_ascii=False)

            return df_json
        except ParserError as e:
            json_error = json.dumps('文件分割符有误', ensure_ascii=False, indent=2)
            return json_error
        except Exception as e:
            Log.error(repr(e))
            json_error = json.dumps(repr(e), ensure_ascii=False, indent=2)
            return json_error
    
    def duck_create_db(
        self,
        sep: str,
        table: str
    ) -> Union[float, str]:
        """ 将csv文件写入到duckdb中,且所有数据类型为VARCHAR """
        try:
            start_time = time.time()

            file_path = os.path.splitext(self.result[0])[0]
            db_path = f'{file_path}_template.duckdb'
            conn = duckdb.connect(db_path)
            c = conn.cursor()
            c.execute(f'CREATE TABLE {table} AS SELECT * FROM read_csv(\'{self.result[0]}\', all_varchar=true, sep=\'{sep}\')')

            end_time = time.time()
            elapsed_time = round(end_time - start_time, 2)

            return elapsed_time
        except Exception as e:
            error_info = {
                'type': type(e).__name__,
                'message': str(e),
                'traceback': traceback.format_exc()
            }
            Log.error(error_info)
            json_error = json.dumps(repr(e), ensure_ascii=False, indent=2)

            return json_error

    def duck_process(
        self,
        entity: str,
        entity_select: str,
        journal_number: str,
        jn_connect: str,
        journal_type: str,
        date_effective: str,
        date_entered: str,
        date_select: str,
        user_enterd: str,
        user_updated: str,
        user_select: str,
        line_desciption: str,
        amount: str,
        amount_select: str,
        account: str,
        account_description: str,
        currency: str,
        currency_select: str,
        ami: str,
        entity_number: str,
        table: str 
    ) -> Union[float, str]:
        """ 生成模板 """
        try:
            start_time = time.time()

            file_path = os.path.splitext(self.result[0])[0]
            db_path = f'{file_path}_template.duckdb'
            conn = duckdb.connect(db_path)
            c = conn.cursor()

            # rename 'Entity', 'Company Name'
            if entity_select == 'column':
                c.sql(f'ALTER TABLE {table} RENAME COLUMN "{entity}" TO "Entity";')
                c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "Company Name" VARCHAR;')
                c.sql(f'UPDATE {table} SET "Company Name" = "Entity";')
            if entity_select == 'input':
                c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "Entity" VARCHAR;')
                c.sql(f'UPDATE {table} SET "Entity" = \'{entity}\';')
                c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "Company Name" VARCHAR;')
                c.sql(f'UPDATE {table} SET "Company Name" = "Entity";')

            # rename 'Data Effective', 'Date Entered',
            # add 'Finincial Period'
            c.sql(f'ALTER TABLE {table} RENAME COLUMN "{date_effective}" TO "Date Effective";')
            c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "Financial Period" VARCHAR;')
            c.sql(f'UPDATE {table} SET "Financial Period" = MONTH(CAST("Date Effective" AS DATE));')
            if date_select == 'equal':
                c.sql(f'UPDATE {table} SET "Date Effective" = strftime(CAST("Date Effective" AS DATE), \'%d/%m/%Y\');')
                c.sql(f'ALTER TABLE {table} ADD COLUMN "Date Entered" VARCHAR;')
                c.sql(f'UPDATE {table} SET "Date Entered" = "Date Effective";')
            if date_select == 'unequal':
                c.sql(f'ALTER TABLE {table} RENAME COLUMN "{date_entered}" TO "Date Entered";')
                c.sql(f'UPDATE {table} SET "Date Entered" = strftime(CAST("Date Entered" AS DATE), \'%d/%m/%Y\');')

            # rename 'Journal Number'
            if jn_connect == 'yes':
                c.sql(f'ALTER TABLE {table} ADD COLUMN "Journal Number" VARCHAR;')
                c.sql(f'UPDATE {table} SET "Journal Number" = CONCAT("{journal_number}", \'_\', "Date Effective");')
            if jn_connect == 'no':
                c.sql(f'ALTER TABLE {table} RENAME COLUMN "{journal_number}" TO "Journal Number";')

            # rename 'Journal Type'
            if journal_type != '':
                c.sql(f'ALTER TABLE {table} RENAME COLUMN "{journal_type}" TO "Journal Type";')
            
            # rename 'userID Entered', 'userID updated'
            if user_select == 'unequal':
                if user_enterd != '':
                    c.sql(f'ALTER TABLE {table} RENAME COLUMN "{user_enterd}" TO "UserID Entered";')
                    c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "Name of User Entered" VARCHAR;')
                    c.sql(f'UPDATE {table} SET "Name of User Entered" = "UserID Entered";')
                if user_updated != '':
                    c.sql(f'ALTER TABLE {table} RENAME COLUMN "{user_updated}" TO "UserID Updated";')
                    c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "Name of User Updated" VARCHAR;')
                    c.sql(f'UPDATE {table} SET "Name of User Updated" = "UserID Updated";')
            if user_select == 'equal':
                if user_enterd != '' and user_updated == '':
                    c.sql(f'ALTER TABLE {table} RENAME COLUMN "{user_enterd}" TO "UserID Entered";')
                    c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "Name of User Entered" VARCHAR;')
                    c.sql(f'UPDATE {table} SET "Name of User Entered" = "UserID Entered";')
                    c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "UserID Updated" VARCHAR;')
                    c.sql(f'UPDATE {table} SET "UserID Updated" = "UserID Entered";')
                    c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "Name of User Updated" VARCHAR;')
                    c.sql(f'UPDATE {table} SET "Name of User Updated" = "UserID Entered";')
                if user_updated != '' and user_enterd =='':
                    c.sql(f'ALTER TABLE {table} RENAME COLUMN "{user_updated}" TO "UserID Updated";')
                    c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "Name of User Updated" VARCHAR;')
                    c.sql(f'UPDATE {table} SET "Name of User Updated" = "UserID Updated";')
                    c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "UserID Entered" VARCHAR;')
                    c.sql(f'UPDATE {table} SET "UserID Entered" = "UserID Updated";')
                    c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "Name of User Entered" VARCHAR;')
                    c.sql(f'UPDATE {table} SET "Name of User Entered" = "UserID Updated";')

            # rename 'Line Description'
            c.sql(f'ALTER TABLE {table} RENAME COLUMN "{line_desciption}" TO "Line Description";')
            # replace char
            pattern = r'[,./:;"|\，。、：；“”‘’]'
            c.sql(f'UPDATE {table} SET "Line Description" = REGEXP_REPLACE("Line Description", \'{pattern}\', \'-\');')
            c.sql(f'UPDATE {table} SET "Line Description" = REPLACE("Line Description", \'\'\', \'-\');')

            # rename amount
            # add 'DC Indicator'
            if amount_select == 'amount':
                c.sql(f'ALTER TABLE {table} RENAME COLUMN "{amount}" TO "Signed Amount EC";')  # Signed Amount EC
                c.sql(f'UPDATE {table} SET "Signed Amount EC" = CAST("Signed Amount EC" AS DECIMAL(18, 2));')
                c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "Unsigned Debit Amount EC" DECIMAL(18, 2);')
                c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "Unsigned Credit Amount EC" DECIMAL(18, 2);')
                c.sql(f'UPDATE {table} \
                    SET "Unsigned Debit Amount EC" = CASE \
                    WHEN CAST("Signed Amount EC" AS DECIMAL(18, 2)) >= CAST(0 AS DECIMAL(18, 2)) THEN CAST("Signed Amount EC" AS DECIMAL(18, 2)) \
                    ELSE 0.0 \
                    END, \
                    "Unsigned Credit Amount EC" = CASE \
                    WHEN CAST("Signed Amount EC" AS DECIMAL(18, 2)) < CAST(0 AS DECIMAL(18, 2)) THEN CAST("Signed Amount EC" AS DECIMAL(18, 2)) \
                    ELSE 0.0 \
                    END;')
                c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "DC Indicator" VARCHAR;')
                c.sql(f'UPDATE {table} \
                    SET "DC Indicator" = CASE \
                    WHEN CAST("Signed Amount EC" AS DECIMAL(18, 2)) >= CAST(0 AS DECIMAL(18, 2)) THEN \'D\' \
                    ELSE \'C\' END;')
            if amount_select == 'd|c':
                debit = amount.split('|')[0]
                credit = amount.split('|')[1]
                c.sql(f'ALTER TABLE {table} RENAME COLUMN "{debit}" TO "Unsigned Debit Amount EC";')  # Unsigned Debit Amount EC
                c.sql(f'ALTER TABLE {table} RENAME COLUMN "{credit}" TO "Unsigned Credit Amount EC";')  # Unsigned Credit Amount EC
                c.sql(f'UPDATE {table} SET "Unsigned Debit Amount EC" = CAST("Unsigned Debit Amount EC" AS DECIMAL(18, 2));')
                c.sql(f'UPDATE {table} SET "Unsigned Credit Amount EC" = CAST("Unsigned Credit Amount EC" AS DECIMAL(18, 2));')
                c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "Signed Amount EC" DECIMAL(18, 2);')
                c.sql(f'UPDATE {table} \
                    SET "Signed Amount EC" = CAST("Unsigned Debit Amount EC" AS DECIMAL(18, 2)) - CAST("Unsigned Credit Amount EC" AS DECIMAL(18, 2));')
                c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "DC Indicator" VARCHAR;')
                c.sql(f'UPDATE {table} \
                    SET "DC Indicator" = CASE \
                    WHEN CAST("Signed Amount EC" AS DECIMAL(18, 2)) >= CAST(0 AS DECIMAL(18, 2)) THEN \'D\' \
                    ELSE \'C\' END;')
            # add 'Signed Journal Amount', 'Unsigned Debit Amount', 'Unsigned Credit Amount'
            c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "Signed Journal Amount" DECIMAL(18, 2);')
            c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "Unsigned Debit Amount" DECIMAL(18, 2);')
            c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "Unsigned Credit Amount" DECIMAL(18, 2);')
            c.sql(f'UPDATE {table} SET "Signed Journal Amount" = "Signed Amount EC";')
            c.sql(f'UPDATE {table} SET "Unsigned Debit Amount" = "Unsigned Debit Amount EC";')
            c.sql(f'UPDATE {table} SET "Unsigned Credit Amount" = "Unsigned Credit Amount EC";')

            # rename 'Account Number'
            c.sql(f'ALTER TABLE {table} RENAME COLUMN "{account}" TO "Account Number";')

            # rename 'Account Description'
            c.sql(f'ALTER TABLE {table} RENAME COLUMN "{account_description}" TO "Account Description";')

            # rename 'Currency'
            if currency_select == 'input':
                c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "Currency" VARCHAR;')
                c.sql(f'UPDATE {table} SET "Currency" = \'{currency}\';')
            if currency_select == 'column':
                c.sql(f'ALTER TABLE {table} RENAME COLUMN "{currency}" TO "Currency";')
            c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "Entity Currency (EC)" VARCHAR;')
            c.sql(f'UPDATE {table} SET "Entity Currency (EC)" = "Currency";')

            # rename 'Auto Manual Interface'
            c.sql(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS "Auto Manual or Interface" VARCHAR;')
            c.sql(f'UPDATE {table} SET "Auto Manual or Interface" = \'{ami}\';')

            # write to txt
            c.sql(f'SELECT \
            Entity, \
            "Company Name", \
            "Journal Number", \
            "Spotlight Type", \
            "Date Entered", \
            "Time Entered", \
            "Date Updated", \
            "Time Updated", \
            "UserID Entered", \
            "Name of User Entered", \
            "UserID Updated", \
            "Name of User Updated", \
            "Date Effective", \
            "Date of Journal", \
            "Financial Period", \
            "Journal Type", \
            "Journal Type Description", \
            "Auto Manual or Interface", \
            "Journal Description", \
            ROW_NUMBER() OVER (PARTITION BY "Journal Number" ORDER BY "Journal Number") AS "Line Number", \
            "Line Description", \
            "Currency", \
            "Entity Currency (EC)", \
            "Exchange Rate", \
            "DC Indicator", \
            "Signed Journal Amount", \
            "Unsigned Debit Amount", \
            "Unsigned Credit Amount", \
            "Signed Amount EC", \
            "Unsigned Debit Amount EC", \
            "Unsigned Credit Amount EC", \
            "Account Number", \
            "Account Description", \
            "Controlling Area for Cost and Profit Centre", \
            "Cost Centre", \
            "Cost Centre Description", \
            "Profit Centre", \
            "Profit Centre Description", \
            "Source Activity or Transaction Code"\
            FROM {table} ORDER BY "Entity", "Journal Number";\
        ').to_csv(f"{file_path}_upload.txt", sep='|')
                
        except Exception as e:
            Log.error(repr(e))
            json_error = json.dumps(repr(e), ensure_ascii=False, indent=2)
            return json_error 
        