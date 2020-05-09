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
    const oldScore = parseInt($score[0].textContent);
    const newScore = oldScore + points;
    $score.text(newScore);
}

// innerText => textContent

$(function () {
    let $timer = $('#timer')
    let remainingTime = parseInt($timer[0].textContent);
    
    let bTimer = setInterval(countdown, 1000);

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
     
    const currentScore = parseInt($score[0].textContent);
    const highScore = parseInt($highScore[0].textContent);
    let newHigh;
    if (currentScore > highScore) {
        newHigh = currentScore;
    } else {
        newHigh = highScore;
    }
    let game_num = parseInt($gameNum[0].textContent);

    game_num = game_num + 1;

    window.location.assign(`../end_game?high_score=${newHigh}&game_num=${game_num}&score=${currentScore}`);
}
