def logger(user, event, msgid, eventtime, reaction = None):
    if reaction:
        print(user, event, reaction, 'on message ID,', msgid, 'at', eventtime)
    else:
        print(user, event, 'message ID,', msgid, 'at', eventtime)

def edit_logger(user, msgid, eventtime, before, after):
    print(user, 'edited', 'message ID,', msgid, 'at', eventtime, 'from', before, 'to', after) 