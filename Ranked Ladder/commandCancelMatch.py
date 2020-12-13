import PlayerManager

def processCancelMatchMessage(parameters):
    if len(parameters) == 1:
        try:
            result = PlayerManager.cancelMatchAtIndex(parameters[0])
            return result
        except Exception as e:
            print(e)
            return ''
    else:
        return 'Invalid parameter count'