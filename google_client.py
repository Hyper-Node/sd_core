from conditional_print import ConditionalPrint
from configuration_handler import ConfigurationHandler

# Imports the Google Cloud client library
from google.cloud import translate
from google.oauth2 import service_account


class GoogleClient(object):

    def __init__(self):
        config_handler = ConfigurationHandler(first_init=False)

        self.config = config_handler.get_config()
        self.cpr = ConditionalPrint(self.config.PRINT_GOOGLE_CLIENT, self.config.PRINT_EXCEPTION_LEVEL,
                                    self.config.PRINT_WARNING_LEVEL, leading_tag=self.__class__.__name__)

        self.cpr.print("init GoogleClient")

        # Get the credentials
        credentials = service_account.Credentials.from_service_account_file(self.config.GOOGLE_CLIENT_API_KEY_PATH)
        # Instantiates a client
        self.translate_client = translate.Client(credentials=credentials)
        self.target_lang = 'de'
        self.source_lang = 'en'
        self.TEXT_SEQ_LIMIT = 64  # for each request there's a maximum of texts to translate

    def do_translate_text_batch(self, texts):
        """
        Batch-wise sends some array of texts to google-translate api and get's the result
        TEXT_SEQ_LIMIT is considered for batch-size
        :param texts:
        :return:
        """
        all_translation = []

        my_batch = []
        my_batch_was_sent = False
        for text_index, text in enumerate(texts):
            my_batch.append(text)
            my_batch_was_sent = False

            if (text_index != 0) and ((text_index+1) % self.TEXT_SEQ_LIMIT == 0): # for multiples of limit
                # send rqs
                translation = self.translate_client.translate(
                    my_batch, target_language=self.target_lang, source_language=self.source_lang)
                all_translation.extend(translation)
                my_batch_was_sent = True
                my_batch = []  # clear batch

        if my_batch_was_sent is False:
            # send last batch
            translation = self.translate_client.translate(
                my_batch, target_language=self.target_lang, source_language=self.source_lang)
            all_translation.extend(translation)

        return all_translation


