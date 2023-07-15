def clear_verification_code(user):
    user.verification_code = ''
    user.save()