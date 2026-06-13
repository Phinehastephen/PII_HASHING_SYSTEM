from modules.database import get_connection


class User:

    @staticmethod
    def find_by_username(username):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT * FROM users
        WHERE username = %s
        """

        cursor.execute(query, (username,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        return user

    @staticmethod
    def create_user(
        username,
        password,
        role
    ):

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO users
        (username,password,role)
        VALUES(%s,%s,%s)
        """

        cursor.execute(
            query,
            (
                username,
                password,
                role
            )
        )

        conn.commit()

        cursor.close()
        conn.close()