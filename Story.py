from datetime import datetime


class Story:

    def __init__(self):

        self.messages = []
        self.start_time = datetime.now()

    def push_message(self, person, message):

        self.messages.append((person, message, datetime.now()))

    @staticmethod
    def datetime_to_string(date_object):

        return '{0}/{1}/{2} - {3}:{4}:{5}'.format(str(date_object.day).zfill(2), str(date_object.month).zfill(2),
                                                  str(date_object.year), str(date_object.hour).zfill(2),
                                                  str(date_object.minute).zfill(2), str(date_object.second).zfill(2))

    def save_as_txt(self, folder_name):

        filename = self.datetime_to_string(datetime.now())

        filename = filename.replace('/', ' ')
        filename = filename.replace(':', ' ')

        with open(folder_name + '/' + filename + '.txt', 'w+', encoding='utf-8') as file:

            file.write(self.datetime_to_string(self.start_time) + ' => ' +
                       self.datetime_to_string(datetime.now()) + '\n\n')

            for person, message, datetime_object in self.messages:

                file.write(self.datetime_to_string(datetime_object) + '\n')
                file.write('Osoba ' + person + ': ' + message + '\n\n')
