from time import sleep, time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoAlertPresentException


class Session:

    def __init__(self, identifier, response_time_limit):

        self.identifier = identifier

        self.stored_local_message_list = []  # messages coming from foreigner of THIS session
        self.stored_incoming_message_list = []  # messages coming from second session

        self.driver = webdriver.Chrome()

        self.last_message_time = time()
        self.status = 'disconnected'

        self.response_time_limit = response_time_limit

    def restart_session(self):

        self.stored_local_message_list.clear()
        self.stored_incoming_message_list.clear()

        self.driver.get('https://6obcy.org/rozmowa')

        try:

            alert = self.driver.switch_to.alert
            alert.accept()

        except NoAlertPresentException:

            print('No alert')

        self.status = 'connected'
        self.last_message_time = time()

    def push_message(self, message_text):

        self.stored_incoming_message_list.append(message_text)
        self.last_message_time = time()

    def read_messages(self):

        if self.stored_incoming_message_list and self.status == 'connected':

            input_box = self.driver.find_element_by_id('box-interface-input')

            try:

                for msg in self.stored_incoming_message_list:
                    input_box.send_keys(msg)
                    input_box.send_keys(Keys.RETURN)

            except ElementNotInteractableException:

                print('User unable to enter the message into input box.')

            self.stored_incoming_message_list.clear()

    def get_local_messages(self):

        show_elements = self.driver.find_elements_by_class_name('show')

        for element in show_elements:

            try:
                element.click()
            except ElementNotInteractableException:
                print('User unable to click the SHOW MORE button.')

        current_message_list = [answer.text for answer in self.driver.find_elements_by_class_name('log-stranger')]
        current_message_list = [msg.replace('Obcy: ', '') for msg in current_message_list]
        current_message_list = [msg.replace('(Schowaj)', '') for msg in current_message_list]

        new_messages = current_message_list[len(self.stored_local_message_list):]

        if len(self.stored_local_message_list) != len(current_message_list):
            self.stored_local_message_list = current_message_list

        return new_messages

    def update_status(self):

        if time() - self.last_message_time > self.response_time_limit:
            self.status = 'unavailable'

        disconnection_infos = [info.text for info in self.driver.find_elements_by_class_name('log-disconnected')]

        if any(info in ['Rozłączyłeś się', 'Obcy się rozłączył'] for info in disconnection_infos):
            self.status = 'disconnected'

    def is_connected(self):

        return True if self.status == 'connected' else False

    def destroy_session(self):

        self.driver.quit()
