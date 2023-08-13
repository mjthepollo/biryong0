const streaming = document.getElementById("streaming");
const ratio = 9 / 16;
function setStreamingHeight() {
  const responsiveHeight = streaming.offsetWidth * ratio;
  streaming.setAttribute("height", responsiveHeight);
}

setStreamingHeight();
window.addEventListener("resize", setStreamingHeight);
