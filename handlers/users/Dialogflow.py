import os
from google.cloud import dialogflow_v2 as dialogflow


class Dialogflow:
    def __init__(self, text):
        self.text = text
        # Set the environment variable for the service account key file
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'private_key.json'

    async def get_dialogflow_response(self):
        # Create a session client
        session_client = dialogflow.SessionsClient()
        a = self.text
        # Set the session ID and project ID
        session_id = 'my_session_id1'
        project_id = 'firstbot-auug'
        session = session_client.session_path(project_id, session_id)

        # Set the text query and language code
        text_input = dialogflow.TextInput(text=self.text, language_code='ru-RU')
        query_input = dialogflow.QueryInput(text=text_input)

        # Send the text query to the agent
        response = session_client.detect_intent(session=session, query_input=query_input)

        # Print the response
        print(response.query_result.fulfillment_text)
        return response.query_result.fulfillment_text
