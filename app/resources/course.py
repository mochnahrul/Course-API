# third-party imports
from flask_restx import Resource, Namespace

# local imports
from .. import api, db
from ..models import Course, Student
from ..api_models import course_response_model, course_model


course_ns = Namespace("Course", path="/courses", description="Operations about Course")

@course_ns.route("")
class CourseList(Resource):
  @course_ns.marshal_list_with(course_response_model)
  def get(self):
    """Get a list of all courses."""
    courses = Course.query.all()
    return courses

  @course_ns.expect(course_model)
  @course_ns.marshal_with(course_response_model, code=201)
  def post(self):
    """Add a new course."""
    name = api.payload["name"]
    student_ids = api.payload["student_ids"]
    
    new_course = Course(name=name)

    # query for the students with the specified IDs
    associated_students = Student.query.filter(Student.id.in_(student_ids)).all()

    new_course.students = associated_students

    db.session.add(new_course)
    db.session.commit()
    return new_course, 201

@course_ns.route("/<int:id>")
@course_ns.doc(responses={404: "Course not found"}, params={"id": "Course ID"})
class CourseResource(Resource):
  @course_ns.marshal_with(course_response_model)
  def get(self, id):
    """Get course details by ID."""
    course = Course.query.get(id)
    if not course:
      api.abort(404, "Course with ID {} not found".format(id))
    return course

  @course_ns.expect(course_model)
  @course_ns.marshal_with(course_response_model)
  def put(self, id):
    """Update courses by ID."""
    course = Course.query.get(id)
    if not course:
      api.abort(404, "Course with ID {} not found".format(id))

    if "name" in api.payload:
      course.name = api.payload["name"]
    # update associated students
    if "student_ids" in api.payload:
      student_ids = api.payload["student_ids"]
      course.students = Student.query.filter(Student.id.in_(student_ids)).all()

    db.session.commit()
    return course

  @course_ns.doc(responses={204: "Course deleted"})
  def delete(self, id):
    """Delete courses by ID."""
    course = Course.query.get(id)

    if not course:
      api.abort(404, "Course with ID {} not found".format(id))

    db.session.delete(course)
    db.session.commit()
    return "", 204