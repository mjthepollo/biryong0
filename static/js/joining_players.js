const container = document.querySelector(".joining_players");
const joiningPlayersUrl = "/joining_players_json/";

function setPlayers() {
  fetch(joiningPlayersUrl)
    .then((data) => {
      return data.json();
    })
    .then((data) => {
      container.innerHTML = "";
      const joiningPlayersInfo = data["joining_players_info"];
      for (let i = 0; i < joiningPlayersInfo.length; i++) {
        const joiningPlayer = document.createElement("div");
        joiningPlayer.classList.add("joining_player");
        const thumbnail = document.createElement("img");
        thumbnail.src = joiningPlayersInfo[i]["thumbnail_image_url"];
        const nickname = document.createElement("span");
        nickname.innerHTML = joiningPlayersInfo[i]["nickname"];
        joiningPlayer.appendChild(thumbnail);
        joiningPlayer.appendChild(nickname);
        container.appendChild(joiningPlayer);
      }
      const overFive = data["over_five"];
      if (overFive) {
        const overFive = document.createElement("div");
        overFive.classList.add("over_five");
        overFive.innerHTML = data["over_five_text"];
        container.appendChild(overFive);
      }
    });
}

setPlayers();
setInterval(setPlayers, 5000);
