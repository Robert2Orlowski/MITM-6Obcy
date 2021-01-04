from time import sleep

from Session import Session
from Story import Story


class Manager:

    def __init__(self, save_folder):

        self.session_1 = Session('1', 30)
        self.session_2 = Session('2', 30)
        self.save_folder = save_folder

    @staticmethod
    def transfer_session_info_to_story(identifier, message_list, story_obj: Story):

        for message in message_list:
            story_obj.push_message(identifier, message)

    @staticmethod
    def transfer_session_info_to_session(message_list, session_obj: Session):

        for message in message_list:
            session_obj.push_message(message)

    def run_once(self):

        self.session_1.restart_session()
        self.session_2.restart_session()

        story = Story()

        while self.session_1.is_connected() and self.session_2.is_connected():
            sleep(0.2)

            message_list_1 = self.session_1.get_local_messages()
            message_list_2 = self.session_2.get_local_messages()

            self.transfer_session_info_to_session(message_list_1, self.session_2)
            self.transfer_session_info_to_session(message_list_2, self.session_1)
            self.transfer_session_info_to_story(self.session_1.identifier, message_list_1, story)
            self.transfer_session_info_to_story(self.session_2.identifier, message_list_2, story)

            self.session_1.read_messages()
            self.session_2.read_messages()

            self.session_1.update_status()
            self.session_2.update_status()

        story.save_as_txt(self.save_folder)

    def run_once_and_exit(self):

        self.run_once()
        self.session_1.destroy_session()
        self.session_2.destroy_session()

    def run_multiple(self, tries):

        for _ in range(tries):
            self.run_once()

        self.session_1.destroy_session()
        self.session_2.destroy_session()

    def run_infinite(self):

        while True:
            self.run_once()
