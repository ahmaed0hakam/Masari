from flask import jsonify, request
from flask_login import login_required, current_user
from app import app, db, llm
from app.models.models import LearningPaths, Courses, Lessons
from app.utils.helpers import parse_prompt

@app.route('/api/generate_learningpath', methods=['POST'])
@login_required
def generate_learning_path():
    try:
        request_data = request.get_json()
        lp_title = request_data.get('text')

        prompt_template = """
        You are creating a personalized learning path for a user interested in {lp_title}. 
        Please provide the courses names only, ordered based on difficulty and correct ordering in the learning path, no another text in the string, only the courses names:

        ## **Generate Output**:
        Format the output to list only the names of the recommended courses under the header Personalized Learning Path: [Learning Path Name].
        Ensure the output adheres strictly to the format provided, without including any descriptive text, comments, or conversational elements.

        ## **Output Format:**
        ```
        # Personalized Learning Path: [Learning Path Name]
        1. [Course Name 1]
        2. [Course Name 2]
        3. (repeat as necessary for additional courses)
        ```
        """

        prompt = prompt_template.format(lp_title=lp_title)
        response_llm = llm.invoke(prompt)
        courses_titles = parse_prompt(response_llm)
        
        new_path = LearningPaths(title=lp_title, user_id=current_user.id)
        db.session.add(new_path)
        db.session.commit()

        for course in courses_titles:
            new_course = Courses(title=course, learning_path_id=new_path.id)
            db.session.add(new_course)
            db.session.commit()

        return jsonify({'id': new_path.id}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate_lessons', methods=['POST'])
@login_required
def generate_lessons():
    try:
        request_data = request.get_json()
        course_title = request_data.get('course_title')
        course_id = request_data.get('course_id')

        existing_lesson = Lessons.query.filter_by(course_id=course_id).first()
        if existing_lesson:
            return jsonify({'id': course_id, 'course_title': course_title}), 201

        learning_paths = current_user.learning_paths
        lesson_prompt_template = """
        # Generating a Personalized Lessons 
        You are creating a course for a user interested in learning about {course_title}, This course from this learning paths {learning_paths}. 
        Please provide proper number of lesson titles that would be suitable for this course, and no other text, just lessons tiles, each prefixed with a number, don't write anything else.

        ## **Generate Output**:
        Format the output to list only the names of the recommended lessons title from course {course_title} under the header Personalized Lessons Of Course: {course_title}.
        Ensure the output adheres strictly to the format provided, without including any descriptive text, comments, or conversational elements.

        ## **Output Format:**
        ```
        # Personalized Learning Path: [Course Name]
        1. [Lesson Name 1]
        2. [Lesson Name 2]
        3. (repeat as necessary for additional Lessons)
        ```
        """

        prompt = lesson_prompt_template.format(course_title=course_title, learning_paths=learning_paths)
        response_llm = llm.invoke(prompt)
        lesson_titles = parse_prompt(response_llm)

        for lesson_title in lesson_titles:
            new_lesson = Lessons(title=lesson_title, course_id=course_id)
            db.session.add(new_lesson)
            db.session.commit()

        return jsonify({'id': course_id, 'course_title': course_title}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate_content', methods=['POST'])
@login_required
def generate_content():
    request_data = request.get_json()
    lesson_title = request_data.get('lesson_title')
    course_title = request_data.get('course_title')
    lesson_id = request_data.get('lesson_id')

    existing_content = Lessons.query.filter_by(id=lesson_id).first().content
    if existing_content:
        return jsonify({'content': existing_content}), 200

    content_prompt_template = f"""
    Lesson: {lesson_title}"

    Lesson Overview:
    In this lesson, we will delve into the key topics related to "{lesson_title}" in "{course_title}", Please provide detailed content covering the following aspects within the course "{course_title}":

    Key Topics to Cover:
    1. 
    2. 
    3. 

    **Examples and Explanations:**
    - Please include illustrative examples to clarify the concepts.
    - Provide detailed explanations to ensure comprehension.

    **Exercises:**
    - Develop exercises or problems related to the lesson topics.
    - Include solutions or hints where applicable.

    **Additional Notes:**
    Feel free to add any additional insights or details that would enhance this lesson.
    
    **Instructions:**
    - Do not use (Here Markdown) or (Here XYZ) or any form of conversations just give me the content without any additional conversations   
    - Design a Markdown template focusing on individual lessons within a course.
    """

    response_llm = llm.invoke(content_prompt_template)
    response_llm = response_llm.replace("```html", "").replace("```", "").strip()
    
    current_lesson = Lessons.query.get(lesson_id)
    if current_lesson:
        current_lesson.content = response_llm
        db.session.commit()
        return jsonify({'content': response_llm}), 200
    else:
        return jsonify({'message': 'Lesson not found'}), 404

@app.route('/api/generate_reply', methods=['POST'])
@login_required
def generate_reply():
    request_data = request.get_json()
    user_input = request_data.get('user_input')
    lesson_id = request_data.get('lesson_id')
    content = Lessons.query.get(lesson_id).content

    context_template = f"""
    You are a learning assistant designed to provide accurate and helpful information. 
    Please use the following details to answer the question provided as short as possible, max to 20 character. 
    If you're unsure about any details, it's important to be honest and precise rather than guessing.

    *Instructions:*
    - Do not use (Here XYZ) or any form of conversations just give me the Answer without any additional conversations  

    Depend on this content and your information:
    
    {content}

    Answer this question:
    Question: {user_input}

    Helpful Answer:"""

    response_llm = llm.invoke(context_template)
    return jsonify({'reply': response_llm}), 200

@app.route('/api/mark_completed', methods=['POST'])
@login_required
def mark_completed():
    request_data = request.get_json()
    lesson_id = request_data.get('lesson_id')

    current_lesson = Lessons.query.get(lesson_id)
    if current_lesson:
        current_lesson.completed = 1
        db.session.commit()
        return jsonify({'message': f"lesson {lesson_id} completed"}), 200 