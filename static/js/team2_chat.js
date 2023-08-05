import { chatLimit, createLine, websocketProtocol } from "./chat.js";

const team2ChatSocket = new WebSocket(
  websocketProtocol + window.location.host + "/ws/chat/" + "team2" + "/"
);

const team2BoxContainer = document.querySelector("#team2_chat .chat-container");
const goToTeam2Bottom = function () {
  team2BoxContainer.scrollTop = team2BoxContainer.scrollHeight;
  let isAtBottom =
    team2BoxContainer.scrollHeight - team2BoxContainer.scrollTop ===
    team2BoxContainer.clientHeight;
  if (isAtBottom) {
    team2BoxContainer.scrollTop = team2BoxContainer.scrollHeight;
  }
};

team2ChatSocket.onmessage = function (e) {
  const type = JSON.parse(e.data).type;
  if (type === "talk") {
    const talk = JSON.parse(e.data).talk;
    const newTalk = createLine(talk);
    team2BoxContainer.appendChild(newTalk);
    if (team2BoxContainer.children.length > chatLimit) {
      team2BoxContainer.removeChild(team2BoxContainer.children[0]);
    }
    goToTeam2Bottom();
  }
};

team2ChatSocket.onclose = function (e) {
  console.error("채팅이 비정상적으로 종료됐습니다!");
};

const team2ChatMessageInput = document.querySelector(
  "#team2_chat .chat-message-input"
);
const team2ChatMessageSubmit = document.querySelector(
  "#team2_chat #chat-message-submit"
);

if (team2ChatMessageInput) {
  team2ChatMessageInput.onkeypress = function (e) {
    if (e.keyCode === 13) {
      team2ChatMessageSubmit.click();
    }
  };
}

if (team2ChatMessageSubmit) {
  team2ChatMessageSubmit.onclick = function (e) {
    const message = team2ChatMessageInput.value;
    team2ChatSocket.send(
      JSON.stringify({
        type: "message",
        content: message,
      })
    );
    team2ChatMessageInput.value = "";
  };
}
