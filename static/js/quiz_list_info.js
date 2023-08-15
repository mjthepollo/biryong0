const quizs = document.querySelector(".quizs");
const top3Players = document.querySelector(".top3_players");
const otherPlayers = document.querySelector(".other_players");
const quizinfoUrl = "/quiz/info/";

function setPlayers() {
  fetch(quizinfoUrl)
    .then((data) => {
      return data.json();
    })
    .then((data) => {
      top3Players.innerHTML = "";
      const top3PlayersInfo = data["top3_players_info"];
      for (let i = 0; i < top3PlayersInfo.length; i++) {
        const top3Player = document.createElement("div");
        top3Player.classList.add("top3_player");
        const rank = document.createElement("div");
        rank.classList.add("rank");
        rank.innerHTML = `${i + 1}등`;
        const thumbnail = document.createElement("img");
        thumbnail.src = top3PlayersInfo[i]["thumbnail_image_url"];
        const nickname = document.createElement("span");
        nickname.classList.add("nickname");
        nickname.innerHTML = top3PlayersInfo[i]["nickname"];
        const playerScore = document.createElement("span");
        playerScore.classList.add("player_score");
        playerScore.innerHTML = top3PlayersInfo[i]["solved_point"];
        top3Player.appendChild(rank);
        top3Player.appendChild(thumbnail);
        top3Player.appendChild(nickname);
        top3Player.appendChild(playerScore);
        top3Players.appendChild(top3Player);
      }

      otherPlayers.innerHTML = "";
      const otherPlayersInfo = data["other_players_info"];
      for (let i = 0; i < otherPlayersInfo.length; i++) {
        const otherPlayer = document.createElement("div");
        otherPlayer.classList.add("other_player");
        const thumbnail = document.createElement("img");
        thumbnail.src = otherPlayersInfo[i]["thumbnail_image_url"];
        const nickname = document.createElement("span");
        nickname.innerHTML = otherPlayersInfo[i]["nickname"];
        const playerScore = document.createElement("span");
        playerScore.classList.add("player_score");
        playerScore.innerHTML = top3PlayersInfo[i]["solved_point"];
        otherPlayer.appendChild(thumbnail);
        otherPlayer.appendChild(nickname);
        otherPlayer.appendChild(playerScore);
        otherPlayers.appendChild(otherPlayer);
      }

      const solvedQuizsPk = data["solved_quizs_pk"];
      const allQuizs = document.querySelectorAll(".quiz");
      for (let i = 0; i < allQuizs.length; i++) {
        const quizPk = allQuizs[i].dataset.pk;
        if (solvedQuizsPk.includes(parseInt(quizPk))) {
          allQuizs[i].classList.add("solved");
        }
      }
    });
}

setPlayers();
setInterval(setPlayers, 5000);
