import secrets
from models import get_all_tokens_db, get_all_classes


def generate_token(length=5):
    token = secrets.token_hex(length)

    all_tk = get_all_tokens_db()

    if token in all_tk:
        generate_token()
    else:
        return token


def get_all_class_service():
    all_cls = []
    try:
        for i in get_all_classes():
            all_cls.append(str(i).strip("(),'"))

        return all_cls
    except Exception as e:
        print(f"Error service - {e}")

