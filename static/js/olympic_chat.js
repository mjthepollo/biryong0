import { chatLimit, createLine, websocketProtocol } from "./chat.js";

const ChatSocket = new WebSocket(
  websocketProtocol + window.location.host + "/ws/chat/" + "olympic" + "/"
);

const BoxContainer = document.querySelector("#chats");
const goToBottom = function () {
  BoxContainer.scrollTop = BoxContainer.scrollHeight;
  let isAtBottom =
    BoxContainer.scrollHeight - BoxContainer.scrollTop ===
    BoxContainer.clientHeight;
  if (isAtBottom) {
    BoxContainer.scrollTop = BoxContainer.scrollHeight;
  }
};

ChatSocket.onmessage = function (e) {
  const type = JSON.parse(e.data).type;
  if (type === "talk") {
    const talk = JSON.parse(e.data).talk;
    const newTalk = createLine(talk);
    BoxContainer.appendChild(newTalk);
    if (BoxContainer.children.length > chatLimit) {
      BoxContainer.removeChild(BoxContainer.children[0]);
    }
    goToBottom();
  }
};

const ChatMessageInput = document.querySelector("#chat-message-input");
const ChatMessageSubmit = document.querySelector("#chat-message-sumbit");

ChatSocket.onclose = function (e) {
  console.error("채팅이 비정상적으로 종료됐습니다!");
};

if (ChatMessageInput) {
  ChatMessageInput.onkeypress = function (e) {
    if (e.keyCode === 13) {
      ChatMessageSubmit.click();
    }
  };
}

if (ChatMessageSubmit) {
  ChatMessageSubmit.onclick = function (e) {
    const message = ChatMessageInput.value;
    ChatSocket.send(
      JSON.stringify({
        type: "message",
        content: message,
      })
    );
    ChatMessageInput.value = "";
  };
}
