import time
import openai
import requests
import hashlib
import datetime
import json
import mysql.connector
import os
from questions import generate_question, generate_picture, get_checklist
import textwrap

# Initialize global variables

# List for available topics and problems:
topics_and_problems = \
    [
        ["Algebra",
         [
             "factored_quadratic_problem", "unfactored_quadratic_problem",
             "quadratic_inequality_problem",
             "rooted_quadratic_problem"
         ]
         ],
        ["Calculus",
         [
             "first_principles_problem", "derivative_problem", "minimum_gradient_problem"
         ]
         ],
        ["Finansies",
         [
             "unknown_interest_problem", "annuity_will_he_make_it_problem",
             "delayed_car_payment_loan"
         ]
         ],
        ["Funksies",
         [
             "hyperbola_unknown_p_and_q_problem", "hyperbola_x_intercept_problem",
             "new_parabola_from_old_problem",
             "hyperbola_axis_of_symmetry_problem", "hyperbola_inequality_question",
             "para_expo_c_problem",
             "para_expo_d_problem", "para_expo_b_and_q_problem", "para_expo_g_range_problem",
             "adding_k_to_f_problem", "linear_inverse_c_problem", "linear_inverse_equation_problem",
             "linear_inverse_a_coordinate_problem", "linear_inverse_ab_length_problem",
             "linear_inverse_area_problem", "unknown_parabola"
         ]
         ],
        ["Waarskynlikheid",
         [
             "event_not_occurring_problem", "abc_intersection_problem",
             "determine_at_least_two_events_problem",
             "are_events_independent", "combination_problem", "another_combination_problem"
         ]
         ],
        ["Rye en Reekse",
         [
             "quadratic_unknown_rule_problem", "quadratic_unknown_tn_problem",
             "quadratic_unknown_n_problem", "quadratic_first_difference_sum_proof_problem",
             "geometric_unknown_rule_problem",
             "geometric_unknown_tn_problem", "geometric_unknown_n_problem",
             "geometric_list_first_terms_problem",
             "geometric_infinity_problem", "sigma_expansion_problem", "rewrite_to_sigma_problem",
             "arithmetic_series_to_n_problem", "arithmetic_find_term_problem",
             "arithmetic_first_five_terms_problem",
             "arithmetic_sequence_rule_problem", "values_for_convergence_problem",
             "geometric_ratio_problem",
             "geometric_series_ratio_problem"
         ]
         ]
    ]

# A few popular menu's used throughout the chatbot logic:
bl_1 = [
    ["1", "Registreer (Student)"],
    ["2", "Registreer (Ouer)👥"],
    ["3", "Meer info en pryse📄💰"]
]

bl_2 = [
    ["1", "Ja, Paket 1💳"],
    ["2", "Ja, Paket 2💳"],
    ["3", "Nee, nie vandag nie🙅"]
]

bl_3 = [
    ["1", "Verander Info 🛠️"],
    ["2", f"Studenteverslag 📊"]
]

bl_4 = [
    ["3", "Terug ⬅"]
]

bl_5 = [
    ["1", "Begin werk 🚀"],
    ["2", "Voeg ouer by 🛠️"],
    ["3", "Raad vir jou 🌟"]
]

bl_5_5 = [
    ["1", "Begin werk 🚀"],
    ["2", "Voeg ouer by 🛠️️"],
    ["10", "Upgrade 🌟"]
]

bl_6 = [
    ["1", "Begin oefen 🚀"],
    ["2", "Kies 'n onderwerp 🔍"],
    ["3", "Kry inspirasie 💡"]
]


########################################################################################################################
########################################################################################################################
# APIs

# OCR API for STEM handwriting:
def convert_mathpix(file_name):
    r = requests.post("https://api.mathpix.com/v3/text",
                      files={"file": open(file_name, "rb")},
                      data={
                          "options_json": json.dumps({
                              "math_inline_delimiters": ["$", "$"],
                              "rm_spaces": True
                          })
                      },
                      headers={
                          "app_id": "remacademy_31121d_f44d55",
                          "app_key": "ac512a1a5ac3009c237492c7f773bcfbed73103588b405d6883c0d77d67b2e37"
                      }
                      )

    response = r.json()
    print(f"response from mathpix \n{response}")
    latex_text = response.get('text')
    return latex_text


# Whatsapp connection to send messages
class WhatsAppGraphAPI:
    def __init__(self, phone_number):
        self.phone_number = phone_number

        self.page_access_token = os.environ.get('PAGE_ACCESS_TOKEN')
        print(f'Page Access Token: {self.page_access_token}')

        self.base_url = self.base_url = f'https://graph.facebook.com/v16.0/124565437403411' \
                                        f'/messages?access_token={self.page_access_token} '

    def get_whatsapp_account_info(self):
        url = 'https://graph.facebook.com/v16.0/124565437403411'
        headers = {'Authorization': f'Bearer {self.page_access_token}'}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f'Error retrieving WhatsApp account info: {response.status_code} {response.text}')
            else:
                print(f'Retrieved WhatsApp account info: {response.json()}')
        except Exception as e:
            print(f"Error: {e}")

    def send_text_message(self, message):
        payload = {
            'messaging_product': 'whatsapp',
            'to': self.phone_number,
            'type': 'text',
            'text': {
                'body': message
            }
        }

        try:
            response = requests.post(self.base_url, json=payload)

            if response.status_code != 200:
                print(f'Error sending message: {response.status_code} {response.text}')
        except Exception as e:
            print(f"Error: {e}")

    def send_text_message_3_buttons(self, message_text, buttons):

        payload = {
            'messaging_product': 'whatsapp',
            'to': self.phone_number,
            'type': 'interactive',
            'interactive': {
                "type": "button",
                "body": {
                    "text": message_text
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": buttons[0][0],
                                "title": buttons[0][1]
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": buttons[1][0],
                                "title": buttons[1][1]
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": buttons[2][0],
                                "title": buttons[2][1]
                            }
                        }

                    ]
                }
            }
        }

        try:
            response = requests.post(self.base_url, json=payload)

            if response.status_code != 200:
                print(f'Error sending message: {response.status_code} {response.text}')
        except Exception as e:
            print(f"Error: {e}")

    def send_text_message_2_buttons(self, message_text, buttons):

        payload = {
            'messaging_product': 'whatsapp',
            'to': self.phone_number,
            'type': 'interactive',
            'interactive': {
                "type": "button",
                "body": {
                    "text": message_text
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": buttons[0][0],
                                "title": buttons[0][1]
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": buttons[1][0],
                                "title": buttons[1][1]
                            }
                        }

                    ]
                }
            }
        }

        response = requests.post(self.base_url, json=payload)
        return response

    def send_text_message_1_button(self, message_text, buttons):

        payload = {
            'messaging_product': 'whatsapp',
            'to': self.phone_number,
            'type': 'interactive',
            'interactive': {
                "type": "button",
                "body": {
                    "text": message_text
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": buttons[0][0],
                                "title": buttons[0][1]
                            }
                        }

                    ]
                }
            }
        }

        response = requests.post(self.base_url, json=payload)
        return response

    def send_template_message(self, template_name, template_parameters):
        payload = {
            'recipient': {'phone_number': self.phone_number},
            'message': {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'button',
                        'text': template_name,
                        'buttons': [template_parameters],
                    },
                },
            },
            'messaging_type': 'MESSAGE_TAG',
            'tag': 'ACCOUNT_UPDATE',
        }

        try:
            response = requests.post(self.base_url, json=payload)

            if response.status_code != 200:
                print(f'Error sending message: {response.status_code} {response.text}')
        except Exception as e:
            print(f"Error: {e}")

    def download_media(self, media_id, file_name, mime_type):

        def get_mime_type_extension(mime_type_: str):
            start_index = mime_type_.find("/")
            extension = mime_type_[start_index + 1:]
            return extension

        media_url = f'https://graph.facebook.com/v16.0/{media_id}'
        headers = {'Authorization': f'Bearer {self.page_access_token}'}
        response = requests.get(media_url, headers=headers)

        if response.status_code == 200:
            response_json = json.loads(response.content)

            # Get the URL of the actual media file from the JSON response.
            media_file_url = response_json.get("url")
            if not media_file_url:
                print("Could not find URL in the response.")
                return None

            # Fetch the actual media file.
            response = requests.get(media_file_url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to download the actual media file: {response.status_code} {response.text}")
                return None

            file_extension = get_mime_type_extension(str(mime_type))
            file_path = f"/tmp/{file_name}.{file_extension}"

            # Save the actual media file.
            with open(file_path, 'wb') as f:
                f.write(response.content)
            return file_path
        elif response.status_code == 404:
            print('Media not found. Please try to retrieve a new media URL and download it again.')
        else:
            print(f'Error downloading media: {response.status_code} {response.text}')

    def upload_media(self, media_path, media_name, media_extension, media_type="image"):
        print(media_path)
        # Check if file exists
        if not os.path.exists(media_path):
            print("File does not exist at specified path.")
            return None

        url = 'https://graph.facebook.com/v17.0/124565437403411/media'

        headers = {
            'Authorization': f'Bearer {self.page_access_token}',
        }

        # Open the file
        try:
            files = {
                'file': (media_name, open(media_path, 'rb'), f'{media_type}/{media_extension}', {'Expires': '0'}),
            }

            response = requests.post(
                url,
                data={
                    'messaging_product': 'whatsapp',
                    'type': f'{media_type}/{media_extension}',
                },
                files=files,
                headers=headers
            )
        except Exception as e:
            print(f"Failed to open file: {e}")
            return None

        media_id = None

        if response.status_code == 200:
            response_json = json.loads(response.text)
            media_id = response_json.get("id", None)
            if media_id:
                print(f"Successfully uploaded media. Media ID is {media_id}")
            else:
                print("Media ID not found in the response")
        else:
            print(f"Failed to upload media. Status code: {response.status_code}, Message: {response.text}")

        return media_id

    def send_whatsapp_media(self, media_path, media_name="output.png", media_extension="png", media_type="image",
                            param_type="IMAGE", caption=""):
        media_object_id = self.upload_media(media_path, media_name=media_name, media_extension=media_extension,
                                            media_type=media_type)
        if media_object_id is None:
            print("Failed to get media ID. Cannot proceed with sending.")
            return

        access_token = self.page_access_token
        to_phone_number = self.phone_number
        url = f'https://graph.facebook.com/v17.0/124565437403411/messages'

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_phone_number,
            "type": param_type,
            f"{param_type.lower()}": {
                "id": media_object_id,
                "caption": caption
            }
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            print(f"Successfully sent media. Response: {response.json()}")
        else:
            print(f"Failed to send media. Status code: {response.status_code}, Message: {response.text}")


# Connection object to get feedback from openai GPT models
class OpenAIAPI:

    def __init__(self):
        self.api_key = os.environ['OPENAI_API_KEY']
        # Assuming you've set the API key as an environment variable
        self.api_key_2 = os.environ['OPENAI_API_KEY_2']
        print()
        openai.api_key = self.api_key

    def transcribe_audio(self, audio_path):
        try:
            audio_file = open(audio_path, "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        except openai.error.RateLimitError:
            openai.api_key = self.api_key_2
            audio_file = open(audio_path, "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file)

        return transcript["text"]

    def get_completion(self, prompt, max_tokens=50, temperature=0.1):
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=temperature,
            )
        except openai.OpenAIError:
            openai.api_key = self.api_key_2
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=temperature,
            )

        return response.choices[0].text.strip()

    def get_chat_completion(self, messages, max_tokens=100, model="gpt-3.5-turbo"):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                max_tokens=max_tokens,
                messages=messages,
            )
        except openai.error.RateLimitError:
            try:
                openai.api_key = self.api_key_2
                response = openai.ChatCompletion.create(
                    model=model,
                    max_tokens=max_tokens,
                    messages=messages,
                )
            except openai.error.RateLimitError:
                try:
                    openai.api_key = self.api_key_2
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        max_tokens=max_tokens,
                        messages=messages,
                    )
                except openai.error.RateLimitError:
                    openai.api_key = self.api_key
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        max_tokens=max_tokens,
                        messages=messages,
                    )

        return response.choices[0].message.content.strip()

    def get_chat_completion_with_function(self, messages, functions, use_gpt_4=False):
        if use_gpt_4:
            model = "gpt-4-0613"
        else:
            model = "gpt-3.5-turbo-0613"
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                functions=functions
            )
        except openai.error.RateLimitError:
            print("ratelimiterror1")
            try:
                openai.api_key = self.api_key_2
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    functions=functions
                )
            except openai.error.RateLimitError:
                print("ratelimiterror2")
                try:
                    openai.api_key = self.api_key_2
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo-0613",
                        messages=messages,
                        functions=functions
                    )
                except openai.error.RateLimitError:
                    print("ratelimiterror3")
                    openai.api_key = self.api_key
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo-0613",
                        messages=messages,
                        functions=functions
                    )

        return response


# function to get instant EFT payment link
def get_ozow_payment_link(phone_number, price):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Unique hash verify request
    def generate_request_hash():
        site_code = 'K20-K20-105'
        country_code = 'ZA'
        currency_code = 'ZAR'
        amount = price
        transaction_reference = f'{current_time}@{phone_number}'
        bank_reference = "Study-Buddy Purchase"
        cancel_url = 'https://europe-west1-nodal-descent-395408.cloudfunctions.net/PaymentSuccessful'
        error_url = 'https://europe-west1-nodal-descent-395408.cloudfunctions.net/PaymentSuccessful'
        success_url = 'https://europe-west1-nodal-descent-395408.cloudfunctions.net/PaymentSuccessful'
        notify_url = 'https://europe-west1-nodal-descent-395408.cloudfunctions.net/PaymentSuccessful'
        private_key = '163dccf623fd44418904b3a8a327b71e'
        is_test = False

        input_string = site_code + country_code + currency_code + amount + transaction_reference + bank_reference + \
                       cancel_url + error_url + success_url + notify_url + str(is_test) + private_key
        input_string = input_string.lower()
        calculated_hash_result = generate_request_hash_check(input_string)
        return calculated_hash_result

    # Check that hash matches
    def generate_request_hash_check(input_string):
        print(f"Before Hashcheck: {input_string}")
        return get_sha512_hash(input_string)

    # convert hash to SHA512
    def get_sha512_hash(input_string):
        sha = hashlib.sha512()
        sha.update(input_string.encode())
        return sha.hexdigest()

    # Send request
    def get_payment_link():
        comp_hash = generate_request_hash()
        c_url = "https://api.ozow.com/postpaymentrequest"

        headers = {
            "Accept": "application/json",
            "ApiKey": "0b2babc33ef345479cbd5797e274be88",
            "Content-Type": "application/json"
        }

        data = {
            "countryCode": "ZA",
            "amount": price,
            "transactionReference": f'{current_time}@{phone_number}',
            "bankReference": "Study-Buddy Purchase",
            "cancelUrl": "https://europe-west1-nodal-descent-395408.cloudfunctions.net/PaymentSuccessful",
            "currencyCode": "ZAR",
            "errorUrl": "https://europe-west1-nodal-descent-395408.cloudfunctions.net/PaymentSuccessful",
            "isTest": False,
            "notifyUrl": "https://europe-west1-nodal-descent-395408.cloudfunctions.net/PaymentSuccessful",
            "siteCode": "K20-K20-105",
            "successUrl": "https://europe-west1-nodal-descent-395408.cloudfunctions.net/PaymentSuccessful",
            "hashCheck": comp_hash
        }

        response = requests.post(c_url, headers=headers, json=data)

        return response.json()

    url = get_payment_link()['url']

    return url


