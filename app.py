import datetime
import json

from spin_sdk import postgres, variables
from spin_sdk.http import IncomingHandler, Request, Response
from spin_sdk.wit.imports.rdbms_types import ParameterValue_Str


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
                webhookEvent = json_object['webhookEvent']

                if webhookEvent == "jira:issue_updated":
                    issue = json_object['issue']
                    issue_key = issue['key']
                    issue_fields_summary = issue['fields']['summary']

                    # Print the variable to console logs
                    print(f"Received issue update for {issue_key} - {issue_fields_summary}")

                    issue_comment = f"Webhook event {webhookEvent} received at {datetime.datetime.now()}"

                    db_name = variables.get('db_name')
                    db_host = variables.get('db_host')
                    db_port = variables.get('db_port')
                    db_user = variables.get('db_user')
                    db_password = variables.get('db_password')

                    with postgres.open(f"user={db_user} dbname={db_name} host={db_host} port={db_port} password={db_password}") as db:
                        update_count = db.execute("update ifaportal.fct_transfers set last_external_comment = $2 where jira_reference = $1",
                                                  [ParameterValue_Str(issue_key), ParameterValue_Str(issue_comment)])
                        print(f"Number of rows updated {update_count}")

                else:
                    print(f"Received event {webhookEvent}")
            except BaseException as e:
                print(f"Exception whilst handling request {e}")
                return Response(500,
                                {"content-type": "text/plain"},
                                bytes(f"Exception whilst handling event", "utf-8"))

        return Response(200,
                        {"content-type": "text/plain"},
                        bytes(f"Ok", "utf-8"))
