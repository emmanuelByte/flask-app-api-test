def restify(success: bool, message: str, data=None, meta=None, error_code=None, errors=None):
    assert isinstance(success, bool)
    assert isinstance(message, str)

    resp = {
        'success': bool(success),
        'message': str(message),
    }
    if data != None:
        assert isinstance(data, dict)
        resp['data'] = data

    if meta != None:
        assert isinstance(meta, dict)
        resp['meta'] = meta

    if errors != None:
        assert isinstance(errors, dict)
        resp['errors'] = errors

    if error_code != None:
        resp['error_code'] = error_code
    
    return resp