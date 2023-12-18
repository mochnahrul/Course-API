# third-party imports
from flask_restx import Resource, Namespace

# local imports
from .. import api, db
from ..models import Student
from ..api_models import student_response_model, student_model
from ..utils import generate_response


student_ns = Namespace("Student", path="/student", description="Operations about Student")

@student_ns.route("")
@student_ns.doc(responses={200: "OK", 201: "Created", 400: "Bad Request"})
class StudentList(Resource):
  def get(self):
    """Get a list of all students."""
    students = Student.query.all()
    return generate_response(200, "Request processed successful", api.marshal(students, student_response_model)), 200

  @student_ns.expect(student_model)
  def post(self):
    """Add a new student."""
    # check if the name is already in use
    existing_student_name = Student.query.filter_by(name=api.payload["name"]).first()
    if existing_student_name:
      return generate_response(400, "Name is already in use"), 400

    new_student = Student(**api.payload)
    db.session.add(new_student)
    db.session.commit()
    return generate_response(201, "Student created successful", api.marshal(new_student, student_response_model)), 201

@student_ns.route("/<int:id>")
@student_ns.doc(responses={200: "OK", 204: "No Content", 400: "Bad Request", 404: "Not Found"}, params={"id": "Student ID"})
class StudentResource(Resource):
  def get(self, id):
    """Get student by ID."""
    student = Student.query.get(id)
    if not student:
      return generate_response(404, "Student not found"), 404
    return generate_response(200, "Request processed successful", api.marshal(student, student_response_model)), 200

  @student_ns.expect(student_model)
  def put(self, id):
    """Update students by ID."""
    student = Student.query.get(id)
    if not student:
      return generate_response(404, "Student not found"), 404

    # check if the new name is already in use
    existing_student_name = Student.query.filter_by(name=api.payload["name"]).first()
    if existing_student_name and existing_student_name.id != id:
      return generate_response(400, "Name is already in use"), 400
    student.name = api.payload["name"]

    db.session.commit()
    return generate_response(200, "Student updated successful", api.marshal(student, student_response_model)), 200

  def delete(self, id):
    """Delete students by ID."""
    student = Student.query.get(id)
    if not student:
      return generate_response(404, "Student not found"), 404

    db.session.delete(student)
    db.session.commit()
    return generate_response(204, "Student deleted successful", api.marshal(student, student_response_model)), 204