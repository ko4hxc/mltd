# from mltd import threads


FAKE_MESSAGE_TEXT = "fake MeSSage"
FAKE_FROM_CALLSIGN = "KFAKE"
FAKE_TO_CALLSIGN = "KMINE"


def fake_packet(
    fromcall=FAKE_FROM_CALLSIGN,
    tocall=FAKE_TO_CALLSIGN,
    message=None,
    msg_number=None,
    message_format=core.PACKET_TYPE_MESSAGE,
    response=None,
):
    packet_dict = {
        "from": fromcall,
        "addresse": tocall,
        "to": tocall,
        "format": message_format,
        "raw": "",
    }
    if message:
        packet_dict["message_text"] = message

    if msg_number:
        packet_dict["msgNo"] = str(msg_number)

    if response:
        packet_dict["response"] = response

    return core.factory(packet_dict)