########################################################################################################################
########################################################################################################################
# DATABASE

# Function to retrieve or add documents to the document database
def connect_document_db(doc_name, path, add_or_get='get'):
    def connect_unix_socket():
        db_user = os.environ["DB_USER"]
        db_pass = os.environ["DB_PASS"]
        db_name = "info_docs_db"
        unix_socket_path = os.environ["INSTANCE_UNIX_SOCKET"]

        config = {
            'user': db_user,
            'password': db_pass,
            'database': db_name,
            'unix_socket': unix_socket_path
        }

        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                print("Successfully connected to the database.")
                return connection
        except mysql.connector.Error as error:
            print(f"Error: {error}")
            return None

    def create_table():
        create_table_query = """
            CREATE TABLE IF NOT EXISTS documents (
                id INT AUTO_INCREMENT PRIMARY KEY,
                doc_name VARCHAR(255) NOT NULL,
                document BLOB NOT NULL
            );
            """

        # Execute the SQL query to create the table
        cursor.execute(create_table_query)
        conn.commit()

    def add_document(doc_name_, file_path):
        try:
            with open(file_path, "rb") as file:
                binary_data = file.read()

            query = "INSERT INTO documents (doc_name, document) VALUES (%s, %s)"
            cursor.execute(query, (doc_name_, binary_data))
            conn.commit()
            print("Document added successfully")
        except SyntaxError as e:
            print(f"Error: {e}")

    def get_document_by_name(doc_name_, output_path):
        try:
            query = "SELECT document FROM documents WHERE doc_name=%s"
            cursor.execute(query, (doc_name_,))
            record = cursor.fetchone()

            if record:
                with open(output_path, "wb") as file:
                    file.write(record[0])
                print(f"Document saved to {output_path}")
            else:
                print("Document not found")
        except SyntaxError as e:
            print(f"Error: {e}")

    conn = connect_unix_socket()
    cursor = conn.cursor()

    create_table()

    if add_or_get == 'add':
        add_document(doc_name, path)
    else:
        get_document_by_name(doc_name, path)


