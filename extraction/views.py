# views.py

from django.shortcuts import render
from django.http import HttpResponse
from pymongo.errors import ServerSelectionTimeoutError
from excell.settings import MONGODB_CLIENT, MONGODB_DB_NAME, MONGODB_COLLECTION_NAME
import pandas as pd
import logging

logger = logging.getLogger(__name__)

CHUNK_SIZE = 1000


def validate_excel_file(excel_file):
    if not excel_file.name.endswith('.xlsx'):
        raise ValueError('Invalid file type. Please upload an Excel file.')


def connect_to_mongodb(mongodb_client):
    db = mongodb_client[MONGODB_DB_NAME]
    collection = db[MONGODB_COLLECTION_NAME]
    return db, collection


def get_excel_sheet_names(excel_file):
    xls = pd.ExcelFile(excel_file)
    return xls.sheet_names


def process_excel_chunk(excel_file, collection, last_sheet_name, chunk_size):
    excel_reader = pd.ExcelFile(excel_file, engine='openpyxl')
    total_rows = excel_reader.book[last_sheet_name].max_row
    print("total_rows", type(total_rows))

    for start_row in range(0, total_rows, chunk_size):
        chunk = pd.read_excel(
            excel_reader, sheet_name=last_sheet_name,
            skiprows=start_row, nrows=chunk_size, engine='openpyxl'
        )
        # Replace NaT values with None
        chunk = chunk.where(pd.notna(chunk), None)

        result = str(chunk) + "\t"
        
        print(result)
        # Convert DataFrame to a list of dictionaries
        data_as_json = chunk.to_dict(orient='records')

        # Use insert_many to upload data to MongoDB
        collection.insert_many(data_as_json)

        # Log progress
        logger.info(f"Processed {start_row + len(chunk)} / {total_rows} rows")

    # Return values after processing
    values = list(collection.find({}, {'_id': 0}))  # Exclude the '_id' field

    return values


def extract_and_upload_to_mongodb(request):
    success_message = None
    my_data = []  # Initialize an empty list to store data

    if request.method == 'POST' and 'excel_file' in request.FILES:
        excel_file = request.FILES['excel_file']

        try:
            validate_excel_file(excel_file)
            db, collection = connect_to_mongodb(MONGODB_CLIENT)

            sheet_names = get_excel_sheet_names(excel_file)
            last_sheet_name = sheet_names[-1]

            # Process the Excel file and get the data
            my_data = process_excel_chunk(
                excel_file, collection, last_sheet_name, CHUNK_SIZE)

            success_message = f'Data from the last sheet "{
                last_sheet_name}" uploaded successfully'

        except ServerSelectionTimeoutError as e:
            logger.exception(f"Error connecting to MongoDB: {e}")
            return HttpResponse('Error connecting to MongoDB. Make sure MongoDB is running.')
        except ValueError as e:
            logger.exception(f"Invalid file type: {e}")
            return HttpResponse(f"Invalid file type: {e}")
        except Exception as e:
            logger.exception(f"Error processing Excel file: {e}")
            return HttpResponse(f"Error processing Excel file: {e}")

    return render(request, 'extract_and_upload.html', {'success_message': success_message, 'my_data': my_data})
