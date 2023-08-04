const expectWinner = document.querySelector("#expect_winner");
const votePOG = document.querySelector("#vote_POG");
const getExpectWinnerUrl = "/get_expect_winner_url/";
const getVotePOGUrl = "/get_vote_POG_url/";
let expectWinnerInnerHTML = "";
let expectWinnerHref = "";
let expectWinnerActive = false;
let votePOGInnerHTML = "";
let votePOGHref = "";
let votePOGActive = false;

function setExpectWinner() {
  fetch(getExpectWinnerUrl)
    .then((data) => {
      return data.json();
    })
    .then((data) => {
      expectWinnerInnerHTML = data["inner_html"];
      expectWinnerHref = data["href"];
      expectWinnerActive = data["active"];
      expectWinner.innerHTML = expectWinnerInnerHTML;
      expectWinner.href = expectWinnerHref;
      if (expectWinnerActive) {
        expectWinner.classList.add("active");
        expectWinner.setAttribute("target", "_blank");
      } else {
        expectWinner.classList.remove("active");
        expectWinner.removeAttribute("target");
        expectWinner.href = "javascript:void(0)";
      }
    });
}
function setVotePOGUrl() {
  fetch(getVotePOGUrl)
    .then((data) => {
      return data.json();
    })
    .then((data) => {
      votePOGInnerHTML = data["inner_html"];
      votePOGHref = data["href"];
      votePOGActive = data["active"];
      votePOG.innerHTML = votePOGInnerHTML;
      votePOG.href = votePOGHref;
      if (votePOGActive) {
        votePOG.classList.add("active");
        votePOG.setAttribute("target", "_blank");
      } else {
        votePOG.classList.remove("active");
        votePOG.removeAttribute("target");
        votePOG.href = "javascript:void(0)";
      }
    });
}

setInterval(setExpectWinner, 10000);
setInterval(setVotePOGUrl, 10000);
setExpectWinner();
setVotePOGUrl();
