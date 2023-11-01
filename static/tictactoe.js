const PLAYER_1 = 'X'
const PLAYER_2 = 'O'

let currentPlayer = PLAYER_1;

let board = [
    ['','',''],
    ['','',''],
    ['','',''],
]

function resetBoard() {
    board = [
    ['','',''],
    ['','',''],
    ['','',''],
];
}

function makeMove(x, y) {
    if (board[x][y] !== '') {
        alert('Invalid move!')
        return;
    }
    board[x][y] = currentPlayer;

    displayBoard();
    if (winCondition()) {
        alert('Igra končana!');
        resetBoard();
    } else {
        switchPlayer();
    }
}

function switchPlayer() {
    if(currentPlayer == PLAYER_1) {
        currentPlayer = PLAYER_2;
    } else {
        currentPlayer = PLAYER_1;
    }
}

function displayBoard() {
    document.getElementById('box0-0').innerHTML = board[0][0];
    document.getElementById('box0-1').innerHTML = board[0][1];
    document.getElementById('box0-2').innerHTML = board[0][2];

    document.getElementById('box1-0').innerHTML = board[1][0];
    document.getElementById('box1-1').innerHTML = board[1][1];
    document.getElementById('box1-2').innerHTML = board[1][2];

    document.getElementById('box2-0').innerHTML = board[2][0];
    document.getElementById('box2-1').innerHTML = board[2][1];
    document.getElementById('box2-2').innerHTML = board[2][2];
}

function winCondition() {
    if (board[0][0] !== '' && board[0][0] == board[0][1] && board[0][1] == board[0][2] ||
        board[1][0] !== '' && board[1][0] == board[1][1] && board[1][1] == board[1][2] ||
        board[2][0] !== '' && board[2][0] == board[2][1] && board[2][1] == board[2][2]) {
            alert('Zmaga po vrstici!')
            return true;
    } else if (
    board[0][0] !== '' && board[0][0] == board[1][0] && board[1][0] == board[2][0] ||
    board[0][1] !== '' && board[0][1] == board[1][1] && board[1][1] == board[2][1] ||
    board[0][2] !== '' && board[0][2] == board[1][2] && board[1][2] == board[2][2]) {
        alert('Zmaga po stolpcu!')
        return true
    } else if (
    board[0][0] !== '' && board[0][0] == board[1][1] && board[1][1] == board[2][2] ||
    board[0][2] !== '' && board[0][2] == board[1][1] && board[1][1] == board[2][0]) {
        alert('Zmaga po diagonali!')
        return true;
    } else if (
    board[0][0] && board[0][1] && board[0][2] &&
    board[1][0] && board[1][1] && board[1][2] &&
    board[2][0] && board[2][1] && board[2][2] !== '') {
        alert('Ni zmagovalca!')
        return true;
    }
    return false;
}
