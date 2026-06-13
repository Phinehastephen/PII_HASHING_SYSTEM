from modules.database import get_connection


class UploadedFile:

    @staticmethod
    def create_file(
        filename,
        stored_filename,
        uploaded_by
    ):

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO uploaded_files
        (
            filename,
            stored_filename,
            uploaded_by
        )
        VALUES
        (%s,%s,%s)
        """

        cursor.execute(
            query,
            (
                filename,
                stored_filename,
                uploaded_by
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def get_all_files():

        conn = get_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute("""
        SELECT *
        FROM uploaded_files
        ORDER BY id DESC
        """)

        files = cursor.fetchall()

        cursor.close()
        conn.close()

        return files
    
    @staticmethod
    def update_status(
        file_id,
        status,
        records_processed
    ):

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        UPDATE uploaded_files
        SET
            status=%s,
            records_processed=%s
        WHERE id=%s
        """

        cursor.execute(
            query,
            (
                status,
                records_processed,
                file_id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()


    @staticmethod
    def get_file(
        file_id
    ):

        conn = get_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM uploaded_files
            WHERE id=%s
            """,
            (file_id,)
        )

        file = cursor.fetchone()

        cursor.close()
        conn.close()

        return file