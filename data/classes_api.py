import flask
from flask import jsonify, request
from . import db_session
from .students import Student


blueprint = flask.Blueprint(
    'classes_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/news/<int:id_class>', methods=['GET'])
def get_one_news(id_class):
    db_sess = db_session.create_session()
    students = db_sess.query(Student).filter(Student.id_class == id_class)
    if not news:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'news': news.to_dict(only=(
                'title', 'content', 'user_id', 'is_private'))
        }
    )
