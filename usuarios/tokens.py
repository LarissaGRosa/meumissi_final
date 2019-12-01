from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class UserTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        user_id = six.text_type(user.pk)
        ts = six.text_type(timestamp)
        is_active = six.text_type(user.is_active)
        context = {
            'user_id': user_id,
            'ts': ts,
            'is_active': is_active,
        }
        return context


user_tokenizer = UserTokenGenerator()