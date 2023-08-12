const banner = document.querySelector("#banner");
const bannerContent = document.querySelector("#banner__content");
const bannerClick = document.querySelector("#banner__click");
const getBannerInfo = "/get_expect_winner_url/";

function setBanner() {
  fetch(getBannerInfo)
    .then((data) => {
      return data.json();
    })
    .then((data) => {
      banner.href = data["banner_href"];
      bannerContent.innerHTML = data["banner_content"];
    });
}

setInterval(setBanner, 10000);
