const chatArea = document.querySelector(
  ".chat-scrollable-area__message-container"
);
const twitchChatSocket = new WebSocket(
  "wss://" + "minbungs.site" + "/ws/twitch_chat/" + "twitch" + "/"
);

function callback(mutations) {
  mutations.forEach((mutation) => {
    if (mutation.type === "childList") {
      mutation.addedNodes.forEach((node) => {
        console.log(node);
        const twitchID = node
          .querySelector("span.chat-author__display-name")
          .getAttribute("data-a-user");
        const text = node.querySelector(
          'span[data-a-target="chat-line-message-body"]'
        ).innerText;
        console.log(`${twitchID} : ${text}`);
        twitchChatSocket.send(
          JSON.stringify({
            twitch_id: twitchID,
            message: text,
          })
        );
      });
    }
  });
}
let observer = new MutationObserver(callback);

const options = {
  childList: true,
};
observer.observe(chatArea, options);
