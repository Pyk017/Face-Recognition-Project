let webcamElement, canvasElement, snapSoundElement, webcam;

window.addEventListener("load", () => {
  document.getElementById("startButton").disabled = false;
  document.getElementById("endButton").disabled = true;
  document.getElementById("clickImage").disabled = true;
});

function startButton() {
  webcamElement = document.getElementById("webcam");
  canvasElement = document.getElementById("canvas");
  snapSoundElement = document.getElementById("snapSound");
  webcam = new Webcam(webcamElement, "user", canvasElement, snapSoundElement);
  webcam
    .start()
    .then((result) => {
      console.log("Webcam started");
    })
    .catch((err) => {
      console.log(err);
    });
  document.getElementById("startButton").disabled = true;
  document.getElementById("endButton").disabled = false;
  document.getElementById("clickImage").disabled = false;
}

function endButton() {
  webcamElement = document.getElementById("webcam");
  canvasElement = document.getElementById("canvas");
  snapSoundElement = document.getElementById("snapSound");
  webcam.stop();
  canvasElement.style.removeProperty("transform");
  document.getElementById("startButton").disabled = false;
  document.getElementById("endButton").disabled = true;
  document.getElementById("clickImage").disabled = true;
}

function clickImage() {
  webcamElement = document.getElementById("webcam");
  canvasElement = document.getElementById("canvas");
  snapSoundElement = document.getElementById("snapSound");
  let picture = webcam.snap();

  let container = document.getElementById("row");
  let col = document.createElement("div");
  col.setAttribute("class", "col");
  let img = document.createElement("img");
  img.src = picture;
  img.width = 180;
  img.height = 130;
  col.appendChild(img);
  row.appendChild(col);

  if (container.childNodes.length == 5) {
    document.getElementById("startButton").disabled = true;
    document.getElementById("endButton").disabled = true;
    document.getElementById("clickImage").disabled = true;
    // webcam.stop();

    submitting();
  }
}

function submitting() {
  let submitBtn = document.getElementById("submit");
  submitBtn.style.display = "flex";
  submitBtn.disabled = false;
  webcam.stop();
  document.getElementById("startButton").disabled = true;
  document.getElementById("endButton").disabled = true;
  document.getElementById("clickImage").disabled = true;
}

function resetting() {
  let container = document.getElementById("row");
  let submitBtn = document.getElementById("submit");

  while (container.firstChild) {
    container.removeChild(container.firstChild);
  }

  submitBtn.style.display = "None";
  submitBtn.disabled = true;

  document.getElementById("startButton").disabled = false;
  document.getElementById("endButton").disabled = true;
  document.getElementById("clickImage").disabled = true;
}
