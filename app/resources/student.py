# third-party imports
from flask_restx import Resource, Namespace

# local imports
from .. import api, db
from ..models import Student
from ..api_models import student_response_model, student_model


student_ns = Namespace("Student", path="/students", description="Operations about Student")

@student_ns.route("")
class StudentList(Resource):
  @student_ns.marshal_list_with(student_response_model)
  def get(self):
    """Get a list of all students."""
    students = Student.query.all()
    return students

  @student_ns.expect(student_model)
  @student_ns.marshal_with(student_response_model, code=201)
  def post(self):
    """Add a new student."""
    new_student = Student(**api.payload)
    db.session.add(new_student)
    db.session.commit()
    return new_student, 201

@student_ns.route("/<int:id>")
@student_ns.doc(responses={404: "Student not found"}, params={"id": "Student ID"})
class StudentResource(Resource):
  @student_ns.marshal_with(student_response_model)
  def get(self, id):
    """Get student details by ID."""
    student = Student.query.get(id)
    if not student:
      api.abort(404, "Student with ID {} not found".format(id))
    return student

  @student_ns.expect(student_model)
  @student_ns.marshal_with(student_response_model)
  def put(self, id):
    """Update students by ID."""
    student = Student.query.get(id)
    if not student:
      api.abort(404, "Student with ID {} not found".format(id))

    if "name" in api.payload:
      student.name = api.payload["name"]

    db.session.commit()
    return student

  @student_ns.doc(responses={204: "Student deleted"})
  def delete(self, id):
    """Delete students by ID."""
    student = Student.query.get(id)
    if not student:
      api.abort(404, "Student with ID {} not found".format(id))
    db.session.delete(student)
    db.session.commit()
    return "", 204