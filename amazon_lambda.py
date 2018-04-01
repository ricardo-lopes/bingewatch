from __future__ import print_function
from bingewatch import setup_clear, setup_one_show, select_a_show

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    session_attributes = {}
    speech_output = "<speak>Please ask me what to watch next or to set up a new show.</speak>"
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(speech_output, None, should_end_session))


def handle_session_end_request():
    speech_output = "<speak>Giddyup!</speak>"
    should_end_session = True
    return build_response({}, build_speechlet_response(speech_output, None, should_end_session))


def reset(user_id):
    setup_clear(user_id)
    speech_output = "<speak>Your data has been reset. <break time=\"1s\"/> Please set up a new show.</speak>"
    should_end_session = False
    return build_response({}, build_speechlet_response(speech_output, None, should_end_session))


def set_up_show(user_id, tv_show_slot):
    speech_output = "<speak>Something went wrong. Can you try again, please?</speak>"
    should_end_session = False
    result = setup_one_show(user_id, tv_show_slot)
    if result:
        speech_output = f"<speak>I have setup {result} and sprinkled a little more</speak>"
    return build_response({}, build_speechlet_response(speech_output, None, should_end_session))


def select_show(user_id):
    speech_output = "<speak>Something went wrong. Can you try again, please?</speak>"
    should_end_session = False
    show = select_a_show(user_id)
    if show:
        speech_output = f"<speak>Hmmmmmmmmm. <break time=\"1s\"/>  I think you should watch {show}</speak>"
    return build_response({}, build_speechlet_response(speech_output, None, should_end_session))


# --------------- Specific Events ------------------

def on_intent(intent_request, session, user_id):
    print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])
    intent_name = intent_request['intent']['name']
    if intent_name == "ResetIntent":
        return reset(user_id)
    if intent_name == "SetupShowIntent":
        tv_show_slot = intent_request['intent']['slots']['tvshow']['value']
        return set_up_show(user_id, tv_show_slot)
    if intent_name == "SelectShowIntent":
        return select_show(user_id)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


# --------------- Generic Events ------------------

def on_session_started(session_started_request, session):
    print(
        "on_session_started requestId=" + session_started_request['requestId'] + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])
    return get_welcome_response()


def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])


# --------------- Main handler ------------------

def lambda_handler(event, context):
    print("event.session.application.applicationId=" + event['session']['application']['applicationId'])
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']}, event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        user_id = event['session']['user']['userId']
        return on_intent(event['request'], event['session'], user_id)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
