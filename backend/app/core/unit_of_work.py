from sqlmodel import Session


class UnitOfWork:

    def __init__(self, session: Session):

        self.session = session

    # =====================================================
    # ENTRADA AL CONTEXTO
    # =====================================================
    def __enter__(self):

        return self.session

    # =====================================================
    # SALIDA DEL CONTEXTO
    # =====================================================
    def __exit__(self, exc_type, exc_val, exc_tb):

        # =================================================
        # SI HUBO ERROR → ROLLBACK
        # =================================================
        if exc_type:

            self.session.rollback()

        # =================================================
        # SI TODO OK → COMMIT
        # =================================================
        else:

            self.session.commit()