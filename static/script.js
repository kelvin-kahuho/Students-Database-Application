document.getElementById('searchForm').onsubmit = function() {
    const studentId = document.getElementById('student_id_input').value;
    const actionUrl = `/student/${encodeURIComponent(studentId)}`;
    this.action = actionUrl;
};
