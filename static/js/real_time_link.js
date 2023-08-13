const matchInfoButton = document.querySelector("#match_info");
const joinMatchButton = document.querySelector("#join_match");

const getRealTimeInfoUrl = "/get_real_time_info_json/";

function getMatchInfoClickFunction(matchUrl) {
  return `window.open("${matchUrl}")`;
}

function getJoinMatchClickFunction(joinMatchFetchUrl) {
  return `fetch("${joinMatchFetchUrl}")`;
}

function setRealTimeInfo() {
  fetch(getRealTimeInfoUrl)
    .then((data) => {
      return data.json();
    })
    .then((data) => {
      if (data.login) {
        joinMatchButton.setAttribute(
          "onclick",
          "alert('로그인이 필요합니다.')"
        );
      } else {
        const matchUrl = data["match_url"];
        const joinMatchFetchUrl = data["join_match_fetch_url"];
        const authenticated = data["authenticated"];
        if (matchUrl) {
          matchInfoButton.setAttribute(
            "onclick",
            getMatchInfoClickFunction(matchUrl)
          );
        }
        if (joinMatchFetchUrl && authenticated) {
          joinMatchButton.setAttribute(
            "onclick",
            getJoinMatchClickFunction(joinMatchFetchUrl)
          );
        } else if (joinMatchFetchUrl && !authenticated) {
          joinMatchButton.setAttribute(
            "onclick",
            "alert('로그인이 필요합니다.')"
          );
        }
      }
    });
}

setRealTimeInfo();
setInterval(setRealTimeInfo, 5000);
