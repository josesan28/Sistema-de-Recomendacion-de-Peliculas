import bcrypt

class AuthController:
    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def check_password(hashed_password, input_password):
        return bcrypt.checkpw(
            input_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )

    @staticmethod
    def register_user(email, password, name=None):
        from controllers.user_controller import UserController
        hashed_pw = AuthController.hash_password(password)
        return UserController.create_user({
            "email": email,
            "password_hash": hashed_pw,
            "name": name
        })

    @staticmethod
    def authenticate_user(email, password):
        from controllers.user_controller import UserController
        user = UserController.get_user_by_email(email)
        if not user or not AuthController.check_password(user['hashed_password'], password):
            return None
        return user