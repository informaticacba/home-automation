from typeguard import typechecked

from repository.IftttRules import IftttRules
from event.ChangeActuatorRequestEvent import ChangeActuatorRequestEvent
from tools.TextToSpeech import TextToSpeech
from logging import RootLogger

class CommandExecutor:
    @typechecked()
    def __init__(self, change_actuator_request_event: ChangeActuatorRequestEvent, text_to_speech : TextToSpeech,
                 logging: RootLogger):
        self.__change_actuator_request_event = change_actuator_request_event
        self.__text_to_speech = text_to_speech
        self.__logging = logging

    @typechecked()
    def execute(self, command: dict) -> None:
        if command[IftttRules.COMMAND_VOICE] != '':
            self.__text_to_speech.say(command[IftttRules.COMMAND_VOICE])
            self.__logging.debug('Speaking text: {0}'.format(command[IftttRules.COMMAND_VOICE]))
        if command[IftttRules.COMMAND_ACTUATOR_NAME] != '':
            actuator_name = command[IftttRules.COMMAND_ACTUATOR_NAME]
            actuator_state = command[IftttRules.COMMAND_ACTUATOR_STATE]
            self.__logging.debug('Changing actuator {0} to state {1}'.format(actuator_name, actuator_state))
            self.__change_actuator_request_event.send(actuator_name, actuator_state)