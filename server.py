from typing import Type
from flask import Flask, jsonify, request
from flask.views import MethodView
from models import Session, Notification
from validation import CreateNotification
import pydantic
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)


class HttpError(Exception):
    def __init__(self, status_code: int, message: str | dict | list):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(er: HttpError):
    response = jsonify({'status': "error", 'message': er.message})
    response.status_code = er.status_code
    return response


def validate(validation_schema: Type[CreateNotification],
             json_data
             ):
    pydantic_obj = validation_schema(**json_data)
    try:
        return pydantic_obj.dict(exclude_none=True)
    except pydantic.ValidationError as er:
        raise HttpError(400, er.errors())


def get_notification(session: Session, notif_id: int):
    notif = session.get(Notification, notif_id)
    if notif is None:
        raise HttpError(404, "Notification not found")
    return notif


class NotificationViews(MethodView):

    # ПОЛУЧЕНИЕ ОБЪЯВЛЕНИЯ ПО "ID"
    def get(self, notif_id: int):
        with Session() as session:
            notif = get_notification(session, notif_id)
            return jsonify(
                {
                    "id": notif_id,
                    "title": notif.title,
                    "description": notif.description,
                    "owner": notif.owner
                }
            )

    # СОЗДАНИЕ ОБЪЯВЛЕНИЯ
    def post(self):
        validated_data = validate(CreateNotification, request.json)
        with Session() as session:
            new_notif = Notification(**validated_data)
            session.add(new_notif)
            try:
                session.commit()
            except IntegrityError as er:
                raise HttpError(409, "USER ALREADY EXIST")
            return jsonify({'id': new_notif.id})

    # УДАЛЕНИЕ ОБЪЯВЛЕНИЯ
    def delete(self, notif_id: int):
        with Session() as session:
            notific = session.delete(Notification, notif_id)
            return jsonify({"id": notific.id})


user_views = NotificationViews.as_view('notif')

app.add_url_rule('/notif/<int:notif_id>',
                 view_func=user_views,
                 methods=['GET', 'PATCH', 'DELETE'])

app.add_url_rule('/notif',
                 view_func=user_views,
                 methods=['POST'])

if __name__ == "__main__":
    app.run(debug=True)
    # gunicorn -b 0.0.0.0:5000 server:app --capture-output
