// Set selected options based on user preferences
document.addEventListener("DOMContentLoaded", function () {
    var numOpenQuestions = "{{ user.open_question_pref }}";
    var numTrueFalseQuestions = "{{ user.true_or_false_pref }}";
    var numClosedQuestions = "{{ user.closed_question_pref }}";

    document.getElementById("numOpenQuestions").value = numOpenQuestions;
    document.getElementById("numTrueFalseQuestions").value = numTrueFalseQuestions;
    document.getElementById("numClosedQuestions").value = numClosedQuestions;
});