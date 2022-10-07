function report(order) {
    if (order=="") return;
    if (order=="ascending") window.location.replace("/ascending");
    if (order=="descending") window.location.replace("/descending")
    if (order=="random") window.location.replace("/random");
}

function sendQuizID(quizID) {
    xhr = new XMLHttpRequest();
    xhr.open('POST', '/setCookie');

    /*
    xhr.responseType = 'json';
    xhr.setRequestHeader('Content-Type', 'application/json');
    */
    xhr.send(quizID);

    document.getElementById(quizID).remove()
}

function hideOverlay(){
    document.getElementById("overlay").style.display = "none";
    document.getElementById("hiddenQuizList").style.display = "none";
}

function showHiddenQuizList(){
    document.getElementById("overlay").style.display = "block";
    document.getElementById("hiddenQuizList").style.display = "block";
}

function unhideQuiz(quizUrl){
    xhr = new XMLHttpRequest();
    xhr.open('POST', '/removeFromHidden');

    xhr.send(quizUrl)
    document.getElementById(quizUrl).remove()
}