# All chatbot database logic: Getters, setters, add and delete functions
class Database:

    def __init__(self, phone_number, message):

        self.conn = self.connect_unix_socket()
        self.cursor = self.conn.cursor()

        self.phone_number = phone_number
        self.message = message

    # Establish a connection to the DB
    @staticmethod
    def connect_unix_socket():
        # Initialize environment variables
        db_user = os.environ["DB_USER"]
        db_pass = os.environ["DB_PASS"]
        db_name = os.environ["DB_NAME"]
        unix_socket_path = os.environ["INSTANCE_UNIX_SOCKET"]

        # Parse variables
        config = {
            'user': db_user,
            'password': db_pass,
            'database': db_name,
            'unix_socket': unix_socket_path
        }

        # Attempt connection
        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                print("Successfully connected to the database.")
                return connection

        # Return None if connection fails.
        except mysql.connector.Error as error:
            print(f"Error: {error}")
            return None

    # Change datatype of specific column:
    def change_column_datatype(self, table, column, new_data_type):
        # save SQL command to change the datatype
        alter_table_sql = f"""
        ALTER TABLE {table}
        MODIFY COLUMN {column} {new_data_type};
        """

        try:
            # Execute SQL command
            self.cursor.execute(alter_table_sql)

            # Commit the transaction (you might do this outside of this function)
            self.conn.commit()

            print("Column datatype changed successfully.")

        except Exception as err:
            print(f"An error occurred: {err}")

    # Legacy Function, can be altered to create future tables
    def create_tables(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS sub_topic_tracker
                            (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                user_id INT,
                                topic_number VARCHAR(255),
                                sub_topic_number VARCHAR(255),
                                FOREIGN KEY (user_id) REFERENCES registered_referral_ (id)
                            )
                        ''')

        self.conn.commit()

    ########################################################################################
    # Session methods

    def get_session_field(self, field, state=None):

        def get_parent_field():
            # Execute SQL query
            self.cursor.execute(
                "SELECT {} FROM session WHERE user_id = (SELECT id FROM user WHERE parent_phone = %s LIMIT 1) "
                "ORDER BY id DESC LIMIT 1"
                .format(field), (self.phone_number,))

            # Fetch result
            result_ = self.cursor.fetchone()

            return result_

        def get_student_field():
            # Execute query
            self.cursor.execute(
                "SELECT {} FROM session WHERE user_id = "
                "(SELECT id FROM user WHERE phone_number = %s LIMIT 1) ORDER "
                "BY id DESC LIMIT 1".format(
                    field), (self.phone_number,))

            # fetch result
            result_ = self.cursor.fetchone()

            return result_

        # Check if state is provided, if Not search for both parent and student states:
        if state is None:
            # Search Parent fields:
            result = get_parent_field()

            # Check result
            if result is None:
                # Search student fields:
                result = get_student_field()

        elif state.lower() == "parent":
            # Search Parent fields:
            result = get_parent_field()

        elif state.lower() == "student":
            # Search student fields:
            result = get_student_field()

        else:
            result = None
            print("Unknown state for get_session_field")

        # check result:
        if result is None:
            return None
        else:
            return result[0]

    def set_session_field(self, field, value, state=None):

        def get_session_id_parent():
            # Execute Query
            self.cursor.execute(
                "SELECT id FROM session WHERE user_id = (SELECT id FROM user WHERE parent_phone = %s LIMIT 1) "
                "ORDER BY id DESC LIMIT 1",
                (self.phone_number,))

            # Fetch result
            session_id_ = self.cursor.fetchone()

            return session_id_

        def get_session_id_student():
            # execute query
            self.cursor.execute(
                "SELECT id FROM session WHERE user_id = (SELECT id FROM user WHERE phone_number = %s LIMIT 1) ORDER "
                "BY id DESC LIMIT 1",
                (self.phone_number,))

            # fetch result
            session_id_ = self.cursor.fetchone()

            return session_id_

        def update_session(session_id_):
            self.cursor.execute(f"UPDATE session SET {field} = %s WHERE id = %s", (value, session_id_[0]))
            self.conn.commit()

        # if state is not provided check both parents and students, else only check appropriately
        if state is None:
            # search for student and parent
            session_id = get_session_id_parent()

            if session_id is None:
                session_id = get_session_id_student()

        elif state.lower() == "parent":
            session_id = get_session_id_parent()

        elif state.lower() == "student":
            session_id = get_session_id_student()

        else:
            session_id = None
            print("Unknown state at set session field")

        if session_id:
            update_session(session_id)
        else:
            print("Problem updating session no session Id found")

    def new_session(self, given_state=None):

        def end_current_session():
            end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.set_session_field("end_time", end_time)

        def get_parent_data():
            # Execute query
            self.cursor.execute(
                "SELECT id, phone_number, parent_phone, payment_status, name, parent_name FROM user WHERE parent_phone = "
                "%s ORDER BY id DESC LIMIT 1",
                (self.phone_number,))

            # fetch result
            user_data_ = self.cursor.fetchone()

            return user_data_

        def get_student_data():
            # execute query
            self.cursor.execute(
                "SELECT id, phone_number, parent_phone, payment_status, name, parent_name FROM user WHERE "
                "phone_number = %s LIMIT 1",
                (self.phone_number,))

            # fetch results
            user_data_ = self.cursor.fetchone()

            return user_data_

        # End old session
        end_current_session()

        # if no state is given then search both parent and student fields
        if given_state is None:
            # Get parent data
            user_data = get_parent_data()

            if user_data:
                # unpack data
                user_id, user_phone, parent_phone, payment_status, name, parent_name = user_data
                state = "parent" if str(payment_status) == "1" or str(payment_status) == "2" else "new"
            else:
                # Get student data
                user_data = get_student_data()

                if user_data:
                    # unpack data
                    user_id, user_phone, parent_phone, payment_status, name, parent_name = user_data
                    state = "student" if str(payment_status) == "1" or str(payment_status) == "2" else "new"
                else:
                    state = "new"

                    # if no user was found add a new user
                    user_id = self.add_or_update_user(phone_number=self.phone_number)

        elif given_state.lower() == "parent":
            # Get parent data
            user_data = get_parent_data()

            if user_data:
                # unpack data
                user_id, user_phone, parent_phone, payment_status, name, parent_name = user_data
                state = "parent" if str(payment_status) == "1" or str(payment_status) == "2" else "new"
            else:
                state = "new"

                # if no user was found add a new user
                user_id = self.add_or_update_user(phone_number=self.phone_number)

        elif given_state.lower() == "student":
            # Get parent data
            user_data = get_student_data()

            if user_data:
                # unpack data
                user_id, user_phone, parent_phone, payment_status, name, parent_name = user_data
                state = "student" if str(payment_status) == "1" or str(payment_status) == "2" else "new"
            else:
                state = "new"

                # if no user was found add a new user
                user_id = self.add_or_update_user(phone_number=self.phone_number)

        else:
            print("unknown state at new_session")
            return

        # set start_time to current time
        start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Execute query
        self.cursor.execute(
            "INSERT INTO session (user_id, state, sub_state, practice_state, handle_practice_menu_state, "
            "select_topic_state, start_time) VALUES (%s, %s, 'start', 'start', 'start', 'start', %s)",
            (user_id, state, start_time))

        # Commit changes
        self.conn.commit()

        return user_id

    def end_session(self, given_state=None):

        def update_parent():
            # execute query
            self.cursor.execute(
                "UPDATE session SET end_time = %s WHERE user_id = (SELECT id FROM user WHERE parent_phone = %s "
                "ORDER BY id DESC limit 1) AND end_time IS NULL",
                (end_time, self.phone_number))

            # save changes
            self.conn.commit()

        def update_student():
            # run query
            self.cursor.execute(
                "UPDATE session SET end_time = %s WHERE user_id = (SELECT id FROM user WHERE phone_number = %s "
                "ORDER BY id DESC limit 1) AND end_time IS NULL",
                (end_time, self.phone_number))
            # save changes
            self.conn.commit()

        # Set end time to current time
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if given_state.lower() == "parent":
            update_parent()
        elif given_state.lower() == "student":
            update_student()
        else:
            update_parent()
            update_student()

    def get_or_start_session(self, given_state=None):

        def get_id_parent():
            self.cursor.execute(
                "SELECT id FROM session WHERE user_id = (SELECT id FROM user WHERE parent_phone = %s LIMIT 1) AND "
                "end_time IS NULL LIMIT 1",
                (self.phone_number,))
            session_data_ = self.cursor.fetchone()

            return session_data_

        def get_id_student():
            self.cursor.execute(
                "SELECT id FROM session WHERE user_id = (SELECT id FROM user WHERE phone_number = %s LIMIT 1) AND "
                "end_time IS NULL LIMIT 1",
                (self.phone_number,))
            session_data_ = self.cursor.fetchone()

            return session_data_

        def get_session_data():
            if given_state.lower() == "parent":
                session_data_ = get_id_parent()

            elif given_state.lower() == "student":
                session_data_ = get_id_student()

            elif given_state is None:
                # Attempt to find the current session for the user based on phone number
                session_data_ = get_id_parent()

                if session_data_ is None:
                    session_data_ = get_id_student()

            else:
                print("Unknown state passed to get_or_start_sesssion")

            return session_data_

        def get_id_from_new_session(user_id_):
            self.cursor.execute(
                "SELECT id FROM session WHERE user_id = %s "
                "ORDER BY id DESC LIMIT 1",
                (user_id,))
            new_session_data_ = self.cursor.fetchone()

            return new_session_data_

        # retrieve existing session id if there is an open session
        session_data = get_session_data()

        # Check results
        if session_data:
            # Return existing session id
            return session_data[0]

        # if no result is found start a new session
        else:
            user_id = self.new_session()

            # Retrieve the id of the newly created session
            new_session_data = get_id_from_new_session(user_id)

            # Check results again
            if new_session_data:
                return new_session_data[0]
            else:
                print("problem with fetching or starting session")
                return None

    def add_message(self, role, content):

        # get session id
        session_id = self.get_or_start_session()

        # retrieve current messages
        self.cursor.execute("SELECT messages FROM session WHERE id = %s", (session_id,))
        session_data = self.cursor.fetchone()

        # parse messages
        messages = json.loads(session_data[0]) if session_data and session_data[0] else []

        # add new message
        messages.append({
            'role': role,
            'content': content
        })

        # save updated messages field
        self.cursor.execute("UPDATE session SET messages = %s WHERE id = %s", (json.dumps(messages), session_id))
        self.conn.commit()

    def get_messages_for_session(self):
        # get_session_id
        session_id = self.get_or_start_session()

        # retrieve messages for session
        self.cursor.execute("SELECT messages FROM session WHERE id = %s", (session_id,))
        session_data = self.cursor.fetchone()

        # return parsed messages field
        return json.loads(session_data[0]) if session_data and session_data[0] else []

    def rewrite_messages(self, message_list):
        # This function overwrites existing messages field

        # get session id
        session_id = self.get_or_start_session()

        # overwrite messages with provided message_list for retrieved session
        self.cursor.execute("UPDATE session SET messages = %s WHERE id = %s", (json.dumps(message_list), session_id))
        self.conn.commit()

    def delete_messages(self):
        # get session id
        session_id = self.get_or_start_session()

        # directly set messages to an empty list (or string)
        self.cursor.execute("UPDATE session SET messages = %s WHERE id = %s", (json.dumps([]), session_id))
        self.conn.commit()

    ########################################################################################
    # User Methods

    def get_parent_field(self, field):
        # execute query
        self.cursor.execute("SELECT {} FROM user WHERE parent_phone = %s ORDER BY id DESC LIMIT 1".format(field),
                            (self.phone_number,))
        # fetch results
        result = self.cursor.fetchone()

        return result[0] if result else None

    def get_user_field(self, field):
        # execute query
        self.cursor.execute("SELECT {} FROM user WHERE phone_number = %s ORDER BY id DESC LIMIT 1".format(field),
                            (self.phone_number,))
        # fetch result
        result = self.cursor.fetchone()

        return result[0] if result else None

    def add_or_update_user(self, **kwargs):

        # get the phone number, defaulting to the instance's phone number
        phone_num = kwargs.get("phone_number",
                               self.phone_number)

        # Check if user is already registered as a parent or student

        # check parent
        self.cursor.execute("SELECT id FROM user WHERE parent_phone = %s", (phone_num,))
        user_data = self.cursor.fetchone()

        if user_data is None:  # No parent
            # check student
            self.cursor.execute("SELECT id FROM user WHERE phone_number = %s", (phone_num,))
            user_data = self.cursor.fetchone()

        # Check results
        if user_data:
            # user exists, update info

            # get id
            id_ = user_data[0]

            # parse kwargs
            update_fields = ", ".join(["{} = %s".format(key) for key in kwargs])

            # execute query
            self.cursor.execute("UPDATE user SET {} WHERE id = %s".format(update_fields),
                                (*kwargs.values(), id_))

        else:  # user doesn't exist
            # add new user

            # parse kwargs
            columns = ", ".join(kwargs.keys())
            placeholders = ", ".join(["%s" for _ in kwargs])

            # execute query
            self.cursor.execute("INSERT INTO user ({}) VALUES ({})".format(columns, placeholders),
                                tuple(kwargs.values()))

            # fetch newly created id
            id_ = self.cursor.lastrowid

        # save any changes
        self.conn.commit()

        return id_

    def add_user(self, **kwargs):
        # parse Kwargs
        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join(["%s" for _ in kwargs])

        # execute query
        self.cursor.execute("INSERT INTO user ({}) VALUES ({})".format(columns, placeholders),
                            tuple(kwargs.values()))

        # save changes
        self.conn.commit()

    def get_current_topic_number(self):
        # see if topic number has been saved
        topic_no = self.get_user_field('current_topic_number')

        if topic_no is None:  # topic number has not been added
            # set topic number to default value
            self.set_user_field("current_topic_number", 0)
            topic_no = 0

        # return found or set value
        return topic_no

    def get_current_sub_topic_number(self):
        # check if sub_topic_number has been saved
        sub_topic_number = self.get_user_field('current_sub_topic_number')

        if sub_topic_number is None:  # has not been saved
            # set to default
            self.set_user_field("current_sub_topic_number", 0)
            sub_topic_number = 0

        return sub_topic_number

    def save_current_question(self, problem, solution):
        # execute sql query
        self.cursor.execute("UPDATE user SET current_problem = %s, current_solution = %s WHERE phone_number = %s",
                            (problem, solution, self.phone_number))
        # save changes
        self.conn.commit()

    def get_current_question(self):
        problem = self.get_user_field('current_problem')
        solution = self.get_user_field('current_solution')
        return problem, solution

    def set_user_field(self, field, value):
        # run query
        self.cursor.execute(f"UPDATE user SET {field} = %s WHERE phone_number = %s", (value, self.phone_number))
        # save changes
        self.conn.commit()

    def set_parent_field(self, field, value):
        # run query
        self.cursor.execute(f"UPDATE user SET {field} = %s WHERE parent_phone = %s", (value, self.phone_number))
        # save changes
        self.conn.commit()

    def delete_users(self):
        # this function deletes redundant user profiles that might have been created during signup
        result = ""

        # Checks if any user profiles has not been completed with signup process:
        self.cursor.execute("SELECT id FROM user WHERE "
                            "(phone_number = %s AND (payment_status != 1 AND payment_status != 2)) OR "
                            "(parent_phone = %s AND (payment_status != 1 AND payment_status != 2))",
                            (self.phone_number, self.phone_number))
        result_list = self.cursor.fetchall()

        # Delete said profiles
        if result_list:
            for result in result_list:
                id_ = result[0]
                self.cursor.execute("DELETE FROM session WHERE user_id = %s",
                                    (id_,))
                self.cursor.execute("DELETE FROM user WHERE id = %s",
                                    (id_,))

                # save changes
                self.conn.commit()

    ########################################################################################
    # topic related methods

    def store_sub_topic_number(self, topic_number, sub_topic_number):
        # get associated user id
        user_id = self.get_user_field("id")

        # run query
        self.cursor.execute(f"UPDATE sub_topic_tracker SET sub_topic_number = %s WHERE user_id = %s AND topic_number "
                            f"= %s", (sub_topic_number, user_id, topic_number))

        # save changes
        self.conn.commit()

    def fetch_sub_topic_number(self, topic_number):
        # get associated user id
        user_id = self.get_user_field("id")

        # run query to get sub_topic_number
        self.cursor.execute(f"SELECT sub_topic_number FROM sub_topic_tracker WHERE user_id = %s and topic_number = %s",
                            (user_id, topic_number))

        # retrieve result
        result = self.cursor.fetchone()

        # check result
        if result:
            result = result[0]
        else:
            # return default (0) if no sub_topic_number was found
            result = 0

        return result

    def add_topic_to_sub_topic_tracker(self, topic_number):
        # get associated id
        user_id = self.get_user_field("id")

        # insert value
        self.cursor.execute(
            f"INSERT INTO sub_topic_tracker (user_id, topic_number, sub_topic_number) VALUES (%s, %s, 0)",
            (user_id, topic_number))

        # save changes
        self.conn.commit()

    # @ legacy method...
    def create_topic_list_for_sub_topic_tracker(self):
        for i in range(len(topics_and_problems)):
            self.add_topic_to_sub_topic_tracker(i)

    def get_topic_field(self, field, topic_number=None):

        # Get necessary variables

        # get appropriate user id
        user_id = self.get_user_field("id")

        # get topic number if none was provided
        if topic_number is None:
            topic_number = self.get_user_field('current_topic_number')
        sub_topic_num = self.get_user_field('current_sub_topic_number')

        # set up sql query to execute
        def run_sql_query(user_id_, topic_number_, sub_topic_num_):
            self.cursor.execute(
                f"SELECT {field} FROM topics WHERE user_id = %s"
                f" AND topic_number = %s AND sub_topic_number = %s ORDER BY "
                f"id DESC LIMIT 1",
                (user_id_, topic_number_, sub_topic_num_))
            result_ = self.cursor.fetchone()

            return result_

        # Querying the specified field for the current topic and sub-topic
        result = run_sql_query(user_id, topic_number, sub_topic_num)

        # Check if results was found
        if result is None:
            # no results found, add topic
            self.add_topic(topic_number=topic_number, sub_topic_number=sub_topic_num)

            # retrieve results again
            result = run_sql_query(user_id, topic_number, sub_topic_num)

        return result[0] if result else None

    def get_current_streak(self):
        # Get and Convert question streak into an integer
        # get:
        question_streak = self.get_question_streak()
        # Convert:
        current_streak = int(question_streak[0]) + int(question_streak[1]) + int(question_streak[2]) + int(
            question_streak[3]) + int(question_streak[4])

        return current_streak

    def get_question_streak(self):
        # Get question streak
        question_streak = self.get_topic_field('question_streak')

        # If no result set question streak to default (00000)
        if question_streak is None:
            self.set_topic_field("question_streak", "00000")

            # Get again
            question_streak = self.get_topic_field('question_streak')

        return question_streak

    def set_question_streak(self, streak_value):

        # Get necessary variables
        user_id = self.get_user_field("id")
        topic_num = self.get_user_field('current_topic_number')
        sub_topic_num = self.get_user_field('current_sub_topic_number')

        # Execute SQL
        self.cursor.execute(
            "UPDATE topics SET question_streak = %s WHERE user_id = %s AND topic_number = %s AND sub_topic_number = "
            "%s",
            (streak_value, user_id, topic_num, sub_topic_num))

        # Save changes
        self.conn.commit()

    def plus_one_question_attempt(self):

        # Get necessary variables
        user_id = self.get_user_field("id")
        current_attempts = self.get_topic_field('attempts')

        # Update if result was found
        if current_attempts is not None:

            # set new value
            new_attempts = current_attempts + 1

            # Update database 'topic' table
            self.set_topic_field("attempts", new_attempts)
        else:
            # if no result was found attempts was at 0 so to speak so update to 1
            self.set_topic_field("attempts", 1)

    def get_current_topic(self):
        # fetch topic number
        topic_number = self.get_current_topic_number()
        # match number with topic in list
        return topics_and_problems[topic_number][0]

    def set_topic_field(self, field, value):

        # get necessary variables
        user_id = self.get_user_field("id")
        topic_num = self.get_user_field('current_topic_number')
        sub_topic_num = self.get_user_field('current_sub_topic_number')

        # run SQL to update db
        self.cursor.execute(
            f"UPDATE topics SET {field} = %s WHERE user_id = %s AND topic_number = %s AND sub_topic_number = %s",
            (value, user_id, topic_num, sub_topic_num))

        # save changes
        self.conn.commit()

    def get_topic_progress(self, topic_number):

        # initialize necessary variables
        sub_topic_number = self.fetch_sub_topic_number(topic_number)
        amount_of_sub_topics = len(topics_and_problems[topic_number][1])

        # calculate progress %
        return_string = f"{((sub_topic_number / amount_of_sub_topics) * 100).__round__(2)}%"

        return return_string

    def get_current_topic_progress(self):
        # Return a neat string which explains the progress
        topic_number = self.get_current_topic_number()
        sub_topic_number = self.get_current_sub_topic_number()

        amount_of_sub_topics = len(topics_and_problems[topic_number][1])
        current_topic = self.get_current_topic()
        return_string = f"Uit {amount_of_sub_topics} tipe vrae in {current_topic} " \
                        f"het jy {sub_topic_number} klaar bemeester. Jy het dus" \
                        f" {((sub_topic_number / amount_of_sub_topics) * 100).__round__(2)}% " \
                        f"van {current_topic} voltooi."

        return return_string

    def sub_topic_plus_one(self):

        # get current progress info
        topic_number = self.get_current_topic_number()
        sub_topic_number = self.get_current_sub_topic_number()

        # get possible progress info
        amount_of_sub_topics = len(topics_and_problems[topic_number][1])
        amount_of_topics = len(topics_and_problems)

        # if all topics and subtopics are finished return all done
        if (sub_topic_number + 1) >= amount_of_sub_topics:
            if (topic_number + 1) >= amount_of_topics:
                return "All done!"

            # if all sub_topics are done but other topics are available update topic number and reset sub_topic_number
            else:
                self.set_user_field("current_topic_number", topic_number + 1)
                self.set_user_field("current_sub_topic_number", 0)
                return "topics updated"

        # if there are still sub_topics to complete only update sub_topics
        else:
            self.set_user_field("current_sub_topic_number", sub_topic_number + 1)
            self.store_sub_topic_number(topic_number, sub_topic_number + 1)
            return "sub topics updated"

    def add_topic(self, topic_number, sub_topic_number):
        user_id = self.get_user_field("id")
        self.cursor.execute(
            f"INSERT INTO topics (user_id, topic_number, sub_topic_number, attempts, question_streak, current_streak) "
            f"VALUES (%s, %s, %s, 0, '00000', 0)",
            (user_id, topic_number, sub_topic_number))
        self.conn.commit()

    #########################################################################################
    # Promo functions

    def validate_promo_code(self, promo_code):
        # See if Promo code is a valid, generated code
        # Search
        self.cursor.execute(
            f"SELECT * from registered_referral_ WHERE promo_code = %s", (promo_code,)
        )
        # Fetch result
        result = self.cursor.fetchone()

        # Check result
        if result:
            return True
        else:
            return False

    def tie_promo_code(self, promo_code):
        # Tie a specific user's account with a promo code.

        # delete any duplicate entries
        self.cursor.execute(f"DELETE FROM promo_signups_ WHERE signup_number = %s", (self.phone_number,))
        # Save changes
        self.conn.commit()

        # Insert user with Promo code
        self.cursor.execute(f"INSERT INTO  promo_signups_ (promo_code, signup_number) VALUES (%s, %s)",
                            (promo_code, self.phone_number))
        # save changes
        self.conn.commit()

    def find_promo_code(self):
        # EXECUTE SQL
        self.cursor.execute("SELECT id from promo_signups_ WHERE signup_number = %s", (self.phone_number,))
        # FETCH RESULTS
        result = self.cursor.fetchone()

        return result[0] if result else None

    #########################################################################################
    # Other

    def student_signup_delete_logic(self, user_id_):

        # Find any other duplicate parent signups from same phone number
        self.cursor.execute("SELECT id FROM user WHERE parent_phone = %s AND id != %s",
                            (self.phone_number, user_id_))
        # fetch result
        result_ = self.cursor.fetchone()

        # If result found save user id
        if result_:
            delete_id = result_[0]
        else:
            # Find any other duplicate student signups from same phone number
            self.cursor.execute("SELECT id FROM user WHERE phone_number = %s AND id != %s",
                                (self.phone_number, user_id_))

            # fetch result
            result_ = self.cursor.fetchone()

            # If result found save user id
            if result_:
                delete_id = result_[0]
            else:
                # No results found, save nonsensical id
                delete_id = 0

        # Execute delete queries
        self.cursor.execute("DELETE FROM session WHERE user_id = %s",
                            (delete_id,))
        self.cursor.execute("DELETE FROM user WHERE id = %s", (delete_id,))
        self.delete_messages()

        # save changes
        self.conn.commit()

        # Create new session for user and end old session
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.set_session_field("end_time", current_time)

        self.cursor.execute("INSERT INTO session (user_id, state, sub_state, start_time)"
                            " VALUES (%s, 'new', 'referral_question_asked', %s)",
                            (user_id_, current_time))

        self.conn.commit()

    def parent_signup_delete_logic(self, user_id_):
        self.cursor.execute("SELECT id FROM user WHERE parent_phone = %s AND id != %s",
                            (self.phone_number, user_id_))
        delete_id = self.cursor.fetchone()
        if delete_id:
            delete_id = delete_id[0]
        else:
            self.cursor.execute("SELECT id FROM user WHERE phone_number = %s AND id != %s",
                                (self.phone_number, user_id_))
            delete_id = self.cursor.fetchone()
            if delete_id:
                delete_id = delete_id[0]
            else:
                delete_id = 0
        self.cursor.execute("DELETE FROM session WHERE user_id = %s",
                            (delete_id,))
        self.cursor.execute("DELETE FROM user WHERE id = %s", (delete_id,))
        self.conn.commit()

        # Clear current messages
        self.delete_messages()

        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.set_session_field("end_time", current_time)
        self.cursor.execute("INSERT INTO session (user_id, state, sub_state, start_time)"
                            " VALUES (%s, 'new', 'referral_question_asked', %s)",
                            (user_id_, current_time))

        self.conn.commit()


########################################################################################################################
########################################################################################################################
# Chatbot

# function to validate phone_number formats
def _validate_phone_number(phone_number: str):
    phone_number = phone_number.replace(" ", "").replace("'", "")

    if phone_number.startswith('0'):
        phone_number = "27" + phone_number[1:]

    elif phone_number.startswith('+27'):
        phone_number = phone_number[1:]

    validated = False
    if len(phone_number[2:]) == 9 and phone_number[2:].isnumeric():
        validated = True

    return validated, phone_number


def _get_valid_name(current_g_name):
    # extract necessary variables from ai feedback
    def extract_params(data_):
        arguments_str = data_["choices"][0]["message"]["function_call"]["arguments"]

        # Convert the 'arguments' string to a dictionary
        arguments_dict = eval(arguments_str)

        # Extract values
        try:
            user_name_ = arguments_dict["user_name"]
        except KeyError:
            user_name_ = ""

        return user_name_

    # Establish openai connection

    # establish openai connection
    openai_connection = OpenAIAPI()

    # Set up function list
    function_list = [
        {
            "name": "save_valid_name",
            "description": "save the user's name (excluding any emoji's that might be present)",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_name": {
                        "type": "string",
                        "description": "The name of the user, excluding any emoji's or unicode"
                                       " representations of emojis or symbols that might be present"
                    }
                }
            }
        }
    ]

    # Set up messages list
    messages = [
        {"role": "system", "content": "You will be given a user's display name on Whatsapp. "
                                      "Your job is to extract the name and exclude any emoji's "
                                      "or unicode reresentations of emoji's and pass the name "
                                      "(Alphabetic characters only) as paramater to the save_valid_name function"},
        {"role": "user", "content": current_g_name}
    ]

    # Get completion
    feedback = openai_connection.get_chat_completion_with_function(messages, function_list, True)

    # isolate name
    user_name = extract_params(feedback)

    return user_name


# Chatbot logic
class Chatbot:

    # Initiate the class
    def __init__(self, message, message_type, phone_number, g_user_name=""):

        # Set necessary class variables
        self.phone_number = phone_number
        self.message = message
        self.message_type = message_type
        self.g_user_name = g_user_name

        # Initiate database connection
        self.db = Database(phone_number, message)

        # Get current session info/create a new session if the user has no open session
        self.db.get_or_start_session()

        # Save state and sub_state as class variables
        self.state = self.db.get_session_field("state")
        self.sub_state = self.db.get_session_field("sub_state")

        # set name to WA display name
        if self.state == "parent":
            try:
                self.db.set_user_field("parent_name", g_user_name)
            except mysql.connector.errors.DatabaseError:
                new_name = _get_valid_name(g_user_name)
                try:
                    self.db.set_user_field("parent_name", new_name)
                except mysql.connector.errors.DatabaseError:
                    pass

        elif self.state == "student":
            try:
                self.db.set_user_field("name", g_user_name)
            except mysql.connector.errors.DatabaseError:
                new_name = _get_valid_name(g_user_name)
                try:
                    self.db.set_user_field("name", new_name)
                except mysql.connector.errors.DatabaseError:
                    pass

    # Initial message filter
    def process_message(self):

        # 0 is the escape character
        # Therefore 0 is checked at each
        # message to get back to the main menu
        if self.message == "0":

            # if the user decides to go back to the
            # main menu a new session will be started
            self.db.new_session()

            # get the states
            self.state = self.db.get_session_field("state")
            self.sub_state = self.db.get_session_field("sub_state")

            # check state and sub_state to send the correct main menu
            if self.state == "parent":
                self.handle_parent()
            elif self.state == "student":
                self.handle_student()
            else:
                self.handle_new_user()

        else:
            # if message was not 0, that means we need to send it on to the correct state handler
            state_handlers = {
                'new': self.handle_new_user,
                'parent': self.handle_parent,
                'student': self.handle_student,
            }

            # find the correct state in the dictionary and save the corresponding method
            handler = state_handlers.get(self.state)

            # if a result is found call the corresponding method
            if handler:
                handler()
            else:
                print(f"Warning: Unhandled state 85'{self.state}'")

    # All logic for new users
    def handle_new_user(self):

        # Level 1
        # Where new_user logic starts
        def send_welcome_message():
            # set sub_state to 'handle_initial_reply'
            self.db.set_session_field("sub_state", 'handle_initial_reply')

            message_text = f"Hi {self.g_user_name}, welkom by Study-Buddy vir Wiskunde! 😊" \
                           f"\n\n" \
                           f"Hoe kan ek jou vandag help?"

            # send welcome message to new user
            self.send_text_message_with_buttons(message_text, bl_1)

        # level 2
        # Handle the reply to the welcome message
        def handle_initial_reply():

            # sends initial signup instructions for students
            def student_signup():

                # add user with current available info
                try:
                    user_id = self.db.add_or_update_user(name=self.g_user_name, phone_number=self.phone_number)
                except mysql.connector.errors.DatabaseError:
                    new_name = _get_valid_name(self.g_user_name)
                    try:
                        user_id = self.db.add_or_update_user(name=new_name, phone_number=self.phone_number)

                    except mysql.connector.errors.DatabaseError:
                        user_id = self.db.add_or_update_user(phone_number=self.phone_number)

                # Delete any duplicates
                self.db.student_signup_delete_logic(user_id)

                # Send next user message
                send_referral_question()

            # sends initial instructions for parents
            def send_signup_info_p():
                # Set the sub_state appropriately
                self.db.set_session_field("sub_state", "process_signup_info_p")

                # send message explaining what info is necessary
                self.send_text_message_with_buttons("Fantasties! 🎉 Ek is bly dat julle wil aansluit by Study-Buddy."
                                                    "\n\nStuur asseblief net nou die student se selfoon nommer"
                                                    " deur. 📋📞", [["0", "Back 🔙"]])

            # Sends a document which further explains our service
            def send_more_info():
                # set state appropriately
                self.db.set_session_field("sub_state", "handle_initial_reply")

                # send informative documents
                self.send_document("meer_informasie_2.pdf")

                # Take user back one step and repeat the menu
                message_text_ = f"Hoe kan ek verder help? 🤔"
                self.send_text_message_with_buttons(message_text_, bl_1)

            # save methods in dictionary
            message_handlers = {
                "1": student_signup,
                "2": send_signup_info_p,
                "3": send_more_info
            }

            # Check the value selected by the user in his reply and call corresponding methods
            m_handler = message_handlers.get(self.message.lower())

            # Call method if possible
            if m_handler:
                m_handler()
            else:
                # if incorrect reply is found repeat previous message with 'error' message
                message_text = "Eks jammer maar ek het nie jou keuse verstaan nie. 😞 Asseblief probeer weer."
                self.send_text_message_with_buttons(message_text, bl_1)

                # Error logging
                print(f"Warning: Unhandled reply '{self.message}'")

        # level 3
        # Handle Parent sign-ups
        def process_signup_info_p():
            # Check if phone number provided was valid
            validated, phone_number = _validate_phone_number(self.message)

            # if so, save info
            if validated:
                # add user with all available info
                try:
                    user_id = self.db.add_or_update_user(parent_phone=self.phone_number, phone_number=phone_number,
                                                         parent_name=self.g_user_name)
                except mysql.connector.errors.DatabaseError:
                    # in case emojis are added in the name get_valid_name will remove them
                    new_name = _get_valid_name(self.g_user_name)
                    try:
                        user_id = self.db.add_or_update_user(parent_phone=self.phone_number, phone_number=phone_number,
                                                             parent_name=new_name)
                    except mysql.connector.errors.DatabaseError:
                        # if there was a problem with the new name as well, no name will be saved for the time being
                        user_id = self.db.add_or_update_user(parent_phone=self.phone_number, phone_number=phone_number)

                # Delete any duplicate transactions
                self.db.parent_signup_delete_logic(user_id)

                # Send next user message
                send_referral_question(parent_route=True)

            # if not, resend menu
            else:
                self.send_text_message_with_buttons("Ongelukkig was die selfoon nommer ongeldig..."
                                                    "\n\nStuur asseblief die student se selfoon nommer"
                                                    " deur. 📋📞\n\n(Formaat: 0998887575)", [["0", "Back 🔙"]])

        # level 3.1
        def send_referral_question(parent_route=False):
            # set appropriate sub_state
            self.db.set_session_field("sub_state", 'referral_question_asked')

            # Check if referral is being sent to a parent
            if parent_route:
                extra_string = "Ons het die student se selfoon nommer gestoor."
            else:
                extra_string = ""

            # send message to user
            self.send_text_message_with_buttons(f"Dankie! {extra_string}😃"
                                                f"\n"
                                                f"\n Het jy miskien 'n 'PROMO CODE'?"
                                                f"\n"
                                                f"\nIndien jy het stuur die kode asseblief nou deur vir jou 10% afslag."
                                                f"\n\nSelfs al vat jy die gratis paket NOU,"
                                                f" kan jy dit nou insit vir as jy moontlik wil opgradeer eendag.",
                                                [['nee', "Ongelukkig nie 😞"]])

        # level 3.2
        def process_referral_response():

            # Check if Promo code was entered
            if self.message == 'nee':
                # If not, continue to send package options
                send_package_selection()

            # if yes, validate promo
            elif self.db.validate_promo_code(self.message):
                # if validated, tie promo to user
                self.db.tie_promo_code(self.message)
                # send promo_package selection
                send_package_selection(promo_accepted=True)
            else:
                # if not validated resend message with 'error'
                self.send_text_message_with_buttons("Ek is jammer maar ek erken nie die 'PROMO CODE' nie. Asseblief"
                                                    " tik 'n geldige 'PROMO CODE' in of stuur 'nee' om aan te beweeg.",
                                                    [['nee', "Ongelukkig nie 😞"]])

        # level 3.3
        def send_package_selection(promo_accepted=False):
            # Check if Promo code was accepted
            if promo_accepted:
                # if accepted send discounted prices
                self.db.set_session_field("sub_state", "process_package_selection_p")

                message_text = f"Dankie 🙏, Jou PROMO kode is aanvaar en jy kry dus 10% afslag op enige aankoop 😃." \
                               f"\n\nWil u graag voortgaan met u aankoop?" \
                               f"\nU het twee pakette om van te kies." \
                               f"\n\n*Paket een:* " \
                               f"\n- Gratis!" \
                               f"\n- Slegs ou vraestel vrae en oplossings" \
                               f"\n- Beperkde gebruik" \
                               f"\n\n*Paket twee:* 🌟" \
                               f"\n- Slegs R170 (Met jou promo kode)" \
                               f"\n- 'Unlimited usage' ♾️" \
                               f"\n- Toegang tot jou eksamens verby is! 🕐" \
                               f"\n- Handskrif lees tegnologie. 👀" \
                               f"\n- AI-merker en -tutor! 👨🏻‍💻" \
                               f"\n- Ouer terugvoer. 🗣"
                self.send_text_message_with_buttons(message_text, bl_2)
                return

            # if not accepted rest of code below will execute with normal prices
            self.db.set_session_field("sub_state", "process_package_selection")

            message_text = f"Geen probleem nie. 😃" \
                           f"\n\nWil u graag voortgaan met u aankoop?" \
                           f"\nU het twee pakette om van te kies." \
                           f"\n\n*Paket een:* " \
                           f"\n- Gratis!" \
                           f"\n- Slegs ou vraestel vrae en oplossings" \
                           f"\n- Beperkde gebruik" \
                           f"\n\n*Paket twee:* 🌟" \
                           f"\n- Slegs R200" \
                           f"\n- 'Unlimited usage' ♾️" \
                           f"\n- Toegang tot jou eksamens verby is! 🕐" \
                           f"\n- Handskrif lees tegnologie. 👀" \
                           f"\n- AI-merker en -tutor! 👨🏻‍💻" \
                           f"\n- Ouer terugvoer. 🗣"
            self.send_text_message_with_buttons(message_text, bl_2)

        # level 4
        def process_package_selection(promo_accepted=False):
            # generate payment link
            def send_payment_link(price):
                # set appropriate sub_state
                self.db.set_session_field("sub_state", 'payment_link_sent')

                # generate ozow link
                payment_link = get_ozow_payment_link(self.phone_number, price)

                # send user message
                self.send_text_message(f"Wonderlik, ons is amper klaar. 😃 Gebruik die volgende skakel "
                                       f"om jou betaling te finaliseer: 💳"
                                       f"\n"
                                       f"\n{payment_link} 🔗"
                                       )

            if promo_accepted:
                # Check if user would like to continue to purchase
                if self.message == "1":
                    add_package_1_user()
                elif self.message == "2":
                    # set sub_state and resend main menu
                    send_payment_link("170.00")
                elif self.message == "3":
                    # back
                    send_welcome_message()
                else:
                    # repeat previous message
                    message_text = f"\n\nWil u graag voortgaan met u aankoop?" \
                                   f"\nU het twee pakette om van te kies." \
                                   f"\n\n*Paket een:* " \
                                   f"\n- Gratis!" \
                                   f"\n- Slegs ou vraestel vrae en oplossings" \
                                   f"\n- Beperkde gebruik" \
                                   f"\n\n*Paket twee:* 🌟" \
                                   f"\n- Slegs R170 (Met jou Promo kode)" \
                                   f"\n- 'Unlimited usage' ♾️" \
                                   f"\n- Toegang tot jou eksamens verby is! 🕐" \
                                   f"\n- Handskrif lees tegnologie. 👀" \
                                   f"\n- AI-merker en -tutor! 👨🏻‍💻" \
                                   f"\n- Ouer terugvoer. 🗣"
                    self.send_text_message_with_buttons(message_text, bl_2)
                return

            # if promo not accepted rest of code below will execute
            # Check if user would like to continue to purchase
            if self.message == "1":
                add_package_1_user()
            elif self.message == "2":
                send_payment_link("200.00")
            elif self.message == "3":
                # back
                send_welcome_message()
            else:
                # repeat message if reply from user did not make sense
                message_text = f"\n\nWil u graag voortgaan met u aankoop?" \
                               f"\nU het twee pakette om van te kies." \
                               f"\n\n*Paket een:* " \
                               f"\n- Gratis!" \
                               f"\n- Slegs ou vraestel vrae en oplossings" \
                               f"\n- Beperkde gebruik" \
                               f"\n\n*Paket twee:* 🌟" \
                               f"\n- Slegs R200" \
                               f"\n- 'Unlimited usage' ♾️" \
                               f"\n- Toegang tot jou eksamens verby is! 🕐" \
                               f"\n- Handskrif lees tegnologie. 👀" \
                               f"\n- AI-merker en -tutor! 👨🏻‍💻" \
                               f"\n- Ouer terugvoer. 🗣"
                self.send_text_message_with_buttons(message_text, bl_2)

        # level 4
        def process_package_selection_p():
            process_package_selection(True)

        # Level 5
        def add_package_1_user():
            # get logic from handle_payment webhook
            self.db.add_or_update_user(payment_status=2)
            self.db.end_session()
            self.db.delete_users()
            self.send_text_message("Dankie! 🎉🎈 Jy kan nou ons diens gebruik deur net "
                                   "'Hi' 🖐️ na hierdie nommer te stuur vanaf enige van die geregistreerde nommers. "
                                   "Hoop om jou gou weer te sien! 😊")

        # Level 5
        def payment_link_sent_message():
            self.send_text_message("Wag asseblief terwyl ons u betaling verwerk. ⏳")

        # save methods in dictionary
        sub_state_handlers = {
            "start": send_welcome_message,
            "handle_initial_reply": handle_initial_reply,
            "process_signup_info_p": process_signup_info_p,
            "referral_question_asked": process_referral_response,
            "process_package_selection": process_package_selection,
            "process_package_selection_p": process_package_selection_p,
            'payment_link_sent': payment_link_sent_message
        }

        # Call the correct sub_state handler
        handler = sub_state_handlers.get(self.sub_state)
        if handler:
            handler()
        else:
            print(f"Warning: Unhandled state 324'{self.sub_state}'")

    # Handle all parent queries; parent reports, info change and cancellation
    def handle_parent(self):

        # level 1
        def send_initial_message():
            # set appropriate sub state
            self.db.set_session_field("sub_state", 'initial_reply')

            # get appropriate fields from database
            parent_name = self.db.get_parent_field('parent_name')
            name = self.db.get_parent_field('name')

            # send User message
            message_text = f"Welkom terug {parent_name}. 😊" \
                           f"\nEk hoop dat {name} Study-Buddy geniet! 📘" \
                           f"\nHoe kan ek u vandag help? 🤔"
            self.send_text_message_with_buttons(message_text, bl_3)

        # level 2
        def handle_initial_reply():

            def send_change_info_message():
                # set appropriate sub_state
                self.db.set_session_field("sub_state", "handle_change_info")

                # Get info from database
                parent_name = self.db.get_parent_field('parent_name')

                # Send user message
                message_text_ = f"Geen probleem {parent_name}. 😊" \
                                f"\nDie enigste informasie wat ons ooit hoef te verander is selfoonnommers. 📱" \
                                f"\nWil jy jou eie selfoonnommer of die student se selfoonnommer verander?" \
                                f"\n" \
                                f"\n1: Jou selfoonnommer 📞" \
                                f"\n2: Die student se selfoonnommer 📞" \
                                f"\n\n(Kies en stuur die gepaste nommer gevolg deur " \
                                f"die nuwe selfoonnommer. eg. 1. 1234567890) 🔢"
                self.send_text_message_with_buttons(message_text_, bl_4)

            # Send all the user's progress in all topics
            def send_report():
                student_name = self.db.get_parent_field("name")

                # Get topic progress information from topic table and parse into one string
                topic_list = ""
                i = 1
                for topic in topics_and_problems:
                    topic_percentage = self.db.get_topic_progress(i - 1)
                    # Added a book emoji for topics and a bar chart for progress
                    topic_list += f"{i}: 📚 *{topic[0]}* ---> \n{student_name} se huidige vordering is 📊 " \
                                  f"{topic_percentage}\n\n"
                    i += 1

                # Create context for AI
                messages = [
                    {
                        "role": "system", "content": f"Dit is 'n opdatering oor {student_name} se voorbereiding vir"
                                                     f" die opkomende wiskunde eksamen. {student_name} se huidige vordering lyk so:"
                                                     f"\n{topic_list}."
                                                     f"\n"
                                                     f"\nDie verskeie afdelings van die eksamen het die volgende persentasies:"
                                                     f"\n Algebra tel omtrent 16%"
                                                     f"\n Rye en reekse omtrent 17%"
                                                     f"\n Funksies omtrent 25%"
                                                     f"\n Finansieele wiskunde omtrent 10%"
                                                     f"\n calculus omtrent 18 %"
                                                     f"\n Waarskynlikheid omtrent 10%"
                                                     f"\n"
                                                     f"Gebaseer op {student_name} se vordering en die gewigte van die "
                                                     f"afdelings, gee raad vir {student_name} se ouer oor hoe hy vorder"
                                                     f" en wat hy kan doen om beter voor te berei. Jy hoef nie die verslag van sy vordering weer te stuur nie. Genereer slegs raad oor hoe om vorentoe te beweeg."
                                                     f"\n{student_name} is in graad 12 en praat Afrikaans."
                                                     f"Onthou. Jy spreek nou die ouer aan wat ook Afrikaans is."
                    },
                ]
                messages2 = [
                    {
                        "role": "system",
                        "content": f"Genereer asseblief 'n kwotasie wat geduld en harde werk aanmoedig."
                    },
                ]

                # create openai connection
                openai_instance = OpenAIAPI()

                # Get respective completions
                return_string = openai_instance.get_chat_completion(messages, max_tokens=400)
                return_string2 = openai_instance.get_chat_completion(messages2)

                # construct final message
                message_to_send = \
                    f"{return_string}\n\n" \
                    f"{student_name} se huidige vordering lyk so:" \
                    f"\n" \
                    f"\n{topic_list}" \
                    f"\n" \
                    f"\n{return_string2}"

                # send report message
                self.send_text_message(message_to_send)

                # send next steps message
                message_text_ = f"Ek hoop u is tevrede met {student_name} se vordering. 😊" \
                                f"\n" \
                                f"\nWaarmee kan ek nog help vandag? 🤔"
                self.send_text_message_with_buttons(message_text_, bl_3)

            # save functions to dictionary
            message_handlers = {
                "1": send_change_info_message,
                "2": send_report
            }

            # call appropriate functions
            m_handler = message_handlers.get(self.message)
            if m_handler:
                m_handler()
            else:
                # Handle nonsensical message
                message_text = f"Ek's jammer, ek verstaan nie die boodskap nie. 😔 Probeer asseblief weer." \
                               f"\n" \
                               f"\nWaarmee kan ek help? 🤔"
                self.send_text_message_with_buttons(message_text, bl_3)

        # level 3
        def handle_change_info():

            def request_new_cell():
                # Create openAI connection
                openai_instance = OpenAIAPI()

                # create context for openai to isolate phone_number
                messages = [
                    {"role": "system", "content": "Your job is to isolate the phone number in the following message "
                                                  "from the user and return it to me as a variable named "
                                                  "phone_number. for example phone_number = '0123456789'"},
                    {"role": "user", "content": self.message}
                ]

                # get completion
                return_string = str(openai_instance.get_chat_completion(messages))

                # find phone number
                start_index = return_string.find("'")
                end_index = return_string.find("'", start_index + 1)

                # save phone number
                phone_number = return_string[start_index: end_index + 1]
                validated, phone_num = _validate_phone_number(phone_number)
                if validated:
                    self.db.set_parent_field("parent_phone", phone_num)

                    # end current session
                    self.db.end_session()

                    # send user message
                    self.send_text_message(
                        f"Dankie, ek het jou selfoonnommer verander. ✅ "
                        f"Jy kan nou toegang verkry tot ons diens vanaf: {phone_number} 📱")

                else:
                    self.send_text_message_with_buttons("Jammer maar die selfoon nommer is ongeldig. "
                                                        "Asseblief probeer weer:"
                                                        f"\n\nWil jy jou eie selfoonnommer of die student se"
                                                        f" selfoonnommer verander?"
                                                        f"\n"
                                                        f"\n1: Jou selfoonnommer 📞"
                                                        f"\n2: Die student se selfoonnommer 📞"
                                                        f"\n\n(Kies en stuur die gepaste nommer gevolg deur "
                                                        f"die nuwe selfoonnommer. eg. 1. 1234567890) 🔢"
                                                        , bl_4)

            def request_new_student_cell():
                # Create openAI connection
                openai_instance = OpenAIAPI()

                # Give context for gpt-4 to isolate phone_number
                messages = [
                    {"role": "system", "content": "Your job is to isolate the phone number in the following message "
                                                  "from the user and return it to me as a variable named "
                                                  "phone_number. for example phone_number = '0123456789'"},
                    {"role": "user", "content": self.message}
                ]

                # Get completion
                return_string = str(openai_instance.get_chat_completion(messages))

                # Isolate phone number
                start_index = return_string.find("'")
                end_index = return_string.find("'", start_index + 1)

                # Save phone number
                phone_number = return_string[start_index: end_index + 1]
                validated, phone_num = _validate_phone_number(phone_number)
                if validated:
                    self.db.set_parent_field("phone_number", phone_num)

                    # set appropriate substate
                    self.db.set_session_field("sub_state", 'initial_reply')

                    # Send user message
                    message_text_ = f"Dankie, ons het die student se selfoonnommer verander. " \
                                    f"✅ Hy/sy kan nou toegang tot ons diens " \
                                    f"verkry vanaf: {phone_number} 📱" \
                                    f"\n" \
                                    f"\nIs daar nog iets waarmee ek kan help vandag? 🤔"
                    self.send_text_message_with_buttons(message_text_, bl_3)

                else:
                    self.send_text_message_with_buttons("Jammer maar die selfoon nommer is ongeldig. "
                                                        "Asseblief probeer weer:"
                                                        f"\n\nWil jy jou eie selfoonnommer of die student se"
                                                        f" selfoonnommer verander?"
                                                        f"\n"
                                                        f"\n1: Jou selfoonnommer 📞"
                                                        f"\n2: Die student se selfoonnommer 📞"
                                                        f"\n\n(Kies en stuur die gepaste nommer gevolg deur "
                                                        f"die nuwe selfoonnommer. eg. 1. 1234567890) 🔢"
                                                        , bl_4)

            def back():
                # Set appropriate sub_state
                self.db.set_session_field("sub_state", "handle_initial_reply")

                # send user message
                message_text_ = f"\nHoe kan ek jou help vandag? 🤔"
                self.send_text_message_with_buttons(message_text_, bl_3)

            # save methods to dictionary
            message_handlers = {
                "1": request_new_cell,
                "2": request_new_student_cell,
                "3": back
            }
            # call appropriate method
            m_handler = message_handlers.get(self.message[0])
            if m_handler:
                m_handler()
            else:
                # handle nonsensical message
                name = self.db.get_parent_field('name')

                message_text = f"Ek is jammer, ek verstaan nie jou boodskap nie. 😔" \
                               f"\nWatter informasie wil jy graag verander? 🤔" \
                               f"\n" \
                               f"\n1: Jou selfoonnommer? 📱" \
                               f"\n2: {name} se selfoonnommer? 📱" \
                               f"\n\n(Kies en stuur die gepaste nommer gevolg deur " \
                               f"die nuwe selfoonnommer. eg. 1. 1234567890) 🔢"
                self.send_text_message_with_buttons(message_text, bl_4)

        # save methods in dictionary
        sub_state_handlers = {
            "start": send_initial_message,
            "initial_reply": handle_initial_reply,
            'handle_change_info': handle_change_info
        }
        # call appropriate method
        handler = sub_state_handlers.get(self.sub_state)
        if handler:
            handler()
        else:
            print("warning unhandled parent sub_state")

    # All logic related to student interactions
    def handle_student(self):
        # Level 1
        def send_student_welcome_message():
            # set appropriate sub_state
            self.db.set_session_field("sub_state", "handle_initial_reply")

            # get fields from db
            payment_status = self.db.get_user_field("payment_status")

            # save message text
            message_text = f"Welkom terug {self.g_user_name}, Ek hoop jy's reg om jou brein in rat te sit. 🧠💡" \
                           f"\n" \
                           f"\nKies asseblief 'n opsie: 🤔"

            # select menu based on payment status
            if str(payment_status) == "1":
                menu = bl_5
            else:
                menu = bl_5_5

            # send message with buttons
            self.send_text_message_with_buttons(message_text, menu)

        # Level 2
        def handle_initial_reply():
            def send_practice_instructions():

                # set appropriate sub_state
                self.db.set_session_field("sub_state", "handle_practice_menu")

                # Get necessary fields from db
                topic = self.db.get_current_topic()
                topic_progress = self.db.get_current_topic_progress()
                payment_status_ = self.db.get_user_field("payment_status")

                # Check payment status and select appropriate message
                if str(payment_status_) == "1":
                    # Message for premium package
                    message_text_ = f"Dis goeie nuus 🎉. Hoe meer tyd jy insit, hoe beter gaan jou resultate wees. 📈" \
                                    f"\n\nJy was besig met {topic} 📚 en tot dusver " \
                                    f"{topic_progress} ✅"
                else:
                    # Message for free package
                    message_text_ = f"Ek is bly om te hoor. 🎉 " \
                                    f"\nHoe meer tyd jy insit, hoe beter gaan jou resultate wees. 📈" \
                                    f"\nJy was besig met {topic}"

                # Send message
                self.send_text_message_with_buttons(message_text, bl_6)

            def send_change_info_instructions():
                # Get db fields
                parent_phone = self.db.get_user_field("parent_phone")
                payment_status_ = self.db.get_user_field("payment_status")

                # Check if parent has been added and handle appropriately
                if parent_phone is None or parent_phone == "":
                    # set appropriate sub_state
                    self.db.set_session_field("sub_state", "handle_change_info_s")

                    # set message and menu for adding a parent
                    message_text_ = f"Jy beter hard werk nou dat jy jou ouer byvoeg! 😂" \
                                    f"\nEk grap maar net. Dis baie goed om aanspreeklikheid te hê!" \
                                    f"\n\n" \
                                    f"Asseblief stuur die selfoon nommer van jou ouer deur. 😄"
                    menulist = bl_4
                else:
                    # set message and menu if parent has already been added
                    message_text_ = f"Jy het klaar 'n ouer bygevoeg. Asseblief kontak Study-Buddy customer" \
                                    f" service by 066 239 0537 as jy perongeluk die verkeerde nommer bygevoeg het."
                    menulist = bl_5 if payment_status_ == 1 else bl_5_5

                # SEND MESSAGE
                self.send_text_message_with_buttons(message_text_, menulist)

            def send_get_advice_message():
                # Get topic progress information from topic table
                # SET EMPTY STRING TO POPULATE IN LOOP
                topic_list = ""
                # SET COUNTER FOR LOOP
                i = 1
                for topic in topics_and_problems:
                    # ADD EACH TOPIC WITH ITS PROGRESS TO THE STRING RESPECTIVELY
                    topic_percentage = self.db.get_topic_progress(i - 1)
                    topic_list += f"{i}: 📚 *{topic[0]}* ---> \nJou huidige vordering is 📊 {topic_percentage}\n\n"
                    i += 1

                # CREATE OPENAI CONNECTION
                openai_instance = OpenAIAPI()

                # CREATE CONTEXT FOR AI
                messages = [
                    {
                        "role": "system", "content": f"Jou werk is om 'n student advies te gee oor sy voorbereiding vir"
                                                     f" die opkomende wiskunde eksamen. Sy huidige vordering lyk so: "
                                                     f"\n{topic_list}. "
                                                     f"\n"
                                                     f"\nDie verskeie afdelings tel ongeveer die volgende persentasies "
                                                     f"vir die eksamen:"
                                                     f"\n Algebra tel omtrent 16%"
                                                     f"\n Rye en reekse omtrent 17%"
                                                     f"\n Funksies omtrent 25%"
                                                     f"\n Finansieele wiskunde omtrent 10%"
                                                     f"\n calculus omtrent 18 %"
                                                     f"\n Waarskynlikheid omtrent 10%"
                                                     f""
                                                     f"Gebaseer op die student se vordering en die gewigte van die "
                                                     f"afdelings gee raad oor die beste pad vorentoe met voorbereiding."
                                                     f""
                                                     f"\n Die student is graad 12 en is Afrikaans. Wees vriendelik en"
                                                     f" gebruik emojis in jou boodskap"
                    },
                ]
                messages2 = [
                    {
                        "role": "system", "content": f"Genereer asseblief 'n inspirerende, lighartige kwotasie."
                                                     f" Sit emojis by. Stuur dit terug in Afrikaans asseblief."
                    },
                ]

                # GET FEEDBACK
                return_string = openai_instance.get_chat_completion(messages, max_tokens=500, model="gpt-4")
                return_string2 = openai_instance.get_chat_completion(messages2, model="gpt-4")

                # CONCATENATE FINAL STRING
                message_to_send = \
                    f"{return_string}\n\n" \
                    f"Jou huidige vordering lyk tot dusver so:" \
                    f"\n" \
                    f"\n{topic_list}" \
                    f"\n" \
                    f"\n{return_string2}"

                # SEND REPORT
                self.send_text_message(message_to_send)

                # SEND NEXT STEP MENU
                message_text_ = "Ek hoop dit help! 🤞" \
                                "\nKan ek jou met nog iets help vandag? 🤔"

                self.send_text_message_with_buttons(message_text_, bl_5)

            def upgrade_student():

                # SET APPROPRIATE SUB STATE
                self.db.set_session_field("sub_state", "upgrade_student")

                # SEE IF PROMO CODE HAS BEEN ADDED
                promo_id = self.db.find_promo_code()

                if promo_id:
                    # IF PROMO IS ADDED SEND DISCOUNTED PRICE
                    payment_link = get_ozow_payment_link(self.phone_number, "170.00")
                else:
                    # ELSE SEND FULL PRICE
                    payment_link = get_ozow_payment_link(self.phone_number, "200.00")

                # SEND MESSAGE WITH PAYMENT LINK
                self.send_text_message_with_buttons(
                    f"Ek hoop jy sien uit vir al die cool nuwe 'features'! 🌟😄. \n"
                    f"Gebruik sommer hierdie skakel om jou betaling te finaliseer: \n\n {payment_link}",
                    [["0", "Terug 🔙"]])

            # SAVE METHODS IN DICTIONARY
            message_handlers = {
                "1": send_practice_instructions,
                "2": send_change_info_instructions,
                "3": send_get_advice_message,
                "10": upgrade_student
            }

            # CALL APPROPRIATE METHOD
            m_handler = message_handlers.get(self.message)
            if m_handler:
                m_handler()
            else:
                # handle nonsensical reply
                message_text = "Jammer, ek verstaan nie jou antwoord nie. 😔 Hoe kan ek help?"

                # SEND CORRECT MENU MESSAGE BASED ON PAYMENT STATUS
                payment_status = self.db.get_user_field("payment_status")
                if str(payment_status) == "1":
                    self.send_text_message_with_buttons(message_text, bl_5)
                else:
                    self.send_text_message_with_buttons(message_text, bl_5_5)

        # Level 3
        def handle_practice_menu():

            # Get the appropriate handle_practice_menu_state
            handle_practice_menu_state = self.db.get_session_field("handle_practice_menu_state")

            # Handle initial reply from user
            # Level 1
            def start():
                # HANDLE REPLY BASED ON PACKAGE OF USER
                # get package/payment status
                payment_status_ = self.db.get_user_field("payment_status")

                # handle appropriately
                if payment_status_ == 1:
                    practice_menu_message_handlers = {
                        "1": practice_state,
                        "2": select_topic,
                        "3": get_inspiration
                    }
                else:
                    practice_menu_message_handlers = {
                        "1": practice_state_2,
                        "2": select_topic,
                        "3": get_inspiration
                    }

                # call appropriate method
                m_handler = practice_menu_message_handlers.get(self.message)
                if m_handler:
                    m_handler()
                else:
                    # REPEAT PREVIOUS MENU AND ADD CONTEXT IF REPLY FROM USER DOESN'T MAKE SENSE

                    # Get topic and topic progress from database
                    topic = self.db.get_current_topic()
                    topic_progress = self.db.get_current_topic_progress()

                    # send user message
                    if payment_status == 1:
                        message_text = f"Jammer, ek verstaan nie jou antwoord nie. 😔" \
                                       f"\n" \
                                       f"\nJy was besig met {topic} en sover het jy {topic_progress} voltooi. 📚"
                    else:
                        message_text = f"Jammer, ek verstaan nie jou antwoord nie. 😔" \
                                       f"\n" \
                                       f"\nJy was besig met {topic}📚"

                    self.send_text_message_with_buttons(message_text, bl_6)

            # LEVEL 2
            def practice_state():

                # set appropriate handle_practice_menu_state
                self.db.set_session_field("handle_practice_menu_state", "practice_state")

                # get appropriate practice_state
                practice_state_1 = self.db.get_session_field("practice_state")

                def send_sum():

                    # set appropriate db fields
                    self.db.set_session_field("practice_state", "mark_sum")
                    self.db.set_topic_field("attempts", 0)

                    # Get topic info from db
                    topic_number = self.db.get_current_topic_number()
                    current_sub_topic_number = self.db.get_current_sub_topic_number()

                    # generate problem based on retrieved info
                    problem, solution = generate_question(topic_number, current_sub_topic_number)

                    # save generated question to db
                    self.db.save_current_question(problem, solution)

                    # send problem to student
                    self.send_output_image("Stuur asseblief 'n foto van jou werk. Skryf so netjies as moontlik om die "
                                           "beste moontlike resultate te kry. 📷✍️")

                    # Set delay in bc photo takes longer to load than text message on whatsapp
                    time.sleep(0.5)

                    # send message with menu and next options
                    self.send_text_message_with_buttons("Sterkte!",
                                                        [["back", "Terug 🔙"], ["next", "Volgende vraag ⏭"]])

                def next_topic_maybe():
                    # Check if user progress warrants an advancement in topic or sub_topic

                    # get progress info from db
                    question_streak = self.db.get_question_streak()
                    streak = self.db.get_current_streak()

                    # check if User has done well enough in current sub_topic
                    if streak >= 3 or question_streak[3:] == "11":
                        # progress sub_topic
                        self.db.sub_topic_plus_one()

                def start_chat_on_current_problem():

                    # handle message if it was a button reply
                    if self.message.lower() == "next":
                        send_sum()

                        # Exit method
                        return

                    elif self.message.lower() == "solution":
                        def send_solution():
                            problem, solution = self.db.get_current_question()
                            generate_picture("", solution)
                            self.send_output_image(
                                "Hoop jy het dit reg gekry! Jy is welkom om nog vrae te stuur as iets onduidelik is!")
                            time.sleep(0.5)
                            self.send_text_message_with_buttons("Wats volgende?", [["back", "Terug🔙"],
                                                                                   ["next", "Volgende vraag➡"],
                                                                                   ["solution",
                                                                                    "Volledige Oplossing✍"]])

                        send_solution()

                        # Exit method
                        return

                    elif self.message.lower() == "back":
                        # set correct states
                        self.db.set_session_field("handle_practice_menu_state", "start")
                        self.db.set_session_field("practice_state", "start")

                        # get progress for message context
                        topic = self.db.get_current_topic()
                        topic_progress = self.db.get_current_topic_progress()

                        # concatenate message string
                        message_text = f"\nJy was besig met {topic}📚 en sover het jy {topic_progress} voltooi. 📚"

                        # send with applicable menu
                        self.send_text_message_with_buttons(message_text, bl_6)

                        # Exit method
                        return

                    # IF THIS CODE IS REACHED THAT MEANS NO BUTTON
                    # REPLY WAS USED AND WE CONTINUE TO GIVE FEEDBACK TO QUESTIONS

                    # get current problem and solution
                    problem, solution = self.db.get_current_question()

                    # add message received to db
                    self.db.add_message("user", self.message)

                    # retrieve any previous messages
                    messages_addition = self.db.get_messages_for_session()

                    # create openAI connection
                    openai_instance = OpenAIAPI()

                    # Give context to ai
                    messages = [
                        {"role": "system",
                         "content": "Jy is 'n wiskunde tutor. Jou taak is om die student te help met "
                                    "enige vrae wat hulle mag hê aangaande die probleem of die "
                                    "raad wat jy hulle gegee het oor hoe om die probleem beter te benader. "
                                    "Gebruik analogieë of metafore en wees behulpsaam, beleefd en vriendelik. "
                                    "Onthou jy moet nou die student in Afrikaans aanspreek."
                         },
                        {"role": "assistant", "content": problem}
                    ]

                    # Add any previous conversation between user and AI on current problem
                    for i in range(len(messages_addition)):
                        messages.append(messages_addition[i])

                    print(messages)

                    # Add current message
                    # messages.append({"role": "user", "content": self.message})

                    # get completion
                    try:
                        return_string = openai_instance.get_chat_completion(messages, model="gpt-4", max_tokens=400)
                    except openai.error:
                        try:
                            # IF FIRST COMPLETION DIDN'T WORK MESSAGES ARE PROBABLY TOO LONG, REDUCE AND TRY AGAIN
                            messages = [{"role": "system",
                                         "content": "Jy is 'n wiskunde tutor. Jou taak is om die student te help met "
                                                    "enige vrae wat hulle mag hê aangaande die probleem of die "
                                                    "raad wat jy hulle gegee het oor hoe om die probleem beter "
                                                    "te benader. "
                                                    "Gebruik analogieë of metafore en wees behulpsaam, beleefd en"
                                                    " vriendelik. "
                                                    "Onthou jy moet nou die student in Afrikaans aanspreek."
                                         }, {"role": "assistant", "content": problem}, messages_addition[0],
                                        messages_addition[-1]]
                            return_string = openai_instance.get_chat_completion(messages, model="gpt-4",
                                                                                max_tokens=400)
                        except openai.error:
                            # IF SECOND ATTEMPT DIDN'T WORK MAYBE RATE LIMIT HAS BEEN REACHED, CHANGE MODEL
                            return_string = openai_instance.get_chat_completion(messages,
                                                                                max_tokens=400)

                    # Add completion to current conversation
                    self.db.add_message("assistant", return_string)

                    # send ai feedback
                    self.send_text_message(return_string)

                    # send menu message with next options
                    button_list = [
                        ["next", "Volgende vraag➡"],
                        ["back", "Terug 🔙"],
                        ["0", "'Main menu'"]
                    ]

                    self.send_text_message_with_buttons(f""
                                                        f"Stuur asseblief "
                                                        f"enige vrae wat jy nog het, of stuur net "
                                                        f"nog 'n foto van jou volgende probeerslag indien "
                                                        f"jy nie enige vrae het nie. ❓📷", button_list)

                def mark_sum():

                    def get_student_final_answer(memo_answer):
                        def extract_param(data_, value):
                            arguments_str = data_["choices"][0]["message"]["function_call"]["arguments"]

                            # Convert the 'arguments' string to a dictionary
                            arguments_dict = eval(arguments_str)

                            # Extract values of a, b, and c
                            answer = arguments_dict[value].lower()

                            return answer

                        # Establish openAI connection
                        openai_instance = OpenAIAPI()

                        # give function and message context
                        functions_list = [
                            {
                                "name": "check_answer",
                                "description": "Compare the student's final answer to the correct final answer",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "student_final_answer": {
                                            "type": "string",
                                            "description": "A string that represents the student's final answer "
                                                           "or value to the maths problem"
                                        }
                                    }
                                }
                            }
                        ]
                        messages_ = [
                            {"role": "system", "content": f"You will be sent a student's attempt at a maths problem. "
                                                          f"Your job is to isolate the student's final answer. "
                                                          f"Then pass it as a paramater to the check_answer function. "
                                                          f"\nAlways save it in decimal form rounded "
                                                          "to 4 digits where applicable"},
                            {"role": "user", "content": self.message}
                        ]

                        # get feedback
                        data = openai_instance.get_chat_completion_with_function(messages_, functions_list,
                                                                                 use_gpt_4=True)

                        # extract necessary data from feedback
                        student_final_answer = extract_param(data, value="student_final_answer")

                        # Error logging
                        print(f"student's answer = {student_final_answer}")

                        return student_final_answer

                    def compare_final_answers(student_answer, memo_answer):

                        def extract_param(data_, value):
                            arguments_str = data_["choices"][0]["message"]["function_call"]["arguments"]

                            # Convert the 'arguments' string to a dictionary
                            arguments_dict = eval(arguments_str)

                            # Extract values of a, b, and c
                            is_correct_ = arguments_dict[value].replace(" ", "").lower()

                            if is_correct_ == "true":
                                is_correct_ = True
                            elif is_correct_ == "false":
                                is_correct_ = False
                            else:
                                print("Problem with gpt feedback at marksum, compare_final_answers, extract_param")
                                return None

                            return is_correct_

                        # establish openai connection
                        openai_instance = OpenAIAPI()

                        # give function and message context
                        functions_list = [
                            {
                                "name": "Give_feedback",
                                "description": "Give the student feedback based on his answer",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "is_correct": {
                                            "type": "string",
                                            "description": "Value of either True or False. True if the student's "
                                                           "answer corresponds to the memo's answer, otherwise False"
                                        }
                                    }
                                }
                            }
                        ]
                        messages_ = [
                            {"role": "system", "content": "You will be given a student's final answer to a maths "
                                                          "problem and the memo's final answer to a maths problem. "
                                                          "Compare the 2 answers. Then call the give feedback function "
                                                          "with the correct paramaters based on the memo and student answers"},
                            {"role": "user",
                             "content": f"Student's answer: {student_answer}\n\nMemo's answer: {memo_answer}"}
                        ]

                        # get feedback
                        data = openai_instance.get_chat_completion_with_function(messages_, functions_list,
                                                                                 use_gpt_4=True)

                        # error logging
                        print(data)

                        # extract necessary data
                        is_correct = extract_param(data, "is_correct")

                        return is_correct

                    def correct(question_streak_):
                        # update progress fields in db
                        self.db.set_question_streak(question_streak_[1:] + "1")

                        # debugging print
                        question_streak_ = self.db.get_question_streak()
                        print("post question streak: " + question_streak_)
                        print("post Question_attempt: " + str(self.db.get_topic_field("attempts")))

                        # Check if sub_topic needs to be updated
                        next_topic_maybe()

                        # reply to user
                        self.send_text_message("Goeie werk! 🥳🍾\nHier is jou volgende vraag:")
                        send_sum()

                    def incorrect(question_streak_):

                        def retrieve_checklist():
                            # get all necessary variables from db
                            current_topic_number = self.db.get_current_topic_number()
                            current_sub_topic_number = self.db.get_current_sub_topic_number()

                            # get applicable checklist for question
                            checklist_ = get_checklist(current_topic_number, current_sub_topic_number)

                            return checklist_

                        # Might use this function in the future with cheaper gpt tokens and asynchronous processing
                        def iterate_checklist():

                            def get_specific_solution(index_list):
                                specific_solution = ""
                                for line_index in index_list:
                                    specific_solution += solution.split("\n")[line_index]

                                return specific_solution

                            def extract_params(data_):

                                arguments_str = data_["choices"][0]["message"]["function_call"]["arguments"]

                                # Convert the 'arguments' string to a dictionary
                                arguments_dict = eval(arguments_str)

                                # Extract values
                                statement_number_1 = arguments_dict["statement_number"]
                                statement_satisfied = arguments_dict["statement_satisfied"].lower()
                                try:
                                    advice1 = arguments_dict["advice"]
                                except KeyError:
                                    advice1 = ""

                                if statement_satisfied == "true":
                                    statement_satisfied = True
                                elif statement_satisfied == "false":
                                    statement_satisfied = False
                                else:
                                    print("Problem with gpt feedback at marksum, compare_final_answers, extract_param")
                                    return None

                                return statement_number_1, statement_satisfied, advice1

                            statement_number, statement_valid, advice = "", "", ""
                            checklist = retrieve_checklist()
                            openai_instance_ = OpenAIAPI()
                            function_list = [
                                {
                                    "name": "student_feedback",
                                    "description": "Give the student feedback based on his answer",
                                    "parameters": {
                                        "type": "object",
                                        "properties": {
                                            "statement_number": {
                                                "type": "string",
                                                "description": "Number of the statement that was checked"
                                            },
                                            "statement_satisfied": {
                                                "type": "string",
                                                "description": "True is the student's answer did in fact satisfy"
                                                               " the question of the statement, False if the student"
                                                               " failed to get the statement correct."
                                            },
                                            "advice": {
                                                "type": "string",
                                                "description": "Empty if statement_satisfied is True else this is "
                                                               "where a description of how the student failed and"
                                                               " how he can prevent making the same mistake in the"
                                                               " future. (This is addressed directly to the student)"
                                                               " Also note the student is Afrikaans so the advice "
                                                               "should be in Afrikaans as well."
                                            }
                                        }
                                    }
                                }
                            ]
                            i = 1

                            for statement in checklist:
                                if len(statement) == 2:
                                    specific_solution = get_specific_solution(statement[1])
                                    messages_ = [
                                        {"role": "system", "content": f"You are a marking assistant."
                                                                      f"\n A student was presented"
                                                                      f" with the following problem:"
                                                                      f"{problem}"
                                                                      f"Please check if the student's "
                                                                      f"answer to the maths "
                                                                      f"problem satisfies the"
                                                                      f" following statement. "
                                                                      f"\n\n"
                                                                      f"Statement {i}: {statement[0]}\n\n "
                                                                      f"The correct solution to the statement "
                                                                      f"is: {specific_solution}"
                                                                      f"\n\n"
                                                                      f"Then call"
                                                                      f" the function student_feedback"
                                                                      f" with the appropriate"
                                                                      f" parameters."},
                                        {"role": "user", "content": self.message}
                                    ]
                                else:
                                    messages_ = [
                                        {"role": "system", "content": f"You are a marking assistant."
                                                                      f"\n A student was presented"
                                                                      f" with the following problem:"
                                                                      f"{problem}"
                                                                      f"Please check if the student's "
                                                                      f"answer to the maths "
                                                                      f"problem satisfies the"
                                                                      f" following statement. "
                                                                      f"\n\n"
                                                                      f"Statement {i}: {statement[0]}"
                                                                      f"\n\n"
                                                                      f"Then call"
                                                                      f" the function student_feedback"
                                                                      f" with the appropriate"
                                                                      f" parameters."},
                                        {"role": "user", "content": self.message}
                                    ]

                                data = openai_instance_.get_chat_completion_with_function(messages_, function_list,
                                                                                          True)
                                print(data)
                                statement_number, statement_valid, advice = extract_params(data)
                                print(f"statement number {statement_number} is {statement_valid}: {advice}")
                                if not statement_valid:
                                    break

                                i += 1

                            return statement_number, statement_valid, advice

                        def wrap_and_exclude_equations(paragraph_):
                            # This function neatly wraps all text but keeps
                            # equations to one line else it has display problems.

                            # separate equations
                            paragraph_list = paragraph_.split("$")

                            # loop through all equations
                            loop_length = round((len(paragraph_list)) / 2)
                            print(loop_length)
                            for i in range(loop_length):

                                if ((i * 2) + 1) >= len(paragraph_list):
                                    # exit loop of index out of range
                                    break

                                # replace all spaces with another character to
                                # keep equation from splitting over two lines when wrapping
                                equation = paragraph_list[(i * 2) + 1]
                                equation = equation.replace(" ", "&")

                                # encapsulate equation in $ signs again
                                equation = f"${equation}$"

                                # replace new equation into list
                                paragraph_list[(i * 2) + 1] = equation

                            # wrap text
                            paragraph_ = "".join(paragraph_list)
                            wrapped_paragraph_ = textwrap.fill(paragraph_, width=50, break_long_words=False)

                            # return & character to spaces
                            wrapped_paragraph_ = wrapped_paragraph_.replace("&", " ")

                            return wrapped_paragraph_

                        def generate_translated_latex_advice(include_solution=False):

                            # get checklist for maths problem
                            checklist = retrieve_checklist()

                            # create openai connection
                            openai_instance = OpenAIAPI()

                            # context (GENERATE ADVICE)
                            if include_solution:
                                messages = [
                                    {
                                        "role": "system",
                                        "content": f"A student was given the following mathematics problem: "
                                                   f"\n\n"
                                                   f"{problem}"
                                                   f"\n\n"
                                                   f"The student made a mistake. Please identify the mistake and provide"
                                                   f" advice on how to prevent the same mistakes in the future."
                                                   f"\n\n"
                                                   f"Here are a list of possible mistakes for you to check:"
                                                   f"\n\n"
                                                   f"{checklist}"
                                                   f"\n\n"
                                                   f"The next message from the user will be his/her attempt at solving"
                                                   f" the problem. "
                                                   f"\n\n"
                                                   f"Here is the solution: {solution}"
                                                   f"\n\n"
                                                   f"NB! You are now addressing the student"
                                                   f""
                                    },
                                    {
                                        "role": "user", "content": self.message
                                    }
                                ]
                            else:
                                messages = [
                                    {
                                        "role": "system",
                                        "content": f"A student was given the following mathematics problem: "
                                                   f"\n\n"
                                                   f"{problem}"
                                                   f"\n\n"
                                                   f"The student made a mistake. Please identify the mistake and provide"
                                                   f" advice on how to prevent the same mistakes in the future."
                                                   f"\n\n"
                                                   f"Here are a list of possible mistakes for you to check:"
                                                   f"\n\n"
                                                   f"{checklist}"
                                                   f"\n\n"
                                                   f"The next message from the user will be his/her attempt at solving"
                                                   f" the problem. "
                                                   f"\n\n"
                                                   f"NB! You are now addressing the student"
                                                   f""
                                    },
                                    {
                                        "role": "user", "content": self.message
                                    }
                                ]

                            # get completion (GENERATE ADVICE)
                            advice_string = str(
                                openai_instance.get_chat_completion(messages, model="gpt-4", max_tokens=400))

                            # context 2 (TRANSLATE TO AFRIKAANS)
                            messages_2 = [
                                {"role": "system", "content": "Please translate the following message into Afrikaans."},
                                {"role": "user", "content": advice_string}
                            ]

                            # completion 2 (TRANSLATE TO AFRIKAANS)
                            translated_advice_string = str(
                                openai_instance.get_chat_completion(messages_2, max_tokens=400))

                            # context 3 (FORMAT INTO LATEX)
                            messages_3 = [
                                {"role": "system", "content": "Please format all mathematical expressions or equations"
                                                              " into LaTeX format in the following string and"
                                                              " enclose each equation in '$' signs seperately."},
                                {"role": "user", "content": translated_advice_string}
                            ]

                            # completion 3 (FORMAT INTO LATEX)
                            formatted_advice_string_ = str(
                                openai_instance.get_chat_completion(messages_3, max_tokens=400))

                            # debugging print
                            print(f"before wrapping: {formatted_advice_string_}")

                            return formatted_advice_string_

                        def wrap_complete_text(formatted_advice_string_):
                            translated_string_list = formatted_advice_string_.split("\n")
                            wrapped_and_translated_advice_string_ = ""

                            for paragraph in translated_string_list:
                                wrapped_paragraph = wrap_and_exclude_equations(paragraph)
                                wrapped_and_translated_advice_string_ += f"\n{wrapped_paragraph}"

                            # REMOVE ANY POSSIBLE REDUNDANT $ SIGNS
                            wrapped_and_translated_advice_string_ = wrapped_and_translated_advice_string_.replace("$$",
                                                                                                                "$")

                            # DEBUGGING PRINT
                            print(f"after wrapping: {wrapped_and_translated_advice_string_}")

                            # save advice from AI in db
                            self.db.add_message("assistant", wrapped_and_translated_advice_string_)

                            return wrapped_and_translated_advice_string_

                        # get formatted completion
                        formatted_advice_string = generate_translated_latex_advice()

                        # WRAP TEXT WITH EQUATIONS ON ONE LINE
                        wrapped_and_translated_advice_string = wrap_complete_text(formatted_advice_string)

                        # GENERATE PICTURE FOR USER
                        generate_picture("", wrapped_and_translated_advice_string)

                        button_list = [
                            ["back", "Terug🔙"],
                            ["next", "Volgende vraag➡"],
                            ["solution", "Volledige Oplossing✍"]
                        ]

                        # send user message
                        self.send_output_image("")

                        # sleep bc picture takes longer for WA to process but we want it to arrive first
                        time.sleep(0.5)
                        self.send_text_message_with_buttons(f"Stuur asseblief "
                                                            f"enige vrae wat jy nog het, of kies nog sulke vraag om"
                                                            f" hierdie tipe vraag verder in te oefen. ❓📷", button_list)

                        # SET APPROPRIATE STATE
                        self.db.set_session_field("practice_state", "chat_on_problem")

                    def check_reply():

                        # Check if user used a button reply instead of answering the question
                        # method returns True if button reply was used otherwise false
                        if self.message.lower() == "next":
                            send_sum()
                            return True
                        elif self.message.lower() == "back":
                            self.db.set_session_field("handle_practice_menu_state", "start")
                            self.db.set_session_field("practice_state", "start")
                            topic = self.db.get_current_topic()
                            topic_progress = self.db.get_current_topic_progress()

                            message_text = f"\nJy was besig met {topic}📚 en sover het jy {topic_progress} voltooi. 📚"

                            self.send_text_message_with_buttons(message_text, bl_6)
                            return True
                        elif self.message.lower() == "solution":
                            def send_solution():
                                problem, solution = self.db.get_current_question()
                                generate_picture("", solution)
                                self.send_output_image("Hoop jy het dit reg gekry!")
                                time.sleep(0.5)
                                self.send_text_message_with_buttons("Wats volgende?", [["back", "Terug🔙"],
                                                                                       ["next", "Volgende vraag➡"],
                                                                                       ["solution",
                                                                                        "Volledige Oplossing✍"]])

                            send_solution()
                            return True
                        else:
                            return False

                    def initiate():
                        # get all necessary variables
                        problem_, solution_ = self.db.get_current_question()

                        # Isolate final answer on memo
                        memo_final_answer = solution_.split("\n")[-1]
                        print(f"memo_final_answer: {memo_final_answer}")

                        # Isolate the student's final answer
                        student_final_answer = get_student_final_answer(memo_final_answer)

                        # Compare
                        answer_is_correct_ = compare_final_answers(student_final_answer, memo_final_answer)
                        question_streak_ = self.db.get_question_streak()

                        return answer_is_correct_, question_streak_, problem_, solution_

                    # Check if user opted to a menu option
                    if check_reply():
                        # exit method
                        return

                    # initiate all necessary variables
                    answer_is_correct, question_streak, problem, solution = initiate()

                    # check verdict
                    if answer_is_correct is not None:
                        if answer_is_correct:
                            correct(question_streak)
                        else:
                            incorrect(question_streak)
                    else:
                        print("Error with feedback at compare final answers, marksum")
                        return

                # call appropriate handler based on practice_state
                practice_state_handlers = {
                    "start": send_sum,
                    "send_sum": send_sum,
                    "mark_sum": mark_sum,
                    "chat_on_problem": start_chat_on_current_problem
                }
                p_handler = practice_state_handlers.get(practice_state_1)
                if p_handler:
                    p_handler()
                else:
                    print("warning unhandled practice_state")

            # level 2
            def practice_state_2():
                # set appropriate handle_practice_menu_state
                self.db.set_session_field("handle_practice_menu_state", "practice_state")

                def send_sum():
                    # Get topic info from db
                    topic_number = self.db.get_current_topic_number()
                    current_sub_topic_number = self.db.get_current_sub_topic_number()

                    # generate problem based on retrieved info
                    problem, solution = generate_question(topic_number, current_sub_topic_number)

                    # save generated question to db
                    self.db.save_current_question(problem, solution)

                    # send problem to student
                    self.send_output_image("Sterkte! ✍️")
                    time.sleep(0.5)
                    self.send_text_message_with_buttons("Wat sal dit wees?", [["2", "Oplossing✍"],
                                                                              ["3", "Volgende tipe vraag⏭"],
                                                                              ["4", "Terug🔙"]])

                def send_solution():
                    problem, solution = self.db.get_current_question()
                    generate_picture("", solution)
                    self.send_output_image("Hoop jy het dit reg gekry!")
                    time.sleep(0.5)
                    self.send_text_message_with_buttons("Wats volgende?", [["1", "Nog sulke vraag☝🏻️"],
                                                                           ["3", "Volgende tipe vraag⏭"],
                                                                           ["4", "Terug 🔙"]])

                def next_sub_topic():
                    self.db.sub_topic_plus_one()
                    send_sum()

                def back():
                    self.db.set_session_field("handle_practice_menu_state", "start")
                    self.db.set_session_field("practice_state", "start")
                    topic = self.db.get_current_topic()

                    message_text = f"\nJy was besig met {topic}📚"

                    self.send_text_message_with_buttons(message_text, bl_6)

                # call appropriate handler based on practice_state
                message_handlers = {
                    "1": send_sum,
                    "2": send_solution,
                    "3": next_sub_topic,
                    "4": back
                }
                p_handler = message_handlers.get(self.message)
                if p_handler:
                    p_handler()
                else:
                    print("warning unhandled practice_state")

            # Level 2
            def select_topic():
                # set appropriate handle_practice_menu_state
                self.db.set_session_field("handle_practice_menu_state", "select_topic")

                # get appropriate select_topic state
                select_topic_state = self.db.get_session_field("select_topic_state")

                def st_start():
                    # set appropriate select_topic state
                    self.db.set_session_field("select_topic_state", "handle_initial_reply")
                    payment_status_ = self.db.get_user_field("payment_status")

                    # Get topic progress information from topic table
                    topic_list = ""
                    i = 1
                    for topic in topics_and_problems:
                        if payment_status_ == 1:
                            topic_percentage = self.db.get_topic_progress(i - 1)
                            # Added a book emoji for topics and a bar chart for progress
                            topic_list += f"{i}: 📚 *{topic[0]}* ---> \nJou huidige vordering is 📊 {topic_percentage}\n\n"
                        else:
                            topic_list += f"{i}: 📚 *{topic[0]}*\n\n"
                        i += 1

                    # send user message
                    # Added a pointing hand emoji to guide the user's choice
                    self.send_text_message(f"Kies asseblief 'n nommer uit die onderwerplys: 👉\n\n{topic_list}")

                def _handle_initial_reply():
                    # Validate message
                    choice = self.message
                    if choice.isdigit():
                        choice = int(self.message)

                        # Further Validate method
                        if 0 < choice < len(topics_and_problems) + 1:

                            # If message is validated set correct states
                            self.db.set_session_field("sub_state", "handle_practice_menu")
                            self.db.set_session_field("handle_practice_menu_state", "start")
                            self.db.set_session_field("select_topic_state", "start")

                            # update topic info in database
                            pre_change_topic_number = self.db.get_current_topic_number()
                            pre_change_sub_topic_number = self.db.get_current_sub_topic_number()
                            self.db.store_sub_topic_number(pre_change_topic_number, pre_change_sub_topic_number)

                            self.db.set_user_field("current_topic_number", choice - 1)
                            sub_topic_number = self.db.fetch_sub_topic_number(choice - 1)
                            self.db.set_user_field("current_sub_topic_number", sub_topic_number)

                            # retrieve new topic info
                            topic = self.db.get_current_topic()
                            topic_progress = self.db.get_current_topic_progress()

                            # send user message
                            if payment_status == 1:
                                message_text = f"✅ Dankie, ons het jou onderwerp verander na: " \
                                               f"\n📚 *{topics_and_problems[choice - 1][0]}*" \
                                               f"\n\n" \
                                               f"🔍 {topic_progress} " \
                                               f"\n\nOm voort te gaan, kies asseblief 'n opsie:"
                            else:
                                message_text = f"✅ Dankie, ons het jou onderwerp verander na: " \
                                               f"\n📚 *{topics_and_problems[choice - 1][0]}*" \
                                               f"\n\nOm voort te gaan, kies asseblief 'n opsie:"

                            self.send_text_message_with_buttons(message_text, bl_6)

                        # Handle unvalidated message
                        else:
                            # send user message
                            topic_list = ""
                            i = 1
                            for topic in topics_and_problems:
                                if payment_status == 1:
                                    topic_percentage = self.db.get_topic_progress(i - 1)
                                    topic_list += f"{i}: {topic[0]} ---> Jou huidige vordering is {topic_percentage}" \
                                                  f"\n\n"
                                else:
                                    topic_percentage = self.db.get_topic_progress(i - 1)
                                    topic_list += f"{i}: {topic[0]}" \
                                                  f"\n\n"
                                i += 1

                            self.send_text_message("Jammer, jou keuse maak nie sin nie. Probeer asseblief weer."
                                                   + f"\n\nKies asseblief 'n nommer uit die onderwerplys:"
                                                     f"\n\n {topic_list}")
                    else:
                        topic_list = ""
                        i = 1
                        for topic in topics_and_problems:
                            if payment_status == 1:
                                topic_percentage = self.db.get_topic_progress(i - 1)
                                topic_list += f"{i}: {topic[0]} ---> Jou huidige vordering is {topic_percentage}" \
                                              f"\n\n"
                            else:
                                topic_percentage = self.db.get_topic_progress(i - 1)
                                topic_list += f"{i}: {topic[0]}" \
                                              f"\n\n"
                            i += 1

                        self.send_text_message("Jammer, jou antwoord maak nie sin nie. Probeer asseblief weer."
                                               + f"\n\nKies asseblief 'n nommer uit die onderwerplys:\n\n {topic_list}")

                # Handle select_topic_state
                select_topic_state_handlers = {
                    "start": st_start,
                    "handle_initial_reply": _handle_initial_reply,
                }

                st_handler = select_topic_state_handlers.get(select_topic_state)
                if st_handler:
                    st_handler()
                else:
                    print("Warning Unhandled select_topic_State")

            # Level 2
            def get_inspiration():

                self.db.set_session_field("sub_state", "handle_practice_menu")
                self.db.set_session_field("handle_practice_menu_state", "start")
                # initiate OpenAi connection
                openai_instance = OpenAIAPI()

                # provide context
                messages = [
                    {"role": "system",
                     "content": "generate a helpful, playful, inspirational quote and message to a high school "
                                "learner that is "
                                "struggling with maths (the learner is Afrikaans so please generate your response in "
                                "Afrikaans)"},
                    {"role": "user", "content": "Hi, ek kort bietjie inspirasie om my te help om wiskunde te slaag"}
                ]

                # Get response
                response = openai_instance.get_chat_completion(messages, max_tokens=100)

                # send user message
                self.send_text_message(response)

                # get progress info from db
                topic = self.db.get_current_topic()
                topic_progress = self.db.get_current_topic_progress()
                payment_status_ = self.db.get_user_field("payment_status")

                # choose correct message
                if payment_status_ == 1:
                    message_text = f"Jy was besig met 📚{topic} en jy het sover {topic_progress} "
                else:
                    message_text = f"Jy was besig met 📚{topic}"

                # send message with menu again
                self.send_text_message_with_buttons(message_text, bl_6)

            # call the appropriate method based on the handle_practice_menu_state
            payment_status = self.db.get_user_field("payment_status")
            if payment_status == 1:
                handle_practice_menu_state_handlers = {
                    "start": start,
                    "practice_state": practice_state,
                    "select_topic": select_topic,
                    "get_inspiration": get_inspiration
                }
            else:
                handle_practice_menu_state_handlers = {
                    "start": start,
                    "practice_state": practice_state_2,
                    "select_topic": select_topic,
                    "get_inspiration": get_inspiration
                }

            state_handler = handle_practice_menu_state_handlers.get(handle_practice_menu_state)
            if state_handler:
                state_handler()
            else:
                print("unhandled state at handle_practice_menu")
                print(handle_practice_menu_state)

        # Level 3
        def handle_change_info_s():

            def add_parent_cell():
                # check if phone number valid
                validated, phone_number = _validate_phone_number(self.message)

                if validated:
                    # add phone number
                    payment_status = self.db.get_user_field("payment_status")

                    self.db.set_user_field("parent_phone", phone_number)
                    self.db.set_session_field("sub_state", "handle_initial_reply")

                    menulist = bl_5 if payment_status == 1 else bl_5_5

                    self.send_text_message_with_buttons("Dankie, ons het jou ouer se selfoon nommer gestoor!", menulist)
                else:
                    self.send_text_message_with_buttons("Askies, maar die selfoon nommer was nie geldig nie. "
                                                        "Asseblief stuur 'n geldige selfoon nommer of kies die"
                                                        " terug opsie.", bl_4)

            def back():
                # set appropriate states
                self.db.set_session_field("sub_state", "handle_initial_reply")
                payment_status = self.db.get_user_field("payment_status")

                # send user message
                message_text = f"Geen probleem, hoe kan ek nog help?🤔"
                menulist = bl_5 if payment_status == 1 else bl_5_5

                self.send_text_message_with_buttons(message_text, menulist)

            # Handle user reply
            if self.message == "3":
                back()
            else:
                add_parent_cell()

        def upgrade_pending():
            self.send_text_message_with_buttons(
                "Asseblief wag terwyl ons jou betaling prosesseer, of klik die terug opsie as jy van keuse verander"
                " het.", [["0", "Terug 🔙"]])

        # Handles sub_state
        sub_state_handlers = {
            "start": send_student_welcome_message,
            "handle_initial_reply": handle_initial_reply,
            "handle_practice_menu": handle_practice_menu,
            "handle_change_info_s": handle_change_info_s,
            "upgrade_student": upgrade_pending
        }

        # call appropriate sub_state handler
        handler = sub_state_handlers.get(self.sub_state)
        if handler:
            handler()
        else:
            print("warning unhandled student sub_state")

    # Connects to the Whatsapp API, send text message
    def send_text_message(self, message):
        phone_number = self.phone_number
        # print(message)

        wa_api = WhatsAppGraphAPI(phone_number)
        wa_api.send_text_message(message)

    def send_text_message_with_buttons(self, message, buttons_list):
        print("send_text_message with buttons is being reached")
        wa_api = WhatsAppGraphAPI(self.phone_number)

        response = None
        if len(buttons_list) == 3:
            print("3 button function being called")
            wa_api.send_text_message_3_buttons(message, buttons_list)
        elif len(buttons_list) == 2:
            response = wa_api.send_text_message_2_buttons(message, buttons_list)
        elif len(buttons_list) == 1:
            response = wa_api.send_text_message_1_button(message, buttons_list)
        else:
            print("button_list is not right")

        if response:
            print(response)

    # Connects to the Whatsapp API, sends document
    def send_document(self, name):

        connect_document_db(name, f"/tmp/{name}")

        wa_api = WhatsAppGraphAPI(self.phone_number)
        wa_api.send_whatsapp_media(media_path=f"/tmp/{name}", media_name=f"{name}", media_extension="pdf",
                                   media_type="application", param_type="DOCUMENT")
        # pass

    # Connects to the Whatsapp API, sends image of Maths Question
    def send_output_image(self, caption):
        wa_api = WhatsAppGraphAPI(self.phone_number)
        wa_api.send_whatsapp_media("/tmp/output.png", caption=caption)
        # pass
