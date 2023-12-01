# excell/extraction/views.py
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from pymongo.errors import ServerSelectionTimeoutError
from excell.settings import MONGODB_CLIENT, MONGODB_DB_NAME, MONGODB_COLLECTION_NAME

# excell/extraction/views.py


def extract_and_upload_to_mongodb(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']

        try:
            # Read Excel file into a pandas DataFrame
            df = pd.read_excel(excel_file)

            # Connect to MongoDB
            db = MONGODB_CLIENT[MONGODB_DB_NAME]
            collection = db[MONGODB_COLLECTION_NAME]

            # Convert DataFrame to a list of dictionaries
            data_as_json = df.to_dict(orient='records')

            # Use insert_many to upload data to MongoDB
            collection.insert_many(data_as_json)

            return HttpResponse('Excel data uploaded to MongoDB successfully.')
        except ServerSelectionTimeoutError:
            return HttpResponse('Error connecting to MongoDB. Make sure MongoDB is running.')
        except Exception as e:
            return HttpResponse(f"Error processing Excel file: {e}")

    return render(request, 'upload_excel.html')
