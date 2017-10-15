import requests
import config
from lxml import objectify
import logging

logger = logging.getLogger('recognize_speech')

def recognize(audio_buffer):
    response = requests.post('https://asr.yandex.net/asr_xml', params={
        'uuid': config.SPEECH_UUID,
        'key': config.YA_KEY,
        'topic': 'queries',
    }, headers={
        'Content-Type': 'audio/x-wav',
        # 'Transfer-Encoding': 'chunked',
    }, data=audio_buffer)



    logger.debug('XML response')
    logger.debug(response.content)

    recognition_results = objectify.fromstring(response.content)
    logger.debug(objectify.dump(recognition_results))

    if not recognition_results.get('success') == '1':
        return

    def dump_variant(variant):
        return {
            'text': variant.text,
            'confidence': variant.get('confidence')
        }

    return [dump_variant(v) for v in recognition_results.variant]
