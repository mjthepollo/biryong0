const banner = document.querySelector("#banner");
const bannerContent = document.querySelector("#banner__content");
const bannerClick = document.querySelector("#banner__click");
const getRealTimeInfoUrl = "/get_real_time_info_json/";

function setBanner() {
  fetch(getRealTimeInfoUrl)
    .then((data) => {
      return data.json();
    })
    .then((data) => {
      bannerContent.innerHTML = data["name"] + " 실시간 보러가기";
    });
}

setBanner();
setInterval(setBanner, 10000);
