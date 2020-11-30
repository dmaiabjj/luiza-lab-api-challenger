DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def build_header(token):
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
