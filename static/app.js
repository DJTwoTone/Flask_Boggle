$guessForm = $('#guessForm');
$message = $('#msg');
$score = $('#score');
$gameNum = $('#gameNum');
$highScore = $('#highScore');

usedWords = []

$guessForm.on('submit', async function (e) {
    e.preventDefault();
    const guess = e.target[0].value
    const resp = await axios.get('/word_check', {params: {word: `${guess}`}})
    const points = guess.length;
    if (resp.data === 'ok' && usedWords.indexOf(guess) != 0) {
        keepingScore(points);
        usedWords.push(guess);
    }
    e.target[0].value = '';
    guessStatus(resp.data);

});

function guessStatus(msg) {
    $message.text('');
    $message.text(msg);
}

function keepingScore(points) {
    const oldScore = parseInt($score[0].innerText);
    const newScore = oldScore + points;
    $score.text(newScore);
}

$(function () {
    let $timer = $('#timer')
    if ($timer != undefined) {
        let remainingTime = parseInt($timer[0].innerText);
    }
    let bTimer = setInterval(function () {countdown()} , 1000);

    function countdown () {
        if (remainingTime === 0) {
            clearInterval(bTimer)
            $('form :input').prop('disabled', true);
            storeStatsEndGame();
            
        } else {
            remainingTime = remainingTime - 1;
            $timer.text(remainingTime);

        }
    }

})

async function storeStatsEndGame() {
     
    const currentScore = parseInt($score[0].innerText);
    const highScore = parseInt($highScore[0].innerText);
    let newHigh;
    if (currentScore > highScore) {
        newHigh = currentScore;
    } else {
        newHigh = highScore;
    }
    let games = parseInt($gameNum[0].innerText);

    games = games + 1;
 

    await axios.get('/end_game', {params: {high_score: `${newHigh}`, games_num: `${games}`, score: `${currentScore}`}})
}
