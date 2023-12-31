alert(
  "SmallTalk는 잡담을 나누는 공간입니다!\n1시간이 지난 채팅은 이후 접속한 사람은 볼 수 없게 되니 현재 같이 얘기를 나누는 사람들과 마음 놓고 얘기하시면 됩니다.\n앞으로 포스트잇 기능과 에세이 기능이 추가될 예정이니 종종 들려주세요!"
);
const roomName = JSON.parse(document.getElementById("room-name").textContent);
const userId = JSON.parse(document.getElementById("user_id").textContent);
let lastTalk;
const userListRefreshInterval = 3000;
const websocketProtocol =
  window.location.protocol === "https:" ? "wss://" : "ws://";
const smallTalkSocket = new WebSocket(
  websocketProtocol + window.location.host + "/ws/smalltalk/" + roomName + "/"
);

const interval = setInterval(function ping() {
  smallTalkSocket.clients.forEach(function each(ws) {
    if (ws.isAlive === false) return ws.terminate();
    ws.isAlive = false;
    ws.ping(() => {});
  });
}, 30000);

const goToBottom = function () {
  const boxContainer = document.querySelector("#smalltalks");
  boxContainer.scrollTop = boxContainer.scrollHeight;
  let isAtBottom =
    boxContainer.scrollHeight - boxContainer.scrollTop ===
    boxContainer.clientHeight;
  if (isAtBottom) {
    boxContainer.scrollTop = boxContainer.scrollHeight;
  }
};

function userInfoListToHtml(userInfoList) {
  let html = "";
  for (let i = 0; i < userInfoList.length; i++) {
    const thumbnailImageUrl = userInfoList[i].thumbnail_image_url;
    const nickname = userInfoList[i].nickname;
    html += `<div class="user-info"><img src="${thumbnailImageUrl}"><span>${nickname}</span></div>`;
  }
  return html;
}

function createLine(talk, lastTalk = undefined) {
  const isMine = talk.user_id === userId;
  let firstTalkOfTalkSet = false;
  if (!isMine) {
    firstTalkOfTalkSet =
      lastTalk === undefined ? true : lastTalk.dataset.user_id !== talk.user_id;
  }
  const ownClass = isMine ? "mine" : "not-mine";
  const newTalk = document.createElement("div");
  newTalk.dataset.user_id = talk.user_id;
  newTalk.classList.add("chat-line");
  newTalk.classList.add(ownClass);
  if (firstTalkOfTalkSet) {
    newTalk.innerHTML = `<div class="user-thumbnail"><img src="${talk.thumbnail_image_url}"></div>
                                <div class="message-container">
                                    <span class="nickname">${talk.nickname}</span>
                                    <p class="message">${talk.message}</p>
                                </div>`;
  } else {
    newTalk.innerHTML = `<div class="empty-thumbnail"></div>
                                <div class="message-container">
                                    <p class="message">${talk.message}</p>
                                </div>`;
  }
  return newTalk;
}

smallTalkSocket.onmessage = function (e) {
  const type = JSON.parse(e.data).type;
  if (type === "user_info_list") {
    const userInfoList = JSON.parse(e.data).user_info_list;
    document.querySelector("#user-list").innerHTML =
      userInfoListToHtml(userInfoList);
  } else if (type === "talk") {
    const talk = JSON.parse(e.data).talk;
    const newTalk = createLine(talk, lastTalk);
    lastTalk = newTalk;
    document.querySelector("#smalltalks").appendChild(newTalk);
    goToBottom();
  } else if (type === "previous_talks") {
    const previousTalks = JSON.parse(e.data).previous_talks;
    for (let i = 0; i < previousTalks.length; i++) {
      const newTalk = createLine(previousTalks[i], lastTalk);
      lastTalk = newTalk;
      document.querySelector("#smalltalks").appendChild(newTalk);
    }
    goToBottom();
  }
};

smallTalkSocket.onclose = function (e) {
  console.error("채팅이 비정상적으로 종료됐습니다!");
};

document.querySelector("#chat-message-input").focus();
document.querySelector("#chat-message-input").onkeypress = function (e) {
  if (e.keyCode === 13) {
    // enter, return
    document.querySelector("#chat-message-submit").click();
  }
};

document.querySelector("#chat-message-submit").onclick = function (e) {
  const messageInputDom = document.querySelector("#chat-message-input");
  const message = messageInputDom.value;
  smallTalkSocket.send(
    JSON.stringify({
      type: "message",
      content: message,
    })
  );
  messageInputDom.value = "";
};
