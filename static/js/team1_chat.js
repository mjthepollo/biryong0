import { chatLimit, createLine, websocketProtocol } from "./chat.js";

const team1ChatSocket = new WebSocket(
  websocketProtocol + window.location.host + "/ws/chat/" + "team1" + "/"
);

const team1BoxContainer = document.querySelector("#team1_chat .chat-container");
const goToTeam1Bottom = function () {
  team1BoxContainer.scrollTop = team1BoxContainer.scrollHeight;
  let isAtBottom =
    team1BoxContainer.scrollHeight - team1BoxContainer.scrollTop ===
    team1BoxContainer.clientHeight;
  if (isAtBottom) {
    team1BoxContainer.scrollTop = team1BoxContainer.scrollHeight;
  }
};

team1ChatSocket.onmessage = function (e) {
  const type = JSON.parse(e.data).type;
  if (type === "talk") {
    const talk = JSON.parse(e.data).talk;
    const newTalk = createLine(talk);
    team1BoxContainer.appendChild(newTalk);
    if (team1BoxContainer.children.length > chatLimit) {
      team1BoxContainer.removeChild(team1BoxContainer.children[0]);
    }
    goToTeam1Bottom();
  }
};

team1ChatSocket.onclose = function (e) {
  console.error("채팅이 비정상적으로 종료됐습니다!");
};

const team1ChatMessageInput = document.querySelector(
  "#team1_chat .chat-message-input"
);
const team1ChatMessageSubmit = document.querySelector(
  "#team1_chat #chat-message-submit"
);

if (team1ChatMessageInput) {
  team1ChatMessageInput.onkeypress = function (e) {
    if (e.keyCode === 13) {
      team1ChatMessageSubmit.click();
    }
  };
}

if (team1ChatMessageSubmit) {
  team1ChatMessageSubmit.onclick = function (e) {
    const message = team1ChatMessageInput.value;
    team1ChatSocket.send(
      JSON.stringify({
        type: "message",
        content: message,
      })
    );
    team1ChatMessageInput.value = "";
  };
}
