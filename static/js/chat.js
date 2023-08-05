const websocketProtocol =
  window.location.protocol === "https:" ? "wss://" : "ws://";

function createLine(talk) {
  const newTalk = document.createElement("div");
  newTalk.classList.add("chat-line");
  newTalk.innerHTML = `<div class="chat-line__left"><span class='nickname'>${talk.nickname}</span></div>
                          <div class="chat-line__right"><p class='message'>${talk.message}</p></div>`;
  return newTalk;
}

const chatLimit = 200;

export { chatLimit, createLine, websocketProtocol };
