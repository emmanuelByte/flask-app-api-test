from validators.utils import ValidationFailure

def password(value: str, min_length=6, max_length=150, one_upper=False, one_lower=False, symbol=False, allowed_symbols=None):
    try:
        allowed_symbols = allowed_symbols or '$.-_+@&#'
        assert isinstance(value, str), "Password has to be a string"
        assert max_length >= len(value) >= min_length, "password should be between {} to {} characters".format(min_length, max_length)

        if one_upper:
            for c in value:
                if c.isupper():
                    break
            else:
                assert False, "There should be at least one uppercase character"

        if one_lower:
            for c in value:
                if c.islower():
                    break
            else:
                assert False, "There should be at least one lowercase character"

        if symbol:
            for c in value:
                if c in allowed_symbols:
                    break
            else:
                assert False, "There should be at least one symbol"

        return True
    except AssertionError as e:
        fail = ValidationFailure(password, dict(value=value, min_length=min_length, max_length=max_length, one_upper=one_upper, one_lower=one_lower, symbol=symbol, allowed_symbols=allowed_symbols))
        fail.message = e.args[0]
        return fail
