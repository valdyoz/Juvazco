ADMIN_ACCOUNT = {
    'username': 'adminjuvazco',
    'email': 'adminjuvazco',
    'password': 'unesa',
    'nama': 'Admin Juvazco',
    'role': 'admin',
}

CUSTOMER_ACCOUNTS = [
    {
        'username': 'user1',
        'email': 'user1@gmail.com',
        'password': 'user1',
        'nama': 'Customer Satu',
        'role': 'customer',
    },
    {
        'username': 'user2',
        'email': 'user2@gmail.com',
        'password': 'user2',
        'nama': 'Customer Dua',
        'role': 'customer',
    },
]


def cek_login(username_or_email, password):
    data = username_or_email.strip().lower()

    if (data == ADMIN_ACCOUNT['username'].lower() or data == ADMIN_ACCOUNT['email'].lower()) and password == ADMIN_ACCOUNT['password']:
        return ADMIN_ACCOUNT

    for customer in CUSTOMER_ACCOUNTS:
        if (data == customer['username'].lower() or data == customer['email'].lower()) and password == customer['password']:
            return customer

    return None


def ambil_semua_user():
    return [ADMIN_ACCOUNT] + CUSTOMER_ACCOUNTS
