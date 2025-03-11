import json
import traceback

from spin_sdk import postgres, variables
from spin_sdk.http import IncomingHandler, Request, Response
from spin_sdk.wit.imports.rdbms_types import ParameterValue_Str, ParameterValue_Int32


class IncomingHandler(IncomingHandler):
    def handle_request(self, request: Request) -> Response:
        # Access the request.method
        if request.method == 'POST':
            try:
                # Read the request.body as a string
                print(str(request.body))
                json_str = request.body.decode('utf-8')
                # Create a JSON object representation of the request.body
                json_object = json.loads(json_str)

                # Access a value in the JSON object
                transfer_id = json_object.get('transfer_id')
                transfer_date = json_object.get('transfer_date')
                value = json_object.get('value')
                origin = json_object.get('origin')
                status = json_object.get('status')

                db_name = variables.get('db_name')
                db_host = variables.get('db_host')
                db_port = variables.get('db_port')
                db_user = variables.get('db_user')
                db_password = variables.get('db_password')

                with postgres.open(f"user={db_user} dbname={db_name} host={db_host} port={db_port} password={db_password}") as db:
                    if status == 'CREATED':
                        updated_count = db.execute("insert into public.transfers (transfer_id, transfer_date, \"value\", origin, status) values (($1::TEXT)::UUID, TO_DATE($2, 'YYYY-MM-DD'), $3, $4, $5)",
                                                  [ParameterValue_Str(transfer_id), ParameterValue_Str(transfer_date), ParameterValue_Int32(value), ParameterValue_Str(origin), ParameterValue_Str(status)] )
                        print(f"Number of rows inserted {updated_count}")

                    elif status == 'UPDATED':
                        updated_count = db.execute("update public.transfers set transfer_date=TO_DATE($2, 'YYYY-MM-DD'), \"value\"=$3, origin=$4, status=$5 where transfer_id=($1::TEXT)::UUID",
                                                  [ParameterValue_Str(transfer_id), ParameterValue_Str(transfer_date), ParameterValue_Int32(value), ParameterValue_Str(origin), ParameterValue_Str(status)] )
                        print(f"Number of rows updated {updated_count}")

                    elif status == 'COMPLETED':
                        deleted_count = db.execute("delete from public.transfers where transfer_id=($1::TEXT)::UUID",
                                                  [ParameterValue_Str(transfer_id)] )
                        print(f"Number of rows deleted {deleted_count}")

                    else:
                        print(f"Unknown status type, {status}")

            except BaseException as e:
                print(f"Exception whilst handling request {e}")
                print(traceback.format_exc())
                return Response(500,
                                {"content-type": "text/plain"},
                                bytes(f"Exception whilst handling event", "utf-8"))

        return Response(200,
                        {"content-type": "text/plain"},
                        bytes(f"Ok", "utf-8"))
