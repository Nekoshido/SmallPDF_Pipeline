import argparse

from etls.bronze_etl import BronzeETL
from etls.silver_etl import SilverETL
from etls.gold_etl import GoldETL

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Query by country')
    parser.add_argument('--country', dest='country', help='Query by country', default="False",
                        required=False)
    args = parser.parse_args()

    print("Running Bronze Layer ETL")
    etl_bronze = BronzeETL()
    etl_bronze.run()

    print("Running Silver Layer ETL")
    etl_silver = SilverETL()
    etl_silver.run()

    print("Running Gold Layer ETL")
    etl_golden = GoldETL(country=bool(args.country))
    etl_golden.run()

    print("FINISHED!!")
