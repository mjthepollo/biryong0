const websocketProtocol =
  window.location.protocol === "https:" ? "wss://" : "ws://";

function createLine(talk) {
  const newTalk = document.createElement("div");
  newTalk.classList.add("chat-line");
  newTalk.innerHTML = `<span class="nickname" style="color:${talk.chat_name_color};">${talk.nickname}</span>${talk.message}</div>`;
  return newTalk;
}

const chatLimit = 200;

export { chatLimit, createLine, websocketProtocol };